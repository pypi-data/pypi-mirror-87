import logging
import sys
import traceback
from typing import Collection

from PySide2.QtCore import Signal, QObject, QRunnable


class LoggerHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, callback=None):
        super().__init__(level)
        self.callback = callback

    def emit(self, record):
        if self.callback:
            self.callback(self.format(record))

class WorkerSignals(QObject):
    started = Signal()
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    logging = Signal(str)


class Worker(QRunnable):
    """Worker can run an arbitrary function in a separate thread.

    :param fn: function to run in a thread
    :param args: arguments passed to the function
    :param kwargs: keyword arguments passed to the function
    :param logger: logs from those loggers are passed to the logging
                   signal
    """
    def __init__(self,
                 fn,
                 *args,
                 logger: Collection[logging.Logger] = (),
                 **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.logger = logger
        self.signals = WorkerSignals()  # progress signal is not implemented

    def run(self) -> None:
        try:
            logger_handler = LoggerHandler(callback=self.signals.logging.emit)
            logger_handler.setFormatter(
                logging.Formatter("[%(levelname)s] %(message)s"))
            logger_handler.setLevel(logging.INFO)
            for x in self.logger:
                x.addHandler(logger_handler)
            self.signals.started.emit()
            result = self.fn(*self.args, **self.kwargs)
        except Exception:  # pylint: disable=broad-except
            exctype, value, _ = sys.exc_info()
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            for x in self.logger:
                x.removeHandler(logger_handler)
            self.signals.finished.emit()
