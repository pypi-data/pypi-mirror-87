import html
from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from sett.core.error import UserError
from .component import SelectionButton
from .parallel import Worker
from ..core import crypt
from ..workflows import (upload_keys as upload_keys_workflow,
                         request_sigs as request_sigs_workflow)

Key = crypt.gpg.Key

def raise_(e: Exception):
    raise e


class KeysTab(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.app_data = self.parent().app_data
        self.update_private_keys()
        self.update_public_keys()

        self.text_panel = QtWidgets.QTextEdit()
        self.text_panel.setReadOnly(True)

        self.priv_keys_view = QtWidgets.QListView()
        self.priv_keys_view.setModel(self.app_data.priv_keys_model)
        self.priv_keys_view.selectionModel().currentChanged.connect(
            self._update_display)

        self.pub_keys_view = QtWidgets.QListView()
        self.pub_keys_view.setModel(self.app_data.pub_keys_model)
        self.pub_keys_view.selectionModel().currentChanged.connect(
            self._update_display)
        self.pub_keys_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

        # When item is selected clear selection in the other list
        self.priv_keys_view.selectionModel().currentChanged.connect(
            lambda: self.pub_keys_view.selectionModel().clear())
        self.pub_keys_view.selectionModel().currentChanged.connect(
            lambda: self.priv_keys_view.selectionModel().clear())

        btn_generate = QtWidgets.QPushButton("Generate new private/public key")
        btn_generate.clicked.connect(
            lambda: KeyGenDialog(parent=self).show())
        btn_group_public = self.create_public_keys_btn_group()
        btn_refresh = QtWidgets.QPushButton("Refresh keys")
        btn_refresh.setStatusTip("Refresh keys from the local keyring")
        btn_refresh.clicked.connect(
            lambda x: (self.update_private_keys(),
                       self.update_public_keys(),
                       self._update_display(
                           self.pub_keys_view.selectionModel().currentIndex()))
        )

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Private keys"), 0, 0)
        layout.addWidget(self.priv_keys_view, 1, 0)
        layout.addWidget(btn_generate, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Public keys"), 2, 0)
        layout.addWidget(self.pub_keys_view, 3, 0)
        layout.addLayout(btn_group_public, 3, 1)
        layout.addWidget(self.text_panel, 4, 0)
        layout.addWidget(btn_refresh, 4, 1)
        layout.setRowStretch(3, 1)
        layout.setRowStretch(4, 1)
        self.setLayout(layout)

    def key_to_html(self, key: Key) -> str:
        content = []
        content.append("<table>")
        rows = [("User ID", html.escape(str(key.uids[0]))),
                ("Key ID", key.key_id),
                ("Key fingerprint", key.fingerprint),
                ("Key length", key.key_length)]
        for k, v in rows:
            content.append(f"<tr><th>{k}</th><td>{v}</td></tr>")

        content.append("<tr><th>Signatures</th><td>")
        content.append("<br>".join(
            [f"{html.escape(str(sig.issuer_uid))} {sig.issuer_key_id} {sig.signature_class}"
             for sig in key.valid_signatures]))
        content.append("</td></tr>")

        content.append("</table>")
        if key.key_type == crypt.gpg.KeyType.public:
            try:
                crypt.validate_pub_key(
                    key,
                    validation_keyid=self.app_data.config.key_validation_authority_keyid,
                    keyserver_url=self.app_data.config.keyserver_url)
                content.append(
                    "<p class=\"safe\">This key has been verified</p>")
            except UserError as e:
                content.append(
                    f"<p class=\"danger\">{e}</p>")
        else:
            content.append(
                "<p>This is a private key. "
                "Private keys can not be signed.</p>")
        return "".join(content)

    @staticmethod
    def key_to_text(key: Key) -> str:
        return (f"User ID: {key.uids[0]}\n"
                f"Fingerprint: {key.fingerprint}")

    def create_public_keys_btn_group(self):
        selection_model = self.pub_keys_view.selectionModel()
        btn_download = QtWidgets.QPushButton("Download keys")
        btn_download.setStatusTip(
            "Search and download keys from the keyserver")
        btn_download.clicked.connect(
            lambda: KeyDownloadDialog(parent=self).show())
        btn_update = SelectionButton("Update keys", selection_model)
        btn_update.setStatusTip("Update selected key from the keyserver")
        btn_update.clicked.connect(self.update_keys)
        btn_import = QtWidgets.QPushButton("Import key")
        btn_import.setStatusTip("Import key from file")
        btn_import.clicked.connect(self.import_key)
        btn_upload = SelectionButton("Upload keys", selection_model)
        btn_upload.setStatusTip("Upload selected key to the keyserver")
        btn_upload.clicked.connect(self.upload_key)
        btn_sign = SelectionButton("Request signature", selection_model)
        btn_sign.setStatusTip("Request signature for the selected keys")
        btn_sign.clicked.connect(self.request_signature)
        btn_delete = SelectionButton("Delete keys", selection_model)
        btn_delete.setStatusTip("Delete selected keys from your computer")
        btn_delete.clicked.connect(self.delete_keys)

        btn_group_public = QtWidgets.QVBoxLayout()
        btn_group_public.addWidget(btn_download)
        btn_group_public.addWidget(btn_update)
        btn_group_public.addWidget(btn_import)
        btn_group_public.addWidget(btn_upload)
        btn_group_public.addWidget(btn_sign)
        btn_group_public.addWidget(btn_delete)
        return btn_group_public

    def update_private_keys(self):
        # Retrieve all private keys from local keyring.
        keys_private = self.app_data.config.gpg_store.list_sec_keys()
        try:
            default_key = (self.app_data.config.default_sender or
                           self.app_data.config.gpg_store.default_key())
            self.app_data.default_key_index = next(index for index, entry in enumerate(
                keys_private) if entry.fingerprint == default_key)
            self.app_data.encrypt_sender = default_key
        except StopIteration:
            pass
        self.app_data.priv_keys_model.set_data(
            {f"{key.uids[0]} {key.key_id}": key for key in keys_private})

    def update_public_keys(self):
        # Retrieve all public keys from local keyring.
        keys_public = self.app_data.config.gpg_store.list_pub_keys(sigs=True)
        self.app_data.pub_keys_model.set_data(
            {f"{key.uids[0]} {key.key_id}": key for key in keys_public})

    def update_keys(self):
        """Updated selected keys from the keyserver."""
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Updated keys")
        msg_ok.setText("Keys have been successfully updated.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key update error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)

        selected_keys = [index.model().get_value(index).fingerprint for
                         index in self.pub_keys_view.selectedIndexes()]
        if selected_keys:
            worker = Worker(crypt.download_keys, selected_keys,
                            self.app_data.config.keyserver_url,
                            self.app_data.config.gpg_store)
            worker.signals.result.connect(
                lambda x: (self.update_public_keys(),
                           self._update_display(
                               self.pub_keys_view.selectionModel().currentIndex()),
                           msg_ok.exec_()))
            worker.signals.error.connect(
                lambda x: (msg_warn.setText(format(x[1])),
                           msg_warn.exec_()))
            self.threadpool.start(worker)

    def import_key(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     "Select GPG key file",
                                                     str(Path.home()))[0]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG public key import")
        try:
            if path:
                with open(path) as fin:
                    key_data = fin.read()
                crypt.import_keys(key_data, self.app_data.config.gpg_store)
                self.update_public_keys()
                self._update_display(
                    self.pub_keys_view.selectionModel().currentIndex())
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Key has been imported.")
                msg.exec_()
        except (UnicodeDecodeError, UserError) as e:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(format(e))
            msg.exec_()

    def delete_keys(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Delete public key")
        msg.setText("Do you really want to delete the following public key?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key deletion error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        priv_keys = self.app_data.config.gpg_store.list_sec_keys()

        selected_keys = [index.model().get_value(index) for index in
                         self.pub_keys_view.selectedIndexes()]
        for key in selected_keys:
            if any(k for k in priv_keys if key.fingerprint == k.fingerprint):
                msg_warn.setText(
                    "Unable to delete key:\n\n"
                    f"{key.uids[0]}\n{key.fingerprint}\n\n"
                    "Deleting private keys (and by extension public keys "
                    "with an associated private key) is not supported by "
                    "this application. Please use an external software  "
                    "such as GnuPG (Linux, MacOS) or Kleopatra (Windows).")
                msg_warn.exec_()
                continue
            msg.setDetailedText(self.key_to_text(key))
            if key is selected_keys[0]:
                click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                try:
                    crypt.delete_keys([key.fingerprint],
                                      self.app_data.config.gpg_store)
                    self.pub_keys_view.selectionModel().clearSelection()
                except UserError as e:
                    msg_warn.setText(format(e))
                    msg_warn.exec_()
                self.text_panel.clear()
        self.update_public_keys()

    def upload_key(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Send public key")
        msg.setText(
            "Do you want to upload the selected key to the key server?")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Send public key")
        msg_ok.setText("Key has been successfully uploaded to the keyserver.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key upload error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)

        selected_keys = [index.model().get_value(index) for index in
                         self.pub_keys_view.selectedIndexes()]
        for key in selected_keys:
            msg.setDetailedText(self.key_to_text(key))
            if key is selected_keys[0]:
                click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                worker = Worker(upload_keys_workflow.upload_keys,
                                [key.fingerprint],
                                keyserver=self.app_data.config.keyserver_url,
                                gpg_store=self.app_data.config.gpg_store,
                                logger=(upload_keys_workflow.logger,),
                                on_error=raise_)
                worker.signals.result.connect(lambda x: msg_ok.exec_())
                worker.signals.error.connect(
                    lambda x: (msg_warn.setText(format(x[1])),
                               msg_warn.exec_()))
                self.threadpool.start(worker)

    def request_signature(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Key signing request")
        msg.setText("Do you want to request signature for the selected key?")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_ok = QtWidgets.QMessageBox()
        msg_ok.setIcon(QtWidgets.QMessageBox.Information)
        msg_ok.setWindowTitle("Key signing request")
        msg_ok.setText("Key signing request has been sent.")
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("Key signing request")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)

        selected_keys = [index.model().get_value(index) for index in
                         self.pub_keys_view.selectedIndexes()]
        for key in selected_keys:
            msg.setDetailedText(self.key_to_text(key))
            if key is selected_keys[0]:
                click_show_details(msgbox=msg)
            status = msg.exec_()
            if status == QtWidgets.QMessageBox.Ok:
                worker = Worker(
                    request_sigs_workflow.request_sigs,
                    key_ids=[key.key_id],
                    portal_pgpkey_endpoint_url=self.app_data.config.dcc_portal_pgpkey_endpoint_url,
                    gpg_store=self.app_data.config.gpg_store,
                    logger=(request_sigs_workflow.logger,),
                    on_error=raise_)
                worker.signals.result.connect(lambda x: msg_ok.exec_())
                worker.signals.error.connect(
                    lambda x: (msg_warn.setText(format(x[1])),
                               msg_warn.exec_()))
                self.threadpool.start(worker)

    def _update_display(self, index: QtCore.QModelIndex):
        style = (
            "<style>"
            "th {text-align: left; padding: 0 20px 5px 0;}"
            ".danger { color: red;}"
            ".safe { color: green;}"
            "</style>"
        )
        if index.isValid():
            try:
                self.text_panel.setHtml(
                    style + self.key_to_html(index.model().get_value(index)))
            except IndexError:
                self.text_panel.setHtml("")


class KeyDownloadDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.setWindowTitle("Download public keys from the server")
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.search_string = QtWidgets.QLineEdit()
        self.btn_search = QtWidgets.QPushButton("Search")
        self.btn_search.clicked.connect(self.search_keys)

        self.key_list_view = QtWidgets.QListView()
        key_list_model = QtCore.QStringListModel()
        self.key_list_view.setModel(key_list_model)

        self.btn_download = QtWidgets.QPushButton("Download")
        self.btn_download.clicked.connect(self.download_selected)

        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(
            QtWidgets.QLabel(
                "Enter a search term (e.g. user name, email, key "
                "fingerprint)"),
            0, 0)
        layout.addWidget(self.search_string, 1, 0)
        layout.addWidget(self.btn_search, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Select a key to download"), 2, 0)
        layout.addWidget(self.key_list_view, 3, 0)
        layout.addWidget(self.btn_download, 3, 1)
        layout.addWidget(btn_cancel, 4, 1)
        self.setLayout(layout)

    def search_keys(self):
        self.btn_search.setEnabled(False)
        self.key_list_view.model().setStringList([])
        worker = Worker(crypt.search_keyserver, self.search_string.text(),
                        self.parent().app_data.config.keyserver_url)
        worker.signals.result.connect(
            lambda keys: self.key_list_view.model().setStringList(
                [f"{k.uid} {k.fingerprint}" for k in keys]))
        worker.signals.finished.connect(
            lambda: self.btn_search.setEnabled(True))
        self.threadpool.start(worker)

    def download_selected(self):
        key_ids = []
        for index in self.key_list_view.selectedIndexes():
            key_ids.append(index.model().data(index).split()[-1])
        if key_ids:
            self.btn_download.setEnabled(False)
            worker = Worker(crypt.download_keys, key_ids,
                            self.parent().app_data.config.keyserver_url,
                            self.parent().app_data.config.gpg_store)
            worker.signals.result.connect(
                lambda x: self.parent().update_public_keys())
            worker.signals.finished.connect(
                lambda: self.btn_download.setEnabled(True))
            self.threadpool.start(worker)


class KeyGenDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.setWindowTitle("Generate new key pair")
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.text_name_full = QtWidgets.QLineEdit()
        self.text_name_extra = QtWidgets.QLineEdit()
        self.text_email = QtWidgets.QLineEdit()
        self.text_pass = QtWidgets.QLineEdit()
        self.text_pass_repeat = QtWidgets.QLineEdit()
        self.toggle_password_visibility(False)

        re_email = QtCore.QRegExp(r"[^@]+@[^@]+\.[^@]+")
        self.text_email.setValidator(QtGui.QRegExpValidator(re_email))

        self.btn_run = QtWidgets.QPushButton("Generate key")
        self.btn_run.setDefault(True)
        self.btn_run.clicked.connect(self.create_private_key)
        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)
        btn_show_pass = QtWidgets.QPushButton("Show")
        btn_show_pass.setCheckable(True)
        btn_show_pass.clicked[bool].connect(self.toggle_password_visibility)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Full name"), 0, 0)
        layout.addWidget(self.text_name_full, 0, 1)
        layout.addWidget(QtWidgets.QLabel("(optional) institution/project"), 1, 0)
        layout.addWidget(self.text_name_extra, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Institutional email"), 2, 0)
        layout.addWidget(self.text_email, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Password"), 3, 0)
        layout.addWidget(self.text_pass, 3, 1)
        layout.addWidget(QtWidgets.QLabel("Password (repeat)"), 4, 0)
        layout.addWidget(self.text_pass_repeat, 4, 1)
        layout.addWidget(btn_show_pass, 4, 2)
        layout.addWidget(btn_cancel, 5, 0)
        layout.addWidget(self.btn_run, 5, 1)
        layout.addWidget(
            QtWidgets.QLabel("Key generation can take a few minutes"),
            6, 0, 1, 3)
        self.setLayout(layout)

    def toggle_password_visibility(self, show: bool):
        mode = (QtWidgets.QLineEdit.Normal if show else
                QtWidgets.QLineEdit.Password)
        self.text_pass.setEchoMode(mode)
        self.text_pass_repeat.setEchoMode(mode)

    def clear_form(self):
        self.text_name_full.clear()
        self.text_name_extra.clear()
        self.text_email.clear()
        self.text_pass.clear()
        self.text_pass_repeat.clear()

    def post_key_creation(self, key: Key):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG Key Generation")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        try:
            revocation_cert = crypt.create_revocation_certificate(
                key.fingerprint, self.text_pass.text(),
                self.parent().app_data.config.gpg_store)
            msg.setText(
                "Your new key has been successfully generated.\n\n"
                "Additionally, a revocation certificate was also created. "
                "It can be used to revoke your key in the eventuality that it "
                "gets compromised, lost, or that you forgot your password.\n"
                "Please store the revocation certificate below in a safe "
                "location, as anyone can use it to revoke your key.")
            msg.setDetailedText(revocation_cert.decode())
            # Programatically click the "Show Details..." button so that the
            # certificate is shown by default.
            click_show_details(msgbox=msg)

        except UserError:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                "Key has been successfully generated. "
                "However, it was not possible to create a revocation "
                "certificate. "
                "Execute the following command to create the certificate\n\n"
                f"gpg --gen-revoke {key.fingerprint}"
            )
        finally:
            msg.exec_()
            self.clear_form()
            self.parent().update_private_keys()
            self.parent().update_public_keys()
            self.close()

    def create_private_key(self):
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG Key Generation Error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        self.btn_run.setEnabled(False)
        full_name = (f"{self.text_name_full.text()} "
                     f"{self.text_name_extra.text()}")
        worker = Worker(crypt.create_key,
                        full_name,
                        self.text_email.text(),
                        self.text_pass.text(),
                        self.text_pass_repeat.text(),
                        self.parent().app_data.config.gpg_store)
        worker.signals.result.connect(self.post_key_creation)
        worker.signals.error.connect(lambda e: (
            msg_warn.setText(format(e[1])), msg_warn.exec_()))
        worker.signals.finished.connect(
            lambda: self.btn_run.setEnabled(True))
        self.threadpool.start(worker)


def click_show_details(msgbox: QtWidgets.QMessageBox):
    for button in msgbox.buttons():
        if msgbox.buttonRole(button) is QtWidgets.QMessageBox.ButtonRole.ActionRole:
            button.click()
