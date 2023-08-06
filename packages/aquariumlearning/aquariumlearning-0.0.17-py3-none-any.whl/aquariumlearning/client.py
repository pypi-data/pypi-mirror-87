"""client.py
============
The main client module.
"""

import os
import datetime
import time
import json
import requests
import shutil
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import ConnectionError
from uuid import uuid4
from io import BytesIO
from tempfile import NamedTemporaryFile, gettempdir
from math import floor, pow
from google.resumable_media.requests import ResumableUpload
from google.resumable_media.common import InvalidResponse, DataCorruption
from tqdm import tqdm
import sys
import pyarrow as pa
import numpy as np
import pandas as pd
from .viridis import viridis_rgb
from .turbo import turbo_rgb
from .util import raise_resp_exception_error
from .issues import IssueManager
import re

retry_strategy = Retry(
    total=4,
    backoff_factor=1,
    status_forcelist=[404, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"],
)
retry_adapter = HTTPAdapter(max_retries=retry_strategy)
requests_retry = requests.Session()
requests_retry.mount("https://", retry_adapter)
requests_retry.mount("http://", retry_adapter)


def create_temp_directory():
    current_temp_directory = gettempdir()
    temp_path = os.path.join(current_temp_directory, "aquarium_learning_disk_cache")
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    return temp_path


TEMP_FILE_PATH = create_temp_directory()

TYPE_PRIMITIVE_TO_STRING_MAP = {
    str: "str",
    int: "int",
    float: "float",
    bool: "bool",
}

MAX_FRAMES_PER_BATCH = 1000
MAX_CHUNK_SIZE = int(pow(2, 23))  # 8 MiB


def _is_one_gb_available():
    """Returns true if there is more than 1 GB available on the current filesystem"""
    return shutil.disk_usage("/").free > pow(1024, 3)  # 1 GB


def assert_valid_name(name):
    is_valid = re.match(r"^[A-Za-z0-9_]+$", name)
    if not is_valid:
        raise Exception(
            "Name {} must only contain alphanumeric and underscore characters".format(
                name
            )
        )


class CustomMetricsDefinition:
    """Definitions for custom user provided metrics.

    Args:
        name (str): The name of this metric.
        metrics_type (str): The metrics type, either 'objective' or 'confusion_matrix'.
    """

    OBJECTIVE = "objective"
    CONFUSION_MATRIX = "confusion_matrix"

    def __init__(self, name, metrics_type):
        valid_metrics_types = set(["objective", "confusion_matrix"])
        self.name = name
        self.metrics_type = metrics_type

    def to_dict(self):
        return {"name": self.name, "metrics_type": self.metrics_type}


class Client:
    """Client class that interacts with the Aquarium REST API.

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    def __init__(self, *, api_endpoint="https://illume.aquariumlearning.com/api/v1"):
        self._creds_token = None
        self._creds_app_id = None
        self._creds_app_key = None
        self._creds_api_key = None
        self.api_endpoint = api_endpoint

    def _get_creds_headers(self):
        """Get appropriate request headers for the currently set credentials.

        Raises:
            Exception: No credentials set.

        Returns:
            dict: Dictionary of headers
        """
        if self._creds_token:
            return {"Authorization": "Bearer {token}".format(token=self._creds_token)}
        elif self._creds_api_key:
            return {"x-illume-api-key": self._creds_api_key}
        elif self._creds_app_id and self._creds_app_key:
            return {
                "x-illume-app": self._creds_app_id,
                "x-illume-key": self._creds_app_key,
            }
        else:
            raise Exception("No credentials set.")

    def set_credentials(self, *, token=None, app_id=None, app_key=None, api_key=None):
        """Set credentials for the client.

        Args:
            api_key (str, optional): A string for a long lived API key. Defaults to None.
            token (str, optional): A JWT providing auth credentials. Defaults to None.
            app_id (str, optional): Application ID string. Defaults to None.
            app_key (str, optional): Application secret key. Defaults to None.

        Raises:
            Exception: Invalid credential combination provided.
        """
        if api_key is not None:
            self._creds_api_key = api_key
        elif token is not None:
            self._creds_token = token
        elif app_id is not None and app_key is not None:
            self._creds_app_id = app_id
            self._creds_app_key = app_key
        else:
            raise Exception(
                "Please provide either an api_key, token, or app_id and app_key"
            )

    def _format_error_logs(self, raw_error_logs):
        """Format error log data into strings.

        Args:
            raw_error_logs (list[dict]): Error log data.

        Returns:
            list[str]: list of string formatted error messages.
        """
        formatted_lines = []
        for raw in raw_error_logs:
            formatted_lines.append(
                f"    {raw.get('aquarium_dataflow_step', '')}: {raw.get('msg', '')}"
            )
        return formatted_lines

    def get_issue_manager(self, project_id):
        """Get an issue manager object.

        Args:
            project_id (str): Project ID to manage.

        Returns:
            IssueManager: The issue manager object.
        """
        return IssueManager(self, project_id)

    def get_projects(self):
        """Get info about existing projects

        Returns:
            list of dict: Project Info
        """
        r = requests_retry.get(
            self.api_endpoint + "/projects", headers=self._get_creds_headers()
        )

        raise_resp_exception_error(r)
        return r.json()

    def delete_project(self, project_id):
        """Mark a project for deletion

        Args:
            project_id (str): project_id
        """
        if not self.project_exists(project_id):
            raise Exception("Project {} does not exist.".format(project_id))

        url = self.api_endpoint + "/projects/{}".format(project_id)
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def project_exists(self, project_id):
        """Checks whether a project exists.

        Args:
            project_id (str): project_id

        Returns:
            bool: Does project exist
        """
        projects = self.get_projects()
        existing_project_ids = [project["id"] for project in projects]
        return project_id in existing_project_ids

    def create_project(
        self,
        project_id,
        label_class_map,
        primary_task=None,
        secondary_labels=None,
        frame_links=None,
        label_links=None,
        default_camera_target=None,
        default_camera_position=None,
        custom_metrics=None,
        max_shown_categories=None,
    ):
        """Create a new project via the REST API.

        Args:
            project_id (string): project_id
            label_class_map (LabelClassMap): The label class map used to interpret classifications.
            primary_task (str, optional): Any specific primary task for a non-object detection or classification task. Can be '2D_SEMSEG' or None.
            secondary_labels (list, optional): List of secondary labels in classification tasks
            frame_links (list of str, optional): List of string keys for links between frames
            label_links (list of str, optional): List of string keys for links between labels
            default_camera_target (list of float, optional): For 3D scenes, the default camera target
            default_camera_position (list of float, optional): For 3D scenes, the default camera position
            custom_metrics (CustomMetricsDefinition or list of CustomMetricsDefinition): Defines which custom metrics exist for this project, defaults to None.
            max_shown_categories (int, optional): For categorical visualizations, set the maximum shown simultaneously. Max 100.
        """

        assert_valid_name(project_id)

        if not isinstance(label_class_map, LabelClassMap):
            raise Exception("label_class_map must be a LabelClassMap")

        if not label_class_map.entries:
            raise Exception("label_class_map must have at least one class")

        dumped_classmap = [x.to_dict() for x in label_class_map.entries]
        payload = {"project_id": project_id, "label_class_map": dumped_classmap}

        if primary_task is not None:
            payload["primary_task"] = primary_task
        if secondary_labels is not None:
            dumped_secondary_labels = []
            for raw in secondary_labels:
                dumped_classmap = [x.to_dict() for x in raw["label_class_map"].entries]
                raw["label_class_map"] = dumped_classmap
                dumped_secondary_labels.append(raw)

            payload["secondary_labels"] = dumped_secondary_labels
        if frame_links is not None:
            if not isinstance(frame_links, list):
                raise Exception("frame_links must be a list of strings")
            payload["frame_links"] = frame_links
        if label_links is not None:
            if not isinstance(label_links, list):
                raise Exception("label_links must be a list of strings")
            payload["label_links"] = label_links
        if default_camera_position is not None:
            if not isinstance(default_camera_position, list):
                raise Exception("default_camera_position must be a list of floats")
            payload["default_camera_position"] = default_camera_position
        if default_camera_target is not None:
            if not isinstance(default_camera_target, list):
                raise Exception("default_camera_target must be a list of floats")
            payload["default_camera_target"] = default_camera_target
        if custom_metrics is not None:
            if isinstance(custom_metrics, CustomMetricsDefinition):
                custom_metrics = [custom_metrics]

            if (
                not custom_metrics
                or (not isinstance(custom_metrics, list))
                or (not isinstance(custom_metrics[0], CustomMetricsDefinition))
            ):
                raise Exception(
                    "custom_metrics must be a CustomMetricsDefinition or list of CustomMetricsDefinition."
                )

            serializable = [x.to_dict() for x in custom_metrics]
            payload["custom_metrics"] = serializable

        if max_shown_categories is not None:
            if not isinstance(max_shown_categories, int):
                raise Exception("max_shown_categories must be an int")
            if max_shown_categories < 1 or max_shown_categories > 100:
                raise Exception("max_shown_categories must be between 1 and 100")
            payload["max_shown_categories"] = max_shown_categories

        r = requests_retry.post(
            self.api_endpoint + "/projects",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def _preview_frame_dict(self, project_id, both_frames_dict):
        """Generate preview with both dataset frame and inference frame as dict

        Args:
            project_id (str): name of project to preview frame with
            both_frames_dict (dict): Dictionary containing the labeled and inference frame
        """
        api_path = "/projects/{}/preview_frame".format(project_id)

        preview_frame_api_root = self.api_endpoint + api_path

        r = requests_retry.post(
            preview_frame_api_root,
            headers=self._get_creds_headers(),
            json=both_frames_dict,
        )
        response_data = r.json()
        if response_data.get("preview_frame_uuid"):
            print("Please visit the following url to preview your frame in the webapp")
            url = (
                self.api_endpoint[:-7]
                + api_path
                + "/"
                + response_data["preview_frame_uuid"]
            )
            print(url)
        else:
            raise Exception(
                "Preview URL could not be constructed by server. "
                "Please make sure you're logged in and check frame data accordingly."
            )

    def preview_frame(self, project_id, labeled_frame, inference_frame=None):
        """prints out a URL that lets you preview a provided frame in the web browser
        Useful for debugging data and image url issues.

        Args:
            project_id (str): Name of project to be associated for this frame preview (for label class association)
            labeled_frame (LabeledFrame): Labeled Frame desired for preview in web-app
            inference_frame (InferenceFrame, optional): Labeled Inference Desired for preview in web-app
        """

        both_frames = {}
        both_frames["labeled_frame"] = labeled_frame.to_dict()
        both_frames["inference_frame"] = (
            inference_frame.to_dict() if inference_frame else None
        )
        self._preview_frame_dict(project_id, both_frames)

    def get_datasets(self, project_id):
        """Get existing datasets for a project.

        Args:
            project_id (str): The project id.

        Returns:
            list: A list of dataset info for the project.
        """
        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_id
        )
        r = requests_retry.get(datasets_api_root, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        return r.json()

    def delete_dataset(self, project_id, dataset_id):
        """Mark a dataset for deletion

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
        """
        if not self.dataset_exists(project_id, dataset_id):
            raise Exception("Dataset {} does not exist.".format(dataset_id))

        url = self.api_endpoint + "/projects/{}/datasets/{}".format(
            project_id, dataset_id
        )
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def dataset_exists(self, project_id, dataset_id):
        """Check if a dataset exists.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            bool: Whether the dataset already exists.
        """
        datasets = self.get_datasets(project_id)
        existing_dataset_ids = [dataset.get("id") for dataset in datasets]
        return dataset_id in existing_dataset_ids

    def is_dataset_processed(self, project_id, dataset_id):
        """Check if a dataset is fully processed.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            bool: If the dataset is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/is_processed".format(project_id, dataset_id)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["processed"]

    def get_dataset_ingest_error_logs(self, project_id, dataset_id):
        """Get ingest error log entries for a dataset.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/ingest_error_logs".format(
                project_id, dataset_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed

    def current_dataset_process_state(self, project_id, dataset_id):
        """Current processing state of a dataset.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/process_state".format(project_id, dataset_id)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def inferences_exists(self, project_id, dataset_id, inferences_id):
        """Check if a set of inferences exists.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id (str): inferences_id

        Returns:
            bool: Whether the inferences id already exists.
        """
        # TODO: FIXME: We need a first class model for inferences,
        # not just name gluing
        inferences_dataset_id = "_".join(["inferences", dataset_id, inferences_id])
        datasets = self.get_datasets(project_id)
        existing_dataset_ids = [dataset.get("id") for dataset in datasets]
        return inferences_dataset_id in existing_dataset_ids

    def is_inferences_processed(self, project_id, dataset_id, inferences_id):
        """Check if a set of inferences is fully processed.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            bool: If the inferences set is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/is_processed".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["processed"]

    def get_inferences_ingest_error_logs(self, project_id, dataset_id, inferences_id):
        """Get ingest error log entries for an inference set.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/ingest_error_logs".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed

    def current_inferences_process_state(self, project_id, dataset_id, inferences_id):
        """current processing state of inferences.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id(str): inferences_id

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/process_state".format(
                project_id, dataset_id, inferences_id
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def upload_asset_from_filepath(self, project_id, dataset_id, filepath):
        """Upload an asset from a local file path.
        This is useful in cases where you have data on your local machine that you want to mirror in aquarium.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            filepath (str): The filepath to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """

        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )

        upload_filename = os.path.basename(filepath)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url = urls["download_url"]

        with open(filepath, "rb") as f:
            upload_resp = requests_retry.put(put_url, data=f)

        raise_resp_exception_error(upload_resp)
        return download_url

    def upload_asset_from_url(self, project_id, dataset_id, source_url):
        """Upload an asset from a private url.
        This is useful in cases where you have data easily accessible on your network that you want to mirror in aquarium.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            source_url (str): The source url to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )

        upload_filename = os.path.basename(source_url)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url = urls["download_url"]

        dl_resp = requests_retry.get(source_url)
        payload = BytesIO(dl_resp.content)

        upload_resp = requests_retry.put(put_url, data=payload)

        raise_resp_exception_error(upload_resp)
        return download_url

    def _upload_rows_from_writer(
        self, project_id, dataset_id, upload_filename, writefunc
    ):
        # Get upload / download URLs
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )
        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )
        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url = urls["download_url"]

        # Serialize to jsonlines
        data_rows_content = NamedTemporaryFile(mode="w", delete=False)
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            data_rows_content.close()
            os.remove(data_rows_content_path)
            return None

        data_rows_content.seek(0)
        data_rows_content.close()

        # Upload
        ## Cannot use the same writing file handle to read, so we use a new file handle
        ## to open the file to read
        with open(data_rows_content_path, "rb") as content_reader:
            upload_resp = requests_retry.put(put_url, data=content_reader)
        raise_resp_exception_error(upload_resp)
        os.remove(data_rows_content_path)

        return download_url

    def _upload_rows_from_files(
        self, project_id, dataset_id, upload_prefix, upload_suffix, file_names
    ):
        # Get upload / download URLs
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(project_id, dataset_id)
        )
        download_urls = []
        if len(file_names) == 0:
            return download_urls

        all_files_bytes = sum([os.path.getsize(file_name) for file_name in file_names])
        with tqdm(
            total=all_files_bytes,
            file=sys.stdout,
            unit="B",
            unit_scale=True,
            desc="Upload Progress",
        ) as pbar:
            for count, file_name in enumerate(file_names, start=1):
                upload_filename = (
                    f"{upload_prefix}_batch_{str(count).zfill(6)}{upload_suffix}"
                )

                params = {
                    "upload_filename": upload_filename,
                    "resumable_upload": "true",
                }
                upload_url_resp = requests_retry.get(
                    get_upload_path, headers=self._get_creds_headers(), params=params
                )
                raise_resp_exception_error(upload_url_resp)
                urls = upload_url_resp.json()
                put_url = urls["put_url"]
                download_url = urls["download_url"]
                download_urls.append(download_url)

                # Upload and Delete
                ## This uploads the file with a reader, and then deletes it.

                xml_api_headers = {
                    "x-goog-resumable": "start",
                    "content-type": "application/octet-stream",
                }
                upload = ResumableUpload(
                    put_url, MAX_CHUNK_SIZE, headers=xml_api_headers
                )

                with open(file_name, "rb") as content_reader:
                    pbar.write(
                        f"Uploading file {str(count).zfill(len(str(len(file_names))))}/{str(len(file_names))}"
                    )
                    upload.initiate(
                        requests_retry, content_reader, {}, "application/octet-stream"
                    )
                    last_upload_bytes = 0
                    while not upload.finished:
                        try:
                            upload.transmit_next_chunk(requests_retry)
                        except (InvalidResponse, DataCorruption):
                            if upload.invalid:
                                upload.recover(requests_retry)
                            continue
                        except ConnectionError:
                            upload.recover(requests_retry)
                            continue
                        pbar.update(upload.bytes_uploaded - last_upload_bytes)
                        last_upload_bytes = upload.bytes_uploaded

                os.remove(file_name)

        return download_urls

    def create_dataset(
        self,
        project_id,
        dataset_id,
        data_url=None,
        embeddings_url=None,
        dataset=None,
        wait_until_finish=False,
        wait_timeout=datetime.timedelta(hours=2),
        embedding_distance_metric="euclidean",
        preview_first_frame=False,
    ):
        """Create a dataset with the provided data urls.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            dataset: (LabeledDataset, optional): The LabeledDataset to upload.
            data_url (str, optional): A URL to the serialized dataset entries.
            embeddings_url (str, optional): A URL to the serialized dataset embeddings. Defaults to None.
            wait_until_finish (bool, optional): Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout (timedelta, optional): Maximum time to wait for. Defaults to 2 hours.
            embedding_distance_metric (string, optional): Distance metric to use for embedding layout. Can be a member of ['euclidean', 'cosine']. Defaults to 'euclidean'.
            preview_first_frame (bool, optional): preview the first frame of the dataset in the webapp before continuing. Requires interaction.
        """

        assert_valid_name(dataset_id)

        if embedding_distance_metric not in ["euclidean", "cosine"]:
            raise Exception("embedding_distance_metric must be euclidean or cosine.")

        if not isinstance(wait_timeout, datetime.timedelta):
            raise Exception("wait_timeout must be a datetime.timedelta object")

        if self.dataset_exists(project_id, dataset_id):
            raise Exception("Dataset already exists.")

        if dataset:
            dataset._flush_to_disk()

            if len(dataset._temp_frame_file_names) == 0:
                raise Exception("Cannot create dataset with 0 frames")

            if preview_first_frame:
                first_frame_dict = dataset.get_first_frame_dict()
                self._preview_frame_dict(
                    project_id,
                    {"labeled_frame": first_frame_dict, "inference_frame": None},
                )
                user_response = input(
                    "Please vist above URL to see your Preview frame.\n\n"
                    "Press ENTER to continue or type `exit` and press ENTER "
                    "to cancel dataset upload.\n"
                )
                if user_response == "exit":
                    print("Canceling dataset upload!")
                    return

            print("Uploading Labeled Dataset...")
            upload_prefix = "{}_data".format(str(uuid4()))
            upload_suffix = ".jsonl"
            final_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                dataset._temp_frame_file_names,
            )
        elif data_url:
            final_urls = [
                data_url,
            ]
        else:
            raise Exception("Please provide either a data_url or dataset argument")

        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_id
        )
        payload = {
            "dataset_id": dataset_id,
            "data_url": final_urls,
            "embedding_distance_metric": embedding_distance_metric,
            "embedding_upload_version": 1,
        }

        if dataset and dataset._temp_frame_embeddings_file_names:
            print("Uploading Labeled Dataset Embeddings...")
            upload_prefix = "{}_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                dataset._temp_frame_embeddings_file_names,
            )
            if uploaded_urls:  # not empty list
                payload["embeddings_url"] = uploaded_urls
        elif embeddings_url:
            payload["embeddings_url"] = [
                embeddings_url,
            ]

        print("Dataset Processing Initiating...")
        r = requests_retry.post(
            datasets_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print("Dataset Processing Initiated Successfully")

        if wait_until_finish:
            with tqdm(
                total=100.0,
                file=sys.stdout,
                unit_scale=True,
                desc="Dataset Processing Progress",
            ) as pbar:
                start_time = datetime.datetime.now()
                processing_state = "PENDING"
                display_processing_state = (
                    lambda state: f"Dataset Processing Status: {state}"
                )
                pbar.write(display_processing_state(processing_state))
                while (datetime.datetime.now() - start_time) < wait_timeout:
                    (
                        new_processing_state,
                        new_percent_done,
                    ) = self.current_dataset_process_state(project_id, dataset_id)
                    pbar.update(new_percent_done - pbar.n)
                    if new_processing_state != processing_state:
                        processing_state = new_processing_state
                        pbar.write(display_processing_state(processing_state))
                    processed = self.is_dataset_processed(
                        project_id=project_id, dataset_id=dataset_id
                    )
                    if processed:
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Dataset is fully processed.")
                        break
                    if processing_state == "FAILED":
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Dataset processing has failed. Exiting...")
                        raw_logs = self.get_dataset_ingest_error_logs(
                            project_id, dataset_id
                        )
                        formatted = self._format_error_logs(raw_logs)
                        for entry in formatted:
                            print(entry)

                        break
                    else:
                        time.sleep(10)

                if datetime.datetime.now() - start_time >= wait_timeout:
                    pbar.close()
                    print("Exceeded timeout waiting for job completion.")

    # TODO: Check if the inferences already exist
    def create_inferences(
        self,
        project_id,
        dataset_id,
        inferences_id,
        data_url=None,
        embeddings_url=None,
        inferences=None,
        wait_until_finish=False,
        wait_timeout=datetime.timedelta(hours=2),
        embedding_distance_metric="euclidean",
    ):
        """Create an inference set with the provided data urls.

        Args:
            project_id (str): project_id
            dataset_id (str): dataset_id
            inferences_id (str): A unique identifier for this set of inferences.
            inferences: (Inferences, optional): The inferences to upload.
            data_url (str, optional): A URL to the serialized inference entries.
            embeddings_url (str, optional): A URL to the serialized inference embeddings. Defaults to None.
            wait_until_finish (bool, optional): Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout (timedelta, optional): Maximum time to wait for. Defaults to 2 hours.
            embedding_distance_metric (string, optional): Distance metric to use for embedding layout. Can be a member of ['euclidean', 'cosine']. Defaults to 'euclidean'.
        """

        assert_valid_name(dataset_id)
        assert_valid_name(inferences_id)

        if embedding_distance_metric not in ["euclidean", "cosine"]:
            raise Exception("embedding_distance_metric must be euclidean or cosine.")

        if not isinstance(wait_timeout, datetime.timedelta):
            raise Exception("wait_timeout must be a datetime.timedelta object")

        if self.inferences_exists(project_id, dataset_id, inferences_id):
            raise Exception("Inferences already exists.")

        inferences_api_root = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences".format(project_id, dataset_id)
        )

        if inferences:
            inferences._flush_to_disk()
            print("Uploading Inferences...")
            upload_prefix = "{}_data".format(str(uuid4()))
            upload_suffix = ".jsonl"
            final_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                inferences._temp_frame_file_names,
            )
        elif data_url:
            final_urls = [
                data_url,
            ]
        else:
            raise Exception("Please provide either a data_url or dataset argument")

        payload = {
            "inferences_id": inferences_id,
            "data_url": final_urls,
            "embedding_distance_metric": embedding_distance_metric,
            "embedding_upload_version": 1,
        }

        if inferences and inferences._temp_frame_embeddings_file_names:
            print("Uploading Inference Embeddings...")
            upload_prefix = "{}_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_id,
                dataset_id,
                upload_prefix,
                upload_suffix,
                inferences._temp_frame_embeddings_file_names,
            )
            if uploaded_urls:  # not empty list
                payload["embeddings_url"] = uploaded_urls
        elif embeddings_url:
            payload["embeddings_url"] = [
                embeddings_url,
            ]

        print("Inferences Processing Initiating...")
        r = requests_retry.post(
            inferences_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print("Inferences Processing Initiated Successfully")

        if wait_until_finish:
            with tqdm(
                total=100.0,
                file=sys.stdout,
                unit_scale=True,
                desc="Inferences Processing Progress",
            ) as pbar:
                start_time = datetime.datetime.now()
                processing_state = "PENDING"
                display_processing_state = (
                    lambda state: f"Inferences Processing State: {state}"
                )
                pbar.write(display_processing_state(processing_state))
                while (datetime.datetime.now() - start_time) < wait_timeout:
                    (
                        new_processing_state,
                        new_percent_done,
                    ) = self.current_inferences_process_state(
                        project_id, dataset_id, inferences_id
                    )
                    pbar.update(new_percent_done - pbar.n)
                    if new_processing_state != processing_state:
                        processing_state = new_processing_state
                        pbar.write(display_processing_state(processing_state))
                    processed = self.is_inferences_processed(
                        project_id=project_id,
                        dataset_id=dataset_id,
                        inferences_id=inferences_id,
                    )
                    if processed:
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Inferences are fully processed.")
                        break
                    if processing_state == "FAILED":
                        pbar.update(100.0 - pbar.n)
                        pbar.close()
                        print("Inferences processing has failed. Exiting...")
                        raw_logs = self.get_inferences_ingest_error_logs(
                            project_id, dataset_id, inferences_id
                        )
                        formatted = self._format_error_logs(raw_logs)
                        for entry in formatted:
                            print(entry)

                        break
                    else:
                        time.sleep(10)

                if datetime.datetime.now() - start_time >= wait_timeout:
                    pbar.close()
                    print("Exceeded timeout waiting for job completion.")


class LabeledDataset:
    """A container used to construct a labeled dataset.

    Typical usage is to create a LabeledDataset, add multiple LabeledFrames to it,
    then serialize the frames to be submitted.
    """

    def __init__(self):
        self._frames = []
        self._frame_ids_set = set()
        current_time = datetime.datetime.now()
        self._temp_frame_prefix = "al_{}_dataset_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_dataset_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []

    def get_first_frame_dict(self):
        first_frame_file_name = self._temp_frame_file_names[0]
        with open(first_frame_file_name, "r") as first_frame_file:
            first_frame_json = first_frame_file.readline().strip()
            return json.loads(first_frame_json)

    def _save_rows_to_temp(self, file_name_prefix, writefunc, mode="w"):
        """[summary]

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=TEMP_FILE_PATH
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def _flush_to_disk(self):
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if len(self._frames) == 0:
            return
        frame_path = self._save_rows_to_temp(
            self._temp_frame_prefix, lambda x: self.write_to_file(x)
        )
        if frame_path:
            self._temp_frame_file_names.append(frame_path)
        embeddings_path = self._save_rows_to_temp(
            self._temp_frame_embeddings_prefix,
            lambda x: self.write_embeddings_to_file(x),
            mode="wb",
        )
        if embeddings_path:
            self._temp_frame_embeddings_file_names.append(embeddings_path)
        self._frames = []

    def add_frame(self, frame):
        """Add a LabeledFrame to this dataset.

        Args:
            frame (LabeledFrame): A LabeledFrame in this dataset.
        """
        if not isinstance(frame, LabeledFrame):
            raise Exception("Frame is not an LabeledFrame")

        if frame.frame_id in self._frame_ids_set:
            raise Exception("Attempted to add duplicate frame id.")

        self._frames.append(frame)
        self._frame_ids_set.add(frame.frame_id)
        if len(self._frames) >= MAX_FRAMES_PER_BATCH:
            self._flush_to_disk()

    def write_to_file(self, filelike):
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame.to_dict()
            filelike.write(json.dumps(row) + "\n")

    def write_embeddings_to_file(self, filelike):
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # Get the first frame embedding dimension
        frame_embedding_dim = len(self._frames[0].embedding["embedding"])
        # Get the first crop embedding dimension
        crop_embedding_dim = 1
        for frame in self._frames:
            if frame.embedding["crop_embeddings"]:
                first_crop_emb = frame.embedding["crop_embeddings"][0]
                crop_embedding_dim = len(first_crop_emb["embedding"])
                break

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_ids[i] = frame.embedding["task_id"]
            frame_embeddings[i] = frame.embedding["embedding"]
            crop_ids[i] = [x["uuid"] for x in frame.embedding["crop_embeddings"]]
            crop_embeddings[i] = [
                x["embedding"] for x in frame.embedding["crop_embeddings"]
            ]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()


class LabeledFrame:
    """A labeled frame for a dataset.

    Args:
        frame_id (str): A unique id for this frame.
        date_captured (str, optional): ISO formatted datetime string. Defaults to None.
        device_id (str, optional): The device that generated this frame. Defaults to None.
    """

    def __init__(self, *, frame_id, date_captured=None, device_id=None):
        if not isinstance(frame_id, str):
            raise Exception("frame ids must be strings")

        if "/" in frame_id:
            raise Exception("frame ids cannot contain slashes (/)")

        self.frame_id = frame_id

        if date_captured is not None:
            self.date_captured = date_captured
        else:
            self.date_captured = str(datetime.datetime.now())

        if device_id is not None:
            self.device_id = device_id
        else:
            self.device_id = "default_device"

        self.coordinate_frames = []
        self.sensor_data = []
        self.label_data = []
        self.geo_data = {}
        self.user_metadata = []
        self.embedding = None

        self._coord_frame_ids_set = set()

    def _add_coordinate_frame(self, coord_frame_obj):
        self.coordinate_frames.append(coord_frame_obj)
        self._coord_frame_ids_set.add(coord_frame_obj["coordinate_frame_id"])

    def _coord_frame_exists(self, coord_frame):
        return coord_frame in self._coord_frame_ids_set

    # TODO: Better datamodel for embeddings, make it more first class
    def add_embedding(self, *, embedding, crop_embeddings=None, model_id=""):
        """Add an embedding to this frame, and optionally to crops/labels within it.

        If provided, "crop_embeddings" is a list of dicts of the form:
            'uuid': the label id for the crop/label
            'embedding': a vector of floats between length 0 and 12,000.

        Args:
            embedding (list of floats): A vector of floats between length 0 and 12,000.
            crop_embeddings (list of dicts, optional): A list of dictionaries representing crop embeddings. Defaults to None.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """
        if crop_embeddings is None:
            crop_embeddings = []

        if not embedding or len(embedding) > 12000:
            raise Exception("Length of embeddings should be between 0 and 12,000")

        self.embedding = {
            "image_url": "",
            "task_id": self.frame_id,
            "crop_embeddings": crop_embeddings,
            "model_id": model_id,
            "date_generated": str(datetime.datetime.now()),
            "embedding": embedding,
        }

    def add_label_text_token(
        self, *, sensor_id, label_id, index, token, classification, visible
    ):
        """Add a label for a text token.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            index (int): the index of this token in the text
            token (str): the text content of this token
            classification (str): the classification string
            visible (bool): is this a visible token in the text

        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"index": index, "token": token, "visible": visible}
        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "TEXT_TOKEN",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    # TODO: Dedupe code between here and inferences
    def add_label_3d_cuboid(
        self,
        *,
        label_id,
        classification,
        position,
        dimensions,
        rotation,
        iscrowd=None,
        user_attrs=None,
        links=None,
        coord_frame_id=None,
    ):
        """Add a label for a 3D cuboid.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            position (list of float): the position of the center of the cuboid
            dimensions (list of float): the dimensions of the cuboid
            rotation (list of float): the local rotation of the cuboid, represented as an xyzw quaternion.
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
            coord_frame_id (str, optional): Coordinate frame id. Defaults to 'world'
        """
        if coord_frame_id is None:
            coord_frame_id = "world"

        if not self._coord_frame_exists(coord_frame_id):
            raise Exception("Sensor id {} does not exists.".format(coord_frame_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")
        attrs = {
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "dim_x": dimensions[0],
            "dim_y": dimensions[1],
            "dim_z": dimensions[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
            "rot_w": rotation[3],
        }

        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        if user_attrs is not None:
            for k, v in user_attrs.items():
                if "user__" not in k:
                    k = "user__" + k
                attrs[k] = v

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CUBOID_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": attrs,
            }
        )

    # TODO: Dedupe code between here and inferences
    def add_label_2d_bbox(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        top,
        left,
        width,
        height,
        iscrowd=None,
        user_attrs=None,
        links=None,
    ):
        """Add a label for a 2D bounding box.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"top": top, "left": left, "width": width, "height": height}
        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        if user_attrs is not None:
            for k, v in user_attrs.items():
                if "user__" not in k:
                    k = "user__" + k
                attrs[k] = v

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "BBOX_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_label_2d_keypoints(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        top,
        left,
        width,
        height,
        keypoints,
        user_attrs=None,
    ):
        """Add a label for a 2D keypoints task.

        A keypoint is a dictionary of the form:
            'x': x-coordinate in pixels
            'y': y-coordinate in pixels
            'name': string name of the keypoint

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            keypoints (list of dicts): The keypoints of this detection
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "keypoints": keypoints,
        }

        if user_attrs is not None:
            for k, v in user_attrs.items():
                if "user__" not in k:
                    k = "user__" + k
                attrs[k] = v

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "KEYPOINTS_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_label_2d_polygon_list(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        polygons,
        center=None,
    ):
        """Add a label for a 2D polygon list instance segmentation task.

        Polygons are dictionaries of the form:
            'vertices': list of (x, y)

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            polygons (list of dicts): The polygon geometry
            center (list of ints or floats, optional): The center point of the instance
        """

        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"polygons": polygons, "center": center}

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "POLYGON_LIST_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_label_2d_semseg(self, *, sensor_id, label_id, mask_url):
        """Add a label for 2D semseg.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            mask_url (str): URL to the pixel mask png.
        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label": "__mask",
                "label_coordinate_frame": sensor_id,
                "label_type": "SEMANTIC_LABEL_URL_2D",
                "attributes": {"url": mask_url},
            }
        )

    def add_label_2d_classification(
        self, *, sensor_id, label_id, classification, secondary_labels=None
    ):
        """Add a label for 2D classification.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            secondary_labels (dict, optional): dictionary of secondary labels
        """
        if not self._coord_frame_exists(sensor_id):
            raise Exception("Sensor id {} does not exists.".format(sensor_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {}
        if secondary_labels is not None:
            for k, v in secondary_labels.items():
                attrs[k] = v

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_label_3d_classification(
        self,
        *,
        label_id,
        classification,
        coord_frame_id=None,
    ):
        """Add a label for 3D classification.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            coord_frame_id (str, optional): The coordinate frame id.
        """

        if coord_frame_id is None:
            coord_frame_id = "world"

        if not self._coord_frame_exists(coord_frame_id):
            raise Exception("Coord frame {} does not exists.".format(coord_frame_id))

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": {},
            }
        )

    def add_user_metadata(self, key, val, val_type=None):
        """Add a user provided metadata field.

        The types of these metadata fields will be infered and they'll be made
        available in the app for querying and metrics.

        Args:
            key (str): The key for your metadata field
            val (str, int, float, or bool): value
            val_type (str): type of val as string as must be part of list ["str", "int", "float", "bool"]
        """
        assert_valid_name(key)
        # Validates that neither val or type is None
        if val is None and val_type is None:
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata key {key} must provide "
                f"scalar value or expected type of scalar value if None"
            )
        # Validates that val has an accepted type
        if val is not None and type(val) not in TYPE_PRIMITIVE_TO_STRING_MAP:
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata Value {val} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )
        # Validates that val_type has an accepted type
        if val_type and val_type not in TYPE_PRIMITIVE_TO_STRING_MAP.values():
            raise Exception(
                f"For frame_id {self.frame_id}: User Metadata Value Type {val_type} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )

        # Sets val_type if it is not set
        if val is not None and not val_type:
            val_type = TYPE_PRIMITIVE_TO_STRING_MAP[type(val)]

        # Checks that inferred type matches what the user put in val_type
        if val is not None:
            for (
                primitive,
                type_string,
            ) in TYPE_PRIMITIVE_TO_STRING_MAP.items():
                if type(val) is primitive and val_type != type_string:
                    raise Exception(
                        f"For frame_id {self.frame_id}, metadata key: {key}, value: {val}, "
                        f"type is inferred as {type_string} but provided type was {val_type}"
                    )

        self.user_metadata.append((key, val, val_type))

    def add_geo_latlong_data(self, lat, lon):
        """Add a user provided EPSG:4326 WGS84 lat long pair to each frame

        We expect these values to be floats

        Args:
            lat (float): lattitude of Geo Location
            lon (float): longitude of Geo Location
        """
        if not (isinstance(lat, float) and isinstance(lon, float)):
            raise Exception(
                f"Lattitude ({lat}) and Longitude ({lon}) must both be floats."
            )

        self.geo_data["geo_EPSG4326_lat"] = lat
        self.geo_data["geo_EPSG4326_lon"] = lon

    def add_point_cloud_pcd(
        self, *, sensor_id, pcd_url, coord_frame_id=None, date_captured=None
    ):
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "pcd_url": pcd_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            if coord_frame_id == "world":
                self._add_coordinate_frame(
                    {
                        "coordinate_frame_id": coord_frame_id,
                        "coordinate_frame_type": "WORLD",
                    }
                )
            else:
                raise exception(
                    "Coordinate frame {} does not exist.".format(coord_frame_id)
                )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "POINTCLOUD_PCD_V0",
            }
        )

    def add_point_cloud_bins(
        self,
        *,
        sensor_id,
        pointcloud_url,
        intensity_url,
        range_url,
        coord_frame_id=None,
        date_captured=None,
    ):
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "pointcloud_url": pointcloud_url,
            "range_url": range_url,
            "intensity_url": intensity_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            if coord_frame_id == "world":
                self._add_coordinate_frame(
                    {
                        "coordinate_frame_id": coord_frame_id,
                        "coordinate_frame_type": "WORLD",
                    }
                )
            else:
                raise exception(
                    "Coordinate frame {} does not exist.".format(coord_frame_id)
                )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "POINTCLOUD_V0",
            }
        )

    def add_obj(
        self,
        *,
        sensor_id,
        obj_url,
        coord_frame_id=None,
        date_captured=None,
    ):
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        if coord_frame_id is None:
            coord_frame_id = "world"

        data_urls = {
            "obj_url": obj_url,
        }

        if not self._coord_frame_exists(coord_frame_id):
            self._add_coordinate_frame(
                {
                    "coordinate_frame_id": coord_frame_id,
                    "coordinate_frame_type": "WORLD",
                }
            )

        self.sensor_data.append(
            {
                "coordinate_frame": coord_frame_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "OBJ_V0",
            }
        )

    def add_image(
        self,
        *,
        sensor_id,
        image_url,
        preview_url=None,
        date_captured=None,
        width=None,
        height=None,
    ):
        """Add an image "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            image_url (str): The URL to load this image data.
            preview_url (str, optional): A URL to a compressed version of the image. It must be the same pixel dimensions as the original image. Defaults to None.
            date_captured (str, optional): ISO formatted date. Defaults to None.
            width (int, optional): The width of the image in pixels.
            height (int, optional): The height of the image in pixels.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        sensor_metadata = {}
        if width is not None:
            if not isinstance(width, int):
                raise Exception("width must be an int")
            sensor_metadata["width"] = width

        if height is not None:
            if not isinstance(height, int):
                raise Exception("height must be an int")
            sensor_metadata["height"] = height

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"image_url": image_url}
        if preview_url is not None:
            data_urls["preview_url"] = preview_url

        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "IMAGE"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": sensor_metadata,
                "sensor_type": "IMAGE_V0",
            }
        )

    def add_audio(
        self,
        *,
        sensor_id,
        audio_url,
        date_captured=None,
    ):
        """Add an audio "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            audio_url (str): The URL to load this audio data (mp3, etc.).
            date_captured (str, optional): ISO formatted date. Defaults to None.
        """
        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        sensor_metadata = {}
        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"audio_url": audio_url}

        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "AUDIO"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": sensor_metadata,
                "sensor_type": "AUDIO_V0",
            }
        )

    def add_coordinate_frame_3d(
        self, *, coord_frame_id, position=None, orientation=None, parent_frame_id=None
    ):
        """Add a 3D Coordinate Frame.

        Args:
            coord_frame_id (str): String identifier for this coordinate frame
            position (dict, optional): Dict of the form {x, y, z}. Defaults to None.
            orientation (dict, optional): Quaternion rotation dict of the form {w, x, y, z}. Defaults to None.
            parent_frame_id (str, optional): String id of the parent coordinate frame. Defaults to None.
        """

        if not isinstance(coord_frame_id, str):
            raise Exception("coord_frame_id must be a string")

        if coord_frame_id == "world":
            raise Exception("coord_frame_id cannot be world")

        if self._coord_frame_exists(coord_frame_id):
            raise Exception("Coordinate frame already exists.")

        # If world doesn't exist, make the world coordinate frame
        if not self._coord_frame_exists("world"):
            self._add_coordinate_frame(
                {
                    "coordinate_frame_id": "world",
                    "coordinate_frame_type": "WORLD",
                }
            )

        if position is None:
            position = {"x": 0, "y": 0, "z": 0}

        if orientation is None:
            orientation = {"w": 1, "x": 0, "y": 0, "z": 0}

        if parent_frame_id is None:
            parent_frame_id = "world"

        metadata = {
            "position": position,
            "orientation": orientation,
            "parent_frame_id": parent_frame_id,
        }

        self._add_coordinate_frame(
            {
                "coordinate_frame_id": coord_frame_id,
                "coordinate_frame_type": "WORLD",
                "coordinate_frame_metadata": json.dumps(metadata),
            }
        )

    def add_text(self, *, sensor_id, text, date_captured=None):
        """Add a text "sensor" data to this frame.

        Args:
            sensor_id (str): The id of this sensor.
            text (str): The text body.
            date_captured (str, optional): ISO formatted date. Defaults to None.
        """

        if not isinstance(sensor_id, str):
            raise Exception("sensor ids must be strings")

        if date_captured is None:
            date_captured = str(datetime.datetime.now())

        data_urls = {"text": text}
        self._add_coordinate_frame(
            {"coordinate_frame_id": sensor_id, "coordinate_frame_type": "TEXT"}
        )
        self.sensor_data.append(
            {
                "coordinate_frame": sensor_id,
                "data_urls": data_urls,
                "date_captured": date_captured,
                "sensor_id": sensor_id,
                "sensor_metadata": {},
                "sensor_type": "TEXT",
            }
        )

    def to_dict(self):
        """Convert this frame into a dictionary representation.

        Returns:
            dict: dictified frame
        """
        row = {
            "task_id": self.frame_id,
            "date_captured": self.date_captured,
            "device_id": self.device_id,
            "coordinate_frames": self.coordinate_frames,
            "sensor_data": self.sensor_data,
            "label_data": self.label_data,
            "geo_data": self.geo_data,
        }
        user_metadata_types = {}

        for k, v, vt in self.user_metadata:
            namespaced = k
            if "user__" not in namespaced:
                namespaced = "user__" + namespaced
            row[namespaced] = v
            user_metadata_types[namespaced] = vt

        row["user_metadata_types"] = user_metadata_types
        return row


class Inferences:
    """A container used to construct a set of inferences.

    Typical usage is to create an Inferences object, add multiple InferencesFrames to it,
    then serialize the frames to be submitted.
    """

    def __init__(self):
        if not _is_one_gb_available():
            raise OSError(
                "Attempting to run with less than 1 GB of available disk space. Exiting..."
            )
        self._frames = []
        self._frame_ids_set = set()
        current_time = datetime.datetime.now()
        self._temp_frame_prefix = "al_{}_inference_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_inference_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []

    def _save_rows_to_temp(self, file_name_prefix, writefunc, mode="w"):
        """[summary]

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush inferences to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=TEMP_FILE_PATH
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def _flush_to_disk(self):
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if len(self._frames) == 0:
            return
        frame_path = self._save_rows_to_temp(
            self._temp_frame_prefix, lambda x: self.write_to_file(x)
        )
        if frame_path:
            self._temp_frame_file_names.append(frame_path)
        embeddings_path = self._save_rows_to_temp(
            self._temp_frame_embeddings_prefix,
            lambda x: self.write_embeddings_to_file(x),
            mode="wb",
        )
        if embeddings_path:
            self._temp_frame_embeddings_file_names.append(embeddings_path)
        self._frames = []

    def add_frame(self, frame):
        """Add an InferencesFrame to this dataset.

        Args:
            frame (InferencesFrame): An InferencesFrame in this dataset.
        """
        if not isinstance(frame, InferencesFrame):
            raise Exception("Frame is not an InferencesFrame")

        if frame.frame_id in self._frame_ids_set:
            raise Exception("Attempted to add duplicate frame id.")

        self._frames.append(frame)
        self._frame_ids_set.add(frame.frame_id)
        if len(self._frames) >= MAX_FRAMES_PER_BATCH:
            self._flush_to_disk()

    def write_to_file(self, filelike):
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        for frame in self._frames:
            row = frame.to_dict()
            filelike.write(json.dumps(row) + "\n")

    def write_embeddings_to_file(self, filelike):
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # Get the first frame embedding dimension
        frame_embedding_dim = len(self._frames[0].embedding["embedding"])
        # Get the first crop embedding dimension
        crop_embedding_dim = 1
        for frame in self._frames:
            if frame.embedding["crop_embeddings"]:
                first_crop_emb = frame.embedding["crop_embeddings"][0]
                crop_embedding_dim = len(first_crop_emb["embedding"])
                break

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_ids[i] = frame.embedding["task_id"]
            frame_embeddings[i] = frame.embedding["embedding"]
            crop_ids[i] = [x["uuid"] for x in frame.embedding["crop_embeddings"]]
            crop_embeddings[i] = [
                x["embedding"] for x in frame.embedding["crop_embeddings"]
            ]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()


class InferencesFrame:
    """A frame containing inferences from an experiment.

    Args:
        frame_id (str): A unique id for this frame.
    """

    def __init__(self, *, frame_id=None):
        if not isinstance(frame_id, str):
            raise Exception("frame ids must be strings")

        if "/" in frame_id:
            raise Exception("frame ids cannot contain slashes (/)")

        self.frame_id = frame_id
        self.inference_data = []
        self.embedding = None
        self.custom_metrics = {}

    def add_embedding(self, *, embedding, crop_embeddings=None, model_id=""):
        """Add an embedding to this frame, and optionally to crops/labels within it.

        If provided, "crop_embeddings" is a list of dicts of the form:
            'uuid': the label id for the crop/label
            'embedding': a vector of floats between length 0 and 12,000.

        Args:
            embedding (list of floats): A vector of floats between length 0 and 12,000.
            crop_embeddings (list of dicts, optional): A list of dictionaries representing crop embeddings. Defaults to None.
            model_id (str, optional): The model id used to generate these embeddings. Defaults to "".
        """

        if crop_embeddings is None:
            crop_embeddings = []

        if not embedding or len(embedding) > 12000:
            raise Exception("Length of embeddings should be between 0 and 12,000")

        self.embedding = {
            "image_url": "",
            "task_id": self.frame_id,
            "crop_embeddings": crop_embeddings,
            "model_id": model_id,
            "date_generated": str(datetime.datetime.now()),
            "embedding": embedding,
        }

    def add_custom_metric(self, name, value):
        if not (isinstance(value, float) or isinstance(value, list)):
            raise Exception(
                "Custom metrics values must be either a float, or a 2D list of floats/integers."
            )

        self.custom_metrics[name] = value

    def add_inference_2d_bbox(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        top,
        left,
        width,
        height,
        confidence,
        area=None,
        iscrowd=None,
    ):
        """Add an inference for a 2D bounding box.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            area (float, optional): The area of the image.
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "confidence": confidence,
        }
        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd
        # TODO: This is mostly legacy for vergesense
        if area is not None:
            attrs["area"] = area

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "BBOX_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_inference_text_token(
        self, *, sensor_id, label_id, index, token, classification, visible, confidence
    ):
        """Add a label for a text token.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            index (int): the index of this token in the text
            token (str): the text content of this token
            classification (str): the classification string
            visible (bool): is this a visible token in the text
            confidence (float): confidence of prediction

        """
        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {
            "index": index,
            "token": token,
            "visible": visible,
            "confidence": confidence,
        }
        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "TEXT_TOKEN",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_inference_3d_cuboid(
        self,
        *,
        label_id,
        classification,
        position,
        dimensions,
        rotation,
        confidence,
        iscrowd=None,
        user_attrs=None,
        links=None,
        coord_frame_id=None,
    ):
        """Add an inference for a 3D cuboid.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            position (list of float): the position of the center of the cuboid
            dimensions (list of float): the dimensions of the cuboid
            rotation (list of float): the local rotation of the cuboid, represented as an xyzw quaternion.
            confidence (float): confidence of prediction
            iscrowd (bool, optional): Is this label marked as a crowd. Defaults to None.
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
            links (dict, optional): Links between labels. Defaults to None.
            coord_frame_id (str, optional): Coordinate frame id. Defaults to 'world'
        """
        if coord_frame_id is None:
            coord_frame_id = "world"

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")
        attrs = {
            "pos_x": position[0],
            "pos_y": position[1],
            "pos_z": position[2],
            "dim_x": dimensions[0],
            "dim_y": dimensions[1],
            "dim_z": dimensions[2],
            "rot_x": rotation[0],
            "rot_y": rotation[1],
            "rot_z": rotation[2],
            "rot_w": rotation[3],
            "confidence": confidence,
        }

        if iscrowd is not None:
            attrs["iscrowd"] = iscrowd

        if user_attrs is not None:
            for k, v in user_attrs.items():
                if "user__" not in k:
                    k = "user__" + k
                attrs[k] = v

        if links is not None:
            for k, v in links.items():
                if "link__" not in k:
                    k = "link__" + k
                attrs[k] = v

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CUBOID_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": attrs,
            }
        )

    def add_inference_2d_keypoints(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        top,
        left,
        width,
        height,
        keypoints,
        confidence,
        user_attrs=None,
    ):
        """Add an inference for a 2D keypoints task.

        A keypoint is a dictionary of the form:
            'x': x-coordinate in pixels
            'y': y-coordinate in pixels
            'name': string name of the keypoint

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            top (int or float): The top of the box in pixels
            left (int or float): The left of the box in pixels
            width (int or float): The width of the box in pixels
            height (int or float): The height of the box in pixels
            keypoints (list of dicts): The keypoints of this detection
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            user_attrs (dict, optional): Any additional label-level metadata fields. Defaults to None.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
            "keypoints": keypoints,
            "confidence": confidence,
        }

        if user_attrs is not None:
            for k, v in user_attrs.items():
                if "user__" not in k:
                    k = "user__" + k
                attrs[k] = v

        self.label_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "KEYPOINTS_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_inference_2d_polygon_list(
        self,
        *,
        sensor_id,
        label_id,
        classification,
        polygons,
        confidence,
        center=None,
    ):
        """Add an inference for a 2D polygon list instance segmentation task.

        Polygons are dictionaries of the form:
            'vertices': list of (x, y)

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            polygons (list of dicts): The polygon geometry
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            center (list of ints or floats, optional): The center point of the instance
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        attrs = {"polygons": polygons, "center": center, "confidence": confidence}

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "POLYGON_LIST_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": attrs,
            }
        )

    def add_inference_2d_semseg(self, *, sensor_id, label_id, mask_url):
        """Add an inference for 2D semseg.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            mask_url (str): URL to the pixel mask png.
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label": "__mask",
                "label_coordinate_frame": sensor_id,
                "label_type": "SEMANTIC_LABEL_URL_2D",
                "attributes": {"url": mask_url},
            }
        )

    def add_inference_2d_classification(
        self, *, sensor_id, label_id, classification, confidence
    ):
        """Add an inference for 2D classification.

        Args:
            sensor_id (str): sensor_id
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
        """

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_2D",
                "label": classification,
                "label_coordinate_frame": sensor_id,
                "attributes": {"confidence": confidence},
            }
        )

    def add_inference_3d_classification(
        self,
        *,
        label_id,
        classification,
        confidence,
        coord_frame_id=None,
    ):
        """Add a label for 3D classification.

        Args:
            label_id (str): label_id which is unique across datasets and inferences.
            classification (str): the classification string
            confidence (float): The confidence between 0.0 and 1.0 of the prediction
            coord_frame_id (optional, str): The coordinate frame id.
        """

        if coord_frame_id is None:
            coord_frame_id = "world"

        if not isinstance(label_id, str):
            raise Exception("label ids must be strings")
        if "/" in label_id:
            raise Exception("label ids cannot contain slashes (/)")

        if not isinstance(classification, str):
            raise Exception("classifications must be strings")

        self.inference_data.append(
            {
                "uuid": label_id,
                "linked_labels": [],
                "label_type": "CLASSIFICATION_3D",
                "label": classification,
                "label_coordinate_frame": coord_frame_id,
                "attributes": {"confidence": confidence},
            }
        )

    def to_dict(self):
        """Convert this frame into a dictionary representation.

        Returns:
            dict: dictified frame
        """
        row = {"task_id": self.frame_id, "inference_data": self.inference_data}
        row["custom_metrics"] = self.custom_metrics

        return row


# https://public.tableau.com/profile/chris.gerrard#!/vizhome/TableauColors/ColorPaletteswithRGBValues
tableau_colors = [
    (31, 119, 180),
    (255, 127, 14),
    (44, 160, 44),
    (214, 39, 40),
    (148, 103, 189),
    (140, 86, 75),
    (227, 119, 194),
    (127, 127, 127),
    (188, 189, 34),
    (23, 190, 207),
]

# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
orig_label_color_list = [
    (230, 25, 75),
    (60, 180, 75),
    (255, 225, 25),
    (67, 99, 216),
    (245, 130, 49),
    (145, 30, 180),
    (70, 240, 240),
    (240, 50, 230),
    (188, 246, 12),
    (250, 190, 190),
    (0, 128, 128),
    (230, 190, 255),
    (154, 99, 36),
    (255, 250, 200),
    (128, 0, 0),
    (170, 255, 195),
    (128, 128, 0),
    (255, 216, 177),
    (0, 0, 117),
    (128, 128, 128),
]


class LabelClassMap:
    """A collection of ClassMapEntries that defines how to interpret classifications.

    Args:
        entries (list of ClassMapEntry, optional): List of classification entries. Defaults to None.

    """

    def from_classnames_max20(classnames):
        """A helper utility to generate a set of distinct colors given a list of classnames

        Args:
            classnames (list of str): List of up to twenty classifications as strings

        Returns:
            LabelClassMap: A LabelClassMap containing categorical colors for the provided classnames.
        """
        if len(classnames) > 20:
            raise Exception("More than 20 classnames were provided.")

        classmap = LabelClassMap()
        for idx, classname in enumerate(classnames):
            entry = ClassMapEntry(
                class_id=idx,
                name=classname,
                color=orig_label_color_list[idx % len(orig_label_color_list)],
            )
            classmap.add_entry(entry)

        return classmap

    def from_classnames_max10(classnames):
        """A helper utility to generate a set of distinct colors given a list of classnames

        Args:
            classnames (list of str): List of up to ten classifications as strings

        Returns:
            LabelClassMap: A LabelClassMap containing categorical colors for the provided classnames.
        """
        if len(classnames) > 10:
            raise Exception("More than 10 classnames were provided.")

        classmap = LabelClassMap()
        for idx, classname in enumerate(classnames):
            entry = ClassMapEntry(
                class_id=idx,
                name=classname,
                color=tableau_colors[idx % len(tableau_colors)],
            )
            classmap.add_entry(entry)

        return classmap

    def from_classnames_turbo(classnames):
        """A helper utility to generate a set of distinct colors given a list of classnames.

        These colors are pulled from the turbo color scheme, and will be assigned
        in order from dark to light.

        Args:
            classnames (list of str): List of classifications as strings.

        Returns:
            LabelClassMap: A LabelClassMap containing colors for the provided classnames.
        """
        classmap = LabelClassMap()
        for idx, classname in enumerate(classnames):
            col_step = floor(len(turbo_rgb) / len(classnames))
            col_idx = col_step * idx
            color = turbo_rgb[col_idx]

            entry = ClassMapEntry(class_id=idx, name=classname, color=color)
            classmap.add_entry(entry)

        return classmap

    def from_classnames_viridis(classnames):
        """A helper utility to generate a set of distinct colors given a list of classnames.

        These colors are pulled from the viridis color scheme, and will be assigned
        in order from dark to light.

        Args:
            classnames (list of str): List of classifications as strings.

        Returns:
            LabelClassMap: A LabelClassMap containing colors for the provided classnames.
        """
        classmap = LabelClassMap()
        for idx, classname in enumerate(classnames):
            col_step = floor(len(viridis_rgb) / len(classnames))
            col_idx = col_step * idx
            color = viridis_rgb[col_idx]

            entry = ClassMapEntry(class_id=idx, name=classname, color=color)
            classmap.add_entry(entry)

        return classmap

    def __init__(self, *, entries=None):
        self.entries = []
        self._name_set = set()
        self._class_id_set = set()

        if entries is not None:
            for entry in entries:
                self.add_entry(entry)

    def add_entry(self, entry):
        """Add a ClassMapEntry.

        Args:
            entry (ClassMapEntry): entry
        """
        if not isinstance(entry, ClassMapEntry):
            raise Exception("entry must be a ClassMapEntry")

        if entry.class_id in self._class_id_set:
            raise Exception(f"An entry with class id {entry.class_id} already exists.")
        if entry.name in self._name_set:
            raise Exception(f"An entry with name {entry.name} already exists.")

        self._class_id_set.add(entry.class_id)
        self._name_set.add(entry.name)

        self.entries.append(entry)


class ClassMapEntry:
    """A description of how to interpret a classification.

    In the common case, only three values are needed:
    - The string representation of the class
    - The int [0,255] representation of the class
    - What color to render it as.

    In more complex cases, some classes may be ignored in evaluation,
    or collapsed together into a different class at inference time,
    or tracked as part of a larger category.

    Args:
        name (str): The string representation of the class
        class_id (int): The int representation of the class
        color (list of ints): A length 3 list/tuple of RGB int values
        train_name (str, optional): The string representation of the class that this label will be inferred as. Defaults to None.
        train_id (int, optional): The int representation of the class that this label will be infererred as. Defaults to None.
        category (str, optional): The string representation of the parent category. Defaults to None.
        category_id (int, optional): The int representation of the parent category. Defaults to None.
        has_instances (bool, optional): Whether each label of this class is a separate instance. Defaults to True.
        ignore_in_eval (bool, optional): Whether to ignore this class while evaluating metrics. Defaults to False.
        train_color ([type], optional): A length 3 list/tuple of RGB int values for showing inferences of this class. Defaults to None.
    """

    def __init__(
        self,
        *,
        name,
        class_id,
        color,
        train_name=None,
        train_id=None,
        category=None,
        category_id=None,
        has_instances=True,
        ignore_in_eval=False,
        train_color=None,
    ):

        # Set defaults for more complex class mapping fields if not set
        if train_name is None:
            train_name = name
        if train_id is None:
            train_id = class_id
        if category is None:
            category = name
        if category_id is None:
            category_id = class_id
        if train_color is None:
            train_color = color

        # Assert on types
        # Names
        if type(name) is not str:
            raise Exception("Argument 'name' must be a string.")
        if type(train_name) is not str:
            raise Exception("Argument 'train_name' must be a string.")
        if type(category) is not str:
            raise Exception("Argument 'category' must be a string.")

        # Class IDs
        if type(class_id) is not int:
            raise Exception("Argument 'class_id' must be an int.")
        if type(train_id) is not int:
            raise Exception("Argument 'train_id' must be an int.")
        if type(category_id) is not int:
            raise Exception("Argument 'category_id' must be an int.")
        if class_id < 0:
            raise Exception("Argument 'class_id' cannot have negative values.")
        if train_id < 0:
            raise Exception("Argument 'train_id' cannot have negative values.")
        if category_id < 0:
            raise Exception("Argument 'category_id' cannot have negative values.")

        # Colors
        if type(color) not in [list, tuple]:
            raise Exception(
                "Argument 'color' must be a list or tuple of ints, in the range [0,255]."
            )
        if type(train_color) not in [list, tuple]:
            raise Exception(
                "Argument 'train_color' must be a list or tuple of ints, in the range [0,255]."
            )
        if len(color) != 3:
            raise Exception("Argument 'color' must have a length of 3.")
        if len(train_color) != 3:
            raise Exception("Argument 'train_color' must have a length of 3.")
        for val in color:
            if (type(val) is not int) or val < 0 or val > 255:
                raise Exception(
                    "Argument 'color' must have integer entries in the range [0,255]."
                )
        for val in train_color:
            if (type(val) is not int) or val < 0 or val > 255:
                raise Exception(
                    "Argument 'train_color' must have integer entries in the range [0,255]."
                )

        self.name = name
        self.class_id = class_id
        self.train_name = train_name
        self.train_id = train_id
        self.category = category
        self.category_id = category_id
        self.has_instances = has_instances
        self.ignore_in_eval = ignore_in_eval
        self.color = list(color)
        self.train_color = list(train_color)

    def to_dict(self):
        """Returns a dictified form of this data structure."""
        return {
            "name": self.name,
            "id": self.class_id,
            "train_name": self.train_name,
            "train_id": self.train_id,
            "category": self.category,
            "category_id": self.category_id,
            "has_instances": self.has_instances,
            "ignore_in_eval": self.ignore_in_eval,
            "color": self.color,
            "train_color": self.train_color,
        }
