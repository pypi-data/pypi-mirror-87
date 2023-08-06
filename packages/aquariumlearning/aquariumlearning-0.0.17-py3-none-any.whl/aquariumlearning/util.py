def raise_resp_exception_error(resp):
    if not resp.ok:
        message = None
        try:
            r_body = resp.json()
            message = r_body.get("message") or r_body.get("msg")
        except:
            # If we failed for whatever reason (parsing body, etc.)
            # Just return the code
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None

        if message:
            raise Exception("Error: {}".format(message))
        else:
            raise Exception(
                "HTTP Error received: {}".format(str(resp.status_code))
            ) from None


def determine_latest_version():
    from bs4 import BeautifulSoup
    from http import HTTPStatus
    import requests
    import re

    PACKAGE_REPO_URL = "https://aquarium-not-pypi.web.app/{}".format(__package__)
    SEM_VER_MATCHER = re.compile(f"{__package__}-(.*)\.tar\.gz")

    r = requests.get(PACKAGE_REPO_URL)
    if r.status_code == HTTPStatus.OK:
        # Python package repos have a standard layout:
        # https://packaging.python.org/guides/hosting-your-own-index/
        versions = BeautifulSoup(r.text, "html.parser").find_all("a")
        if len(versions) > 0:
            version_match = SEM_VER_MATCHER.match(versions[-1]["href"])
            if version_match != None:
                return version_match.group(1)
    return None


def check_if_update_needed():
    from importlib_metadata import version
    from termcolor import colored

    current_version = version(__package__)
    latest_version = determine_latest_version()

    if latest_version != None and current_version != latest_version:
        print(
            colored(
                f"aquariumlearning: Please upgrade from version {current_version} to latest version {latest_version}.",
                "yellow",
            )
        )
