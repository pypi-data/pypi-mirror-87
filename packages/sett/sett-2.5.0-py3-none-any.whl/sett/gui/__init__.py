#!/usr/bin/env python3
"""Secure Encryption and Transfer Tool."""

import sys
import logging
from PySide2.QtWidgets import QApplication

from . import main_window
from ..utils.log import add_rotating_file_handler_to_logger


def run():
    application = QApplication(sys.argv)
    window = main_window.MainWindow()
    logger = logging.getLogger()
    add_rotating_file_handler_to_logger(logger,
                log_dir=window.app_data.config.log_dir,
                file_max_number=window.app_data.config.log_max_file_number)
    window.show()
    return application.exec_()


if __name__ == "__main__":
    run()
