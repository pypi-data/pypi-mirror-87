try:
    from importlib.metadata import version as _version, PackageNotFoundError

    def version(dep: str):
        try:
            return _version(dep)
        except PackageNotFoundError:
            return None
except ImportError:
    from pkg_resources import get_distribution, DistributionNotFound

    def version(dep: str):
        try:
            return get_distribution(dep).version
        except DistributionNotFound:
            return None

APP_NAME_SHORT = "sett"
APP_NAME_LONG = "Secure Encryption and Transfer Tool"
URL_READTHEDOCS = "https://sett.readthedocs.io"
URL_GITLAB = "https://gitlab.com/biomedit/sett"
URL_GITLAB_ISSUES = URL_GITLAB + '/-/issues'

__project_name__ = "sett"
__version__ = version(__project_name__) or "0.0.0.dev"


def dep_version(dep: str) -> str:
    return version(dep) or "not_found"


VERSION_WITH_DEPS = f"{APP_NAME_SHORT} {__version__} (" + \
                    ", ".join(f"{n} {dep_version(n)}"
                              for n in ("gpg-lite", "libbiomedit")) + \
                    ")"
