import warnings
import re
import urllib.error
from ..core.request import urlopen


from .. import __version__, __project_name__


def check_version(repo_url: str):
    latest = get_latest_version(repo_url)
    if not __version__.startswith("0.0.0.dev") and __version__ != latest and latest is not None:
        warnings.warn(
            f"Your version ({__version__}) is outdated. {latest} is available. Please upgrade!")


def get_latest_version(repo_url: str):
    try:
        url = repo_url + "/simple/" + __project_name__ + "/"
        with urlopen(url) as response:  # nosec
            versions = re.findall(__project_name__.encode() +
                                  b"-([0-9]*.[0-9]*.[0-9]*).tar.gz", response.read())
            version = max(tuple(map(int, v.split(b".")))
                          for v in versions)
            return ".".join(map(str, version))
    except urllib.error.URLError:
        warnings.warn(
            "Could not connect to pypi repository to query the latest version. "
            "You might have an outdated version. Please check yourself!")
    except IndexError:
        warnings.warn(
            "No releases found on the pypi repository! Please contact the developers!")
