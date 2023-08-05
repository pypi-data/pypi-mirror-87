from functools import partial
from pathlib import Path
from typing import Callable, Optional

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtWidgets import QPushButton, QLabel

from .parallel import Worker
from ..utils.progress import ProgressInterface


class MandatoryLabel(QLabel):
    """A label extension which appends a '*' to label's end to mark the field as required.
    """

    def __init__(self, label: str):
        super().__init__(label + " <sup><font color='red'>*</font></sup>")


class SelectionButton(QPushButton):
    """A push button extension which connects this button to given selection model.

    The button is disabled by default. And gets enabled when the selection has, at least,
    one selected row.
    """

    def __init__(self, label: str, selection_model: QItemSelectionModel):
        super().__init__(label)
        self.setEnabled(False)
        self._selection_model = selection_model
        selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        # Following works better than using 'QItemSelection', especially in cases
        # where multiple selection is possible
        self.setEnabled(bool(len(self._selection_model.selectedRows())))
        # Repaint the button on each selection changed. Should happen automatically,
        # but does NOT seem to be always the case on Mac OS X.
        self.repaint()


class GuiProgress(QtCore.QObject, ProgressInterface):
    updated = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.n = 0

    def update(self, completed_fraction):
        self.n = completed_fraction
        self.updated.emit(round(completed_fraction * 100, 0))

    def get_completed_fraction(self):
        return self.n


class ConsoleWidget(QtWidgets.QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.textbox = QtWidgets.QPlainTextEdit()
        self.textbox.setReadOnly(True)
        btn_clear_console = QtWidgets.QPushButton("Clear console")
        btn_clear_console.clicked.connect(self.clear)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(btn_clear_console)
        self.setLayout(layout)

    def clear(self) -> None:
        self.textbox.clear()
        self.textbox.repaint()

    def append(self, text: str) -> None:
        self.textbox.appendPlainText(text)

    def write(self, text: str) -> None:
        self.textbox.appendPlainText(text)


class PathInput:
    """Path selection widget with a select button and a show path field."""

    def __init__(self, directory=True, path: Optional[Path] = Path.home(),
                 parent=None):
        self.parent = parent
        self.text = QtWidgets.QLineEdit(parent)
        self.text.setReadOnly(True)
        self.btn = QtWidgets.QPushButton("Change location")
        self.btn.clicked.connect(partial(self._update_location, directory))
        # Additional button to clear the selected path
        self.btn_clear = QtWidgets.QPushButton("Clear")
        self.btn_clear.clicked.connect(self._clear_location)
        self.update_path(path)

    def update_path(self, path: Optional[Path]):
        self.path = path
        self.text.setText("" if path is None else str(path))
        self.text.editingFinished.emit()
        # 'repaint' invocation is needed on MacOS X
        self.text.repaint()

    def _update_location(self, directory: bool):
        if self.path and self.path.exists():
            location = self.path if self.path.is_dir() else self.path.parent
        else:
            location = Path.home()
        if directory:
            new_path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent, "Select Directory", str(location))
        else:
            new_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.parent, "Select File", str(location))
        if new_path:
            self.update_path(Path(new_path))

    def _clear_location(self):
        self.update_path(None)

    @property
    def btn_label(self) -> str:
        """Button label"""
        return self.btn.text()

    @btn_label.setter
    def btn_label(self, label: str):
        self.btn.setText(label)

    @property
    def status_tip(self) -> str:
        return self.text.statusTip()

    @status_tip.setter
    def status_tip(self, msg: str):
        self.text.setStatusTip(msg)

    def on_path_change(self, fn: Callable[[Optional[Path]], None]) -> None:
        """Run callback when path changes."""
        self.text.editingFinished.connect(lambda: fn(self.path))


class TabMixin:
    def create_console(self):
        self.console = ConsoleWidget("Console", self)

    def create_progress_bar(self):
        self.progress_bar = QtWidgets.QProgressBar(self)

    @staticmethod
    def _create_disabled_button(action_name: str) -> QPushButton:
        button = QtWidgets.QPushButton(action_name)
        button.setEnabled(False)
        return button

    def set_buttons_enabled(self, enabled: bool):
        self.btn_run.setEnabled(enabled)
        self.btn_run.repaint()
        self.btn_test.setEnabled(enabled)
        self.btn_test.repaint()

    def create_run_panel(self, panel_name: str, action: Callable,
                         action_name: str):
        self.run_panel = QtWidgets.QGroupBox(panel_name)
        layout = QtWidgets.QHBoxLayout()
        self.btn_test = TabMixin._create_disabled_button("Test")
        # On pressed button, make sure that the focus switches to that button (Mac specific issue)
        self.btn_test.pressed.connect(self.btn_test.setFocus)
        self.btn_test.clicked.connect(partial(action, dry_run=True))
        self.btn_run = TabMixin._create_disabled_button(action_name)
        # On pressed button, make sure that the focus switches to that button (Mac specific issue)
        self.btn_run.pressed.connect(self.btn_run.setFocus)
        self.btn_run.clicked.connect(action)
        layout.addWidget(self.btn_test)
        layout.addWidget(self.btn_run)
        self.run_panel.setLayout(layout)

    def add_worker_actions(self, worker: Worker):
        """Attach GUI-updating signals to worker"""
        worker.signals.started.connect(
            lambda: self.run_panel.setEnabled(False))
        worker.signals.logging.connect(self.console.write)
        worker.signals.error.connect(lambda e: self.console.append(str(e[1])))
        worker.signals.finished.connect(
            lambda: self.run_panel.setEnabled(True))


def run_dialog(parent, msg: str, password: bool = True):
    dialog_pwd = QtWidgets.QInputDialog(parent)
    dialog_pwd.setLabelText(msg)
    dialog_pwd.setWindowTitle("SETT")
    if password:
        dialog_pwd.setTextEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    if dialog_pwd.exec_() != QtWidgets.QDialog.Accepted or not dialog_pwd.textValue():
        return None
    return dialog_pwd.textValue()
