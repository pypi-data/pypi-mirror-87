from pathlib import Path
from typing import Iterable, List

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QAbstractButton

from sett.gui.component import SelectionButton, MandatoryLabel


class FileSelectionWidget(QtWidgets.QGroupBox):
    """File selection widget"""

    def __init__(self, label_text, parent, name_filter=None):
        super().__init__("Input", parent)
        self.path = str(Path.home())
        self.name_filter = name_filter

        self.file_list_model = QtCore.QStringListModel()
        self.file_list_view = QtWidgets.QListView(self)
        self.file_list_view.setModel(self.file_list_model)
        self.file_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.file_list_view.setLayout(QtWidgets.QVBoxLayout())

        buttons = self._create_buttons()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(MandatoryLabel(label_text), 0, 0, 1, 2, QtCore.Qt.AlignTop)
        layout.addWidget(self.file_list_view, 1, 0, len(buttons), 1)
        for i, btn in enumerate(buttons):
            layout.addWidget(btn, i + 1, 2)
        self.setLayout(layout)

    def get_list(self) -> List[str]:
        """Returns the paths."""
        return self.file_list_model.stringList()

    def _create_buttons(self) -> List[QAbstractButton]:
        return [self._create_add_files_button(), self._create_remove_selected_button(),
                self._create_clear_list_button()]

    def _create_add_files_button(self) -> QAbstractButton:
        button = QtWidgets.QPushButton('Add files', self)
        button.clicked.connect(self._add_files)
        return button

    def _create_remove_selected_button(self) -> QAbstractButton:
        def clear_selected() -> None:
            indices = self.file_list_view.selectedIndexes()
            for index in indices:
                self.file_list_model.removeRows(index.row(), 1)
            self.file_list_model.layoutChanged.emit()

        button = SelectionButton('Remove selected',
                                 self.file_list_view.selectionModel())
        button.clicked.connect(clear_selected)
        return button

    def _create_clear_list_button(self) -> QAbstractButton:
        def clear_list() -> None:
            # Clear the selection BEFORE resetting the model
            self.file_list_view.selectionModel().clearSelection()
            self.file_list_model.setStringList([])
            self.file_list_model.layoutChanged.emit()

        button = QtWidgets.QPushButton('Clear list', self)
        button.clicked.connect(clear_list)
        return button

    def _update_paths(self, paths: Iterable[str]) -> None:
        paths = set(filter(None, paths))
        if paths:
            self.path = Path(next(iter(paths))).parent
        self.file_list_model.setStringList(
            sorted(set(self.file_list_model.stringList()) | paths))
        self.file_list_model.layoutChanged.emit()

    def _add_files(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dialog.setDirectory(str(self.path))
        if self.name_filter:
            dialog.setNameFilter(self.name_filter)
            dialog.selectNameFilter(self.name_filter)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._update_paths(dialog.selectedFiles())


class DirectoryAndFileSelectionWidget(FileSelectionWidget):
    """File selection widget extension adding directory selection"""

    def __init__(self, label_text, parent):
        super().__init__(label_text, parent)

    def _create_buttons(self):
        buttons = super()._create_buttons()
        buttons.insert(1, self._create_add_directory_button())
        return buttons

    def _create_add_directory_button(self):
        def add_directory():
            directory = (QtWidgets.QFileDialog.getExistingDirectory(
                self, 'Select directory', str(self.path)))
            self._update_paths((directory,))

        button = QtWidgets.QPushButton('Add directory', self)
        button.clicked.connect(add_directory)
        return button


class ArchiveOnlyFileSelectionWidget(FileSelectionWidget):
    """File selection widget extension for selecting TAR archives only."""

    def __init__(self, label_text, parent):
        super().__init__(label_text, parent, "Archives *.tar (*.tar)")
