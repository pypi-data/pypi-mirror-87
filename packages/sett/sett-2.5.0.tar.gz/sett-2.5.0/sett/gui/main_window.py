import warnings

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QSysInfo
from PySide2.QtGui import QKeySequence

from sett import APP_NAME_LONG, URL_READTHEDOCS, URL_GITLAB_ISSUES, \
    APP_NAME_SHORT, __version__, URL_GITLAB, VERSION_WITH_DEPS
from ..core.versioncheck import check_version
from .keys_tab import KeysTab
from .transfer_tab import TransferTab
from .decrypt_tab import DecryptTab
from .encrypt_tab import EncryptTab
from .model import AppData
from .parallel import Worker
from ..utils.config import load_config

QtCore.QThreadPool.globalInstance().setExpiryTimeout(-1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = f"{APP_NAME_LONG} ({__version__})"
        self.app_data = AppData(config=load_config())
        self.setWindowTitle(self.title)
        self.add_menu()
        self.add_tabs()
        self.add_status_bar()
        self.check_version()

    def add_tabs(self):
        tab_keys = KeysTab(self)  # FIXME created first to populate gpg keys
        tab_encrypt = EncryptTab(self)
        tab_decrypt = DecryptTab(self)
        tab_transfer = TransferTab(self)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(tab_encrypt, "&Encrypt")
        tabs.addTab(tab_transfer, "&Transfer")
        tabs.addTab(tab_decrypt, "&Decrypt")
        tabs.addTab(tab_keys, "&Keys")

        self.setCentralWidget(tabs)

    def add_status_bar(self):
        self.status = QtWidgets.QStatusBar()
        self.setStatusBar(self.status)

    def add_menu(self):
        action_exit = QtWidgets.QAction(QtGui.QIcon(), '&Exit', self)
        action_exit.setShortcut(QKeySequence('Ctrl+Q'))
        action_exit.setStatusTip('Exit application')
        action_exit.triggered.connect(self.close)

        menu = self.menuBar()
        menu.setNativeMenuBar(QSysInfo.productType() != 'osx')
        menu_file = menu.addMenu("&File")
        menu_file.addAction(action_exit)

        action_help = QtWidgets.QAction(QtGui.QIcon(), "&Documentation", self)
        action_help.setStatusTip('Open online documentation')
        action_help.setShortcut(QKeySequence(QKeySequence.HelpContents))
        action_help.triggered.connect(open_url(URL_READTHEDOCS))

        action_bug_report = QtWidgets.QAction(QtGui.QIcon(),
                                              "&Report an Issue", self)
        action_bug_report.setStatusTip('Open online bug report form')
        action_bug_report.triggered.connect(open_url(URL_GITLAB_ISSUES))

        action_about = QtWidgets.QAction(QtGui.QIcon(), "&About", self)
        action_about.setStatusTip("Show info about application")
        action_about.triggered.connect(self.show_about)

        menu_help = menu.addMenu("&Help")
        menu_help.addAction(action_help)
        menu_help.addAction(action_bug_report)
        menu_help.addAction(action_about)

    def closeEvent(self, event):
        if self.app_data.config.gui_quit_confirmation:
            reply = QtWidgets.QMessageBox.question(
                self, "Quit", "Do you really want to quit?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def check_version(self):
        if self.app_data.config.offline or not self.app_data.config.check_version:
            return

        def get_warnings():
            with warnings.catch_warnings(record=True) as w:
                check_version(self.app_data.config.repo_url)
                return "\n".join(format(warning.message) for warning in w)

        def show_msg(text):
            msg = QtWidgets.QMessageBox(parent=self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle(f"{self.title}")
            msg.setText(text)
            msg.show()

        worker = Worker(get_warnings)
        worker.signals.result.connect(lambda x: x and show_msg(x))
        QtCore.QThreadPool.globalInstance().start(worker)

    def show_about(self):
        msg = QtWidgets.QMessageBox(parent=self)
        msg.setWindowTitle(f"About {APP_NAME_SHORT}")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setText(
            f"{APP_NAME_LONG}<br>"
            f"{VERSION_WITH_DEPS}<br><br>"
            f"For documentation go to "
            f"<a href='{URL_READTHEDOCS}'>{URL_READTHEDOCS}</a><br>"
            f"To report an issue go to "
            f"<a href='{URL_GITLAB_ISSUES}'>{URL_GITLAB_ISSUES}</a><br>"
            f"Source code is available at "
            f"<a href='{URL_GITLAB}'>{URL_GITLAB}</a><br><br>"
            f"{APP_NAME_SHORT} is developed as part of the "
            f"<a href='https://sphn.ch/network/projects/biomedit/'>BioMedIT "
            f"project</a>")
        msg.show()


def open_url(url: str):
    """Retruns a function that will opens the specified URL in the user's
    default browser when called. The function that is returned has no
    arguments.
    :param url: URL to open.
    :returns: function that opens specifed URL.
    """

    def open_url_template():
        if not QtGui.QDesktopServices.openUrl(QtCore.QUrl(url)):
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText(f"Unable to open URL at \n{url}.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            msg_warn.exec_()

    return open_url_template
