import enum
import operator
from pathlib import Path

import time
from PySide2 import QtWidgets, QtCore

from .component import TabMixin, PathInput,\
    GuiProgress, run_dialog, MandatoryLabel
from .file_selection_widget import ArchiveOnlyFileSelectionWidget
from .parallel import Worker
from .. import protocols
from ..workflows import transfer


class TransferTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data
        self.app_data.transfer_protocol_args = {"sftp": {},
                                                "liquid_files": {}}

        files_panel = self.create_files_panel()
        options_panel = self.create_options_panel()
        self.create_run_panel("Transfer data", self.transfer,
                              "Transfer selected files")
        self.app_data.add_listener('transfer_files', self._enable_buttons)
        self.create_console()
        self.create_progress_bar()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(files_panel, 0, 0, 1, 2)
        layout.addWidget(options_panel, 1, 0, 1, 2)
        layout.addWidget(self.run_panel, 2, 0, 1, 2)
        layout.addWidget(self.console, 3, 0, 1, 2)
        layout.addWidget(self.progress_bar, 4, 0, 1, 2)
        self.setLayout(layout)

    def _enable_buttons(self):
        self.set_buttons_enabled(len(self.app_data.transfer_files) > 0)

    def create_files_panel(self):
        box = ArchiveOnlyFileSelectionWidget("Encrypted files to transfer", self)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "transfer_files", box.get_list()))
        return box

    def create_sftp_options_panel(self):
        field_mapping = FieldMapping()

        text_username = field_mapping.bind_text("username", QtWidgets.QLineEdit())
        text_username.setStatusTip("Username on the SFTP server")
        text_destination_dir = field_mapping.bind_text("destination_dir", QtWidgets.QLineEdit())
        text_username.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "username", text_username.text()))
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_host.setStatusTip("URL of the SFTP server with an optional port "
                               "number")
        text_host.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                            "host", text_host.text()))
        text_jumphost = field_mapping.bind_text("jumphost", QtWidgets.QLineEdit())
        text_jumphost.setStatusTip("(optional) URL of the jumphost server")
        text_jumphost.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "jumphost", text_jumphost.text() or None))
        text_destination_dir.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                            "destination_dir", text_destination_dir.text()))
        text_destination_dir.setStatusTip("Relative or absolute path to the "
                                          "destination directory on the SFTP "
                                          "server")
        pkey_location = field_mapping.bind_path("pkey", PathInput(directory=False, path=None))
        pkey_location.btn_label = "Select private key"
        pkey_location.status_tip = "Path to the private SSH key used for authentication"
        pkey_location.on_path_change(lambda path:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "pkey", "" if path is None else str(path)))
        pkey_password = field_mapping.bind_text("pkey_password", QtWidgets.QLineEdit())
        pkey_password.setStatusTip("Passphrase for the SSH private key")
        pkey_password.setEchoMode(QtWidgets.QLineEdit.Password)
        pkey_password.editingFinished.connect(lambda:
            operator.setitem(self.app_data.transfer_protocol_args["sftp"],
                             "pkey_password", pkey_password.text()))

        layout = QtWidgets.QGridLayout()
        layout.addWidget(MandatoryLabel("User name"), 0, 0)
        layout.addWidget(text_username, 0, 1)
        layout.addWidget(MandatoryLabel("Host URL"), 1, 0)
        layout.addWidget(text_host, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Jumphost URL"), 2, 0)
        layout.addWidget(text_jumphost, 2, 1)
        layout.addWidget(MandatoryLabel("Destination directory"), 3, 0)
        layout.addWidget(text_destination_dir, 3, 1)
        layout.addWidget(QtWidgets.QLabel("SSH key location"), 4, 0)
        layout.addWidget(pkey_location.text, 4, 1)
        layout.addWidget(pkey_location.btn, 4, 2)
        layout.addWidget(pkey_location.btn_clear, 4, 3)
        layout.addWidget(QtWidgets.QLabel("SSH key password"), 5, 0)
        layout.addWidget(pkey_password, 5, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_liquidfiles_options_panel(self):
        field_mapping = FieldMapping()
        text_host = field_mapping.bind_text("host", QtWidgets.QLineEdit())
        text_api_key = field_mapping.bind_text("api_key", QtWidgets.QLineEdit())
        text_host.editingFinished.connect(lambda: operator.setitem(
            self.app_data.transfer_protocol_args["liquid_files"], "host",
            text_host.text()))
        text_api_key.editingFinished.connect(lambda: operator.setitem(
            self.app_data.transfer_protocol_args["liquid_files"],
            "api_key", text_api_key.text()))
        layout = QtWidgets.QGridLayout()
        layout.addWidget(MandatoryLabel("Host URL"), 0, 0)
        layout.addWidget(text_host, 0, 1)
        layout.addWidget(MandatoryLabel("API Key"), 1, 0)
        layout.addWidget(text_api_key, 1, 1)
        box = QtWidgets.QGroupBox("Parameters")
        box.setFlat(True)
        box.setLayout(layout)
        box.load_connection = field_mapping.load
        return box

    def create_options_panel(self):
        box = QtWidgets.QGroupBox("Connection")

        verify_dtr = QtWidgets.QCheckBox("Verify DTR ID")
        verify_dtr.setStatusTip("Verify DTR (Data Transfer Request) ID")
        verify_dtr.setChecked(not self.app_data.config.offline and
                              self.app_data.transfer_verify_dtr)
        if self.app_data.config.offline:
            verify_dtr.setEnabled(not self.app_data.config.offline)
            verify_dtr.setStatusTip("Verifying Transfer Request ID in offline mode is not possible")
        verify_dtr.stateChanged.connect(lambda state:
            setattr(self.app_data, "transfer_verify_dtr",
                    state == QtCore.Qt.Checked))

        connections_selection = QtWidgets.QComboBox(box)
        connections_selection.setStatusTip(
            "Select a predefined connection profile. "
            "Check documentation for details.")
        connections_selection.addItems(list(self.app_data.config.connections))

        protocol_selection = QtWidgets.QComboBox(box)
        protocol_selection.setStatusTip("Select a protocol for the connection "
                                        "to the remote server")
        protocol_selection.addItems(["sftp", "liquid_files"])

        box_sftp = self.create_sftp_options_panel()
        box_liquidfiles = self.create_liquidfiles_options_panel()
        boxes = {"sftp": box_sftp, "liquid_files": box_liquidfiles}
        box_liquidfiles.hide()

        def load_connection():
            connection = self.app_data.config.connections.get(connections_selection.currentText())
            if not connection:
                return
            protocol_selection.setCurrentText(connection.protocol)
            box = boxes[connection.protocol]
            box.load_connection(connection.parameters)
            self.app_data.transfer_protocol_args[self.app_data.transfer_protocol_name].update(
                connection.parameters)

        connections_selection.currentIndexChanged.connect(load_connection)

        protocol_selection.currentTextChanged.connect(lambda text:
            (setattr(self.app_data, "transfer_protocol_name", text),
            box_sftp.setVisible(
                not box_sftp.isVisible()),
                box_liquidfiles.setVisible(not box_liquidfiles.isVisible())))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(verify_dtr)
        layout.addWidget(QtWidgets.QLabel("Predefined connections"))
        layout.addWidget(connections_selection)
        layout.addWidget(QtWidgets.QLabel("Protocol"))
        layout.addWidget(protocol_selection)
        layout.addWidget(box_sftp)
        layout.addWidget(box_liquidfiles)
        box.setLayout(layout)
        load_connection()
        return box

    def transfer(self, dry_run=False):
        progress = GuiProgress()
        progress.updated.connect(self.progress_bar.setValue)

        second_factor = None

        class Msg(enum.Enum):
            code = enum.auto()

        class MsgSignal(QtCore.QObject):
            msg = QtCore.Signal(object)

        msg_signal = MsgSignal()

        def second_factor_callback():
            msg_signal.msg.emit(Msg.code)
            time_start = time.time()
            timeout = 120
            while time.time() - time_start < timeout:
                time.sleep(1)
                if second_factor is not None:
                    break
            return second_factor

        def show_second_factor_dialog(msg: str):
            nonlocal second_factor
            second_factor = None
            if msg == Msg.code:
                output = run_dialog(self, "Verification code", password=False)
                second_factor = "" if output is None else output

        worker = Worker(
            transfer.transfer,
            files=self.app_data.transfer_files,
            logger=(transfer.logger, protocols.sftp.logger),
            protocol=protocols.protocols_by_name[
                self.app_data.transfer_protocol_name],
            protocol_args=self.app_data.transfer_protocol_args[
                self.app_data.transfer_protocol_name],
            config=self.app_data.config,
            dry_run=dry_run,
            verify_dtr=self.app_data.transfer_verify_dtr,
            progress=progress,
            on_error=lambda _: None,
            two_factor_callback=second_factor_callback)
        self.add_worker_actions(worker)
        msg_signal.msg.connect(show_second_factor_dialog)
        self.threadpool.start(worker)


class FieldMapping:
    def __init__(self):
        self._mapping = {}

    def bind_text(self, field_name, w):
        self._mapping[field_name] = w.setText
        return w

    def bind_path(self, field_name, w):
        self._mapping[field_name] = lambda p: w.update_path(Path(p))
        return w

    def load(self, parameters):
        for key, val in parameters.items():
            try:
                self._mapping[key](val)
            except KeyError:
                raise ValueError(f"Invalid field `{key}` found in your "
                                 "config file") from None
