import sys
import platform
from functools import wraps
import logging
import logging.handlers
import warnings
from typing import Callable, Tuple, Dict, cast, Type, Union
from pathlib import Path


class LogTask:
    """Context manager that logs a user-defined message with level INFO upon
    entering the context manager, and either "OK" or "FAILED" upon exiting
    depending on whether exceptions occurred during its body or not.

    : param message: message to log with INFO level when entering the
        context manager.
    : param ok_logger: method associated with the logger level at which the
        message string should be logged. E.g. logging.info will log the message
        at the INFO level.
    : param err_logger: same as above but for logger level associated with
        errors.
    """

    def __init__(self,
                 message: str,
                 ok_logger: Callable = logging.info,
                 err_logger: Callable = logging.error):
        self.ok_logger = ok_logger
        self.err_logger = err_logger
        self.message = message

    def __enter__(self):
        self.ok_logger(self.message)

    def __exit__(self, exception_type, value, traceback):
        if exception_type is None:
            self.ok_logger("OK")
            return True
        self.err_logger("FAILED")
        return False


ExceptionType = Union[Type[BaseException], Tuple[Type[BaseException], ...]]


def exception_to_message(error_types: ExceptionType = (), logger=logging):
    """A function decorator catching the first exception of instance contained
    in or equal to error_types, occurring while executing the decorated
    function, logging an error and exiting python.
    """
    def dec(f):
        @wraps(f)
        def wrapped_f(*args, on_error=lambda _: sys.exit(1), **kwargs):
            try:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    r = f(*args, **kwargs)
                    for warning in w:
                        logger.warning(format(warning.message))
                    return r
            except error_types as e:
                logger.error(format(e))
                on_error(e)
        return wrapped_f
    return dec


class LoggerExt(logging.Logger):
    """Logger class with additional functionality"""

    def log_task(self, message: str) -> LogTask:
        """A context manager to log a task which can potentially fail"""
        return LogTask(message,
                       ok_logger=self.info,
                       err_logger=self.error)


logging.setLoggerClass(LoggerExt)


def create_logger(name, logger_level: int = logging.DEBUG) -> LoggerExt:
    """Instantiate and return a new logger object with the user selected name
     and logging level (e.g. DEBUG, INFO).

    :param name: name of logger.
    :param logger_level: level of logger. Any messages under the selected
        level will not be printed to screen and logfile.
    :return: logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logger_level)
    return cast(LoggerExt, logger)  # We called logging.setLoggerClass


def add_rotating_file_handler_to_logger(logger: logging.Logger,
                                        log_dir: str,
                                        logger_level: int = logging.DEBUG,
                                        file_max_number: int = 1000,
                                        file_max_size: int = 1000000) -> None:
    """Add a rotating file handler to the specified logger. When the logfile
    reaches file_max_size, it gets renamed (a number is appended) and a new
    logfile is started. When file_max_number is exceeded, the oldest backup
    file is deleted.

    :param logger: logger object to which the file handler should be added.
    :param log_dir: directory where to write the logfile.
    :param logger_level: level of logger (e.g. logging.DEBUG, logging.INFO).
        Messages under the selected level will be ignored by the handler.
    :param file_max_number: maximum number of logfiles to keep as backup.
    :param file_max_size: maximum size in bytes of an individual logfile.
    """
    # Create log directory if it does not exist yet.
    log_dir_path = Path(log_dir)
    if not log_dir_path.is_dir():
        try:
            log_dir_path.mkdir(parents=True)
        except PermissionError:
            logger.error(
                f'unable to create directory {log_dir_path.as_posix()}.')

    # Setup handler for logging info to file. The file logging format adds
    # the data and time at the start of each logged message.
    log_file = log_dir_path.joinpath('log')
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file.as_posix(),
        mode='a',
        maxBytes=file_max_size,
        backupCount=file_max_number - 1)
    file_handler.setFormatter(
        logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
    file_handler.setLevel(logger_level)
    logger.addHandler(file_handler)


def add_stream_handler_to_logger(logger: logging.Logger,
                                 logger_level: int = logging.INFO) -> None:
    """Add a stream handler to display logging info in console.

    :param logger: logger object to which the stream handler should be added.
    :param logger_level: level of logger (e.g. logging.DEBUG, logging.INFO).
        Messages under the selected level will be ignored by the handler.
    """
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('[%(levelname)s] %(message)s'))
    console_handler.setLevel(logger_level)
    logger.addHandler(console_handler)


def get_default_log_dir() -> str:
    """Returns a string with the default location of the directory where log
    files are stored on the host operating system.
    """
    default_log_dir_by_os: Dict[str, Tuple[str, ...]] = {'Linux': ('.local/var/log/sett',),
                                                         'Darwin': ('.local/var/log/sett',),
                                                         'Windows': ('AppData', 'Roaming', 'sett')}
    return Path.home().joinpath(
        *default_log_dir_by_os[platform.system()]).as_posix()
