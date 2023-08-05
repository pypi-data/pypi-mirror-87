import inspect

from . import liquid_files, sftp
from ..core.error import UserError


# TODO: change type to a tuple of items implementing a protocol
# (once protocol is standard in python)
protocols = (liquid_files, sftp)
protocols_by_name = {p.__name__.replace(
    __name__ + ".", ""): p.upload for p in protocols}  # type: ignore

__all__ = tuple(protocols_by_name)


def parse_protocol(s: str):
    try:
        return protocols_by_name[s]
    except KeyError:
        raise UserError(f"Invalid protocol: {s}") from None


def needs_argument(protocol, argument: str):
    args = inspect.signature(protocol)
    return argument in args.parameters
