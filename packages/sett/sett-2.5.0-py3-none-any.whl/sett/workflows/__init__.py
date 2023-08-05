import platform
from logging import Logger
from functools import wraps
from typing import Tuple, Type, Union

from .. import VERSION_WITH_DEPS
from ..utils.log import exception_to_message


def workflow(logger: Logger,
             error_types: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = ()):
    """A function decorator that should be used by every workflow.

    At the beggining of the workflow the decorator logs:
    - application version
    - versions of the main dependencies
    - version of the operating system where the application is running

    The function is wrapped in turn with the `exception_to_message`
    decorator.
    """
    def dec(f):
        _f = exception_to_message(error_types=error_types, logger=logger)(f)

        @wraps(f)
        def wrapped_f(*args, **kwargs):
            logger.info(
                f"{VERSION_WITH_DEPS} (platform: {platform.platform()})")
            return _f(*args, **kwargs)
        return wrapped_f
    return dec
