from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Hashable, Iterable, List, Optional, Tuple, Union, Sequence, Callable

from PySide2 import QtCore

from ..core.metadata import Purpose
from ..utils.config import Config


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data: Sequence[Sequence[Any]] = (),
                 columns: Optional[Tuple[str, ...]] = None):
        super().__init__()
        self.set_data(data or tuple(tuple()))
        self.columns = columns or tuple(
            map(str, range(self.columnCount())))

    @property
    def columns(self) -> Tuple[str, ...]:
        return self._columns

    @columns.setter
    def columns(self, values: Sequence[str]):
        self._columns = tuple(values)

    def get_data(self) -> Tuple[Sequence[Any], ...]:
        return self._data

    def set_data(self, data: Sequence[Sequence[Any]]) -> None:
        self._data = tuple(sorted(tuple(x) for x in data))
        self.layoutChanged.emit()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(), self.columnCount()))

    def rowCount(self, _parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, _parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._data) and len(self._data[0])

    def headerData(self, section: int, orientation=QtCore.Qt.Horizontal,
                   role=QtCore.Qt.DisplayRole) -> Optional[str]:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._columns[section]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return str(section)
        return None

    # Default value Qt.DisplayRole for index is not an int (upstream issue):
    def data(self, index: QtCore.QModelIndex,  # type: ignore
             role: int) -> Optional[Hashable]:
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def removeRows(self, row: int, count: int, _parent=QtCore.QModelIndex()) -> bool:
        if row > -1 and row + count <= self.rowCount():
            self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
            self.set_data(self.get_data()[:row] +
                          self.get_data()[row + count:])
            self.endRemoveRows()
            return True
        return False


class KeyValueListModel(QtCore.QAbstractListModel):
    """List model extension for key-value objects."""

    def __init__(
            self,
            *args,
            data: Optional[Iterable[Tuple[Hashable, Any]]] = None,
            **kwargs):
        super().__init__(*args, **kwargs)
        self.set_data(data or [])

    def set_data(self, data: Iterable[Tuple[Hashable, Any]]) -> None:
        self._keyvalues = dict(data)
        self._keys = list(self._keyvalues.keys())
        self.layoutChanged.emit()

    # Default value Qt.DisplayRole for index is not an int (upstream issue):
    def data(self, index, role) -> Optional[Hashable]:   # type: ignore
        if role == QtCore.Qt.DisplayRole:
            return self._keys[index.row()]
        return None

    def rowCount(self, _parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return len(self._keys)

    def get_value(self, index: Union[int, QtCore.QModelIndex]) -> Any:
        if isinstance(index, int):
            return self._keyvalues[self._keys[index]]
        if isinstance(index, QtCore.QModelIndex):
            return self._keyvalues[self._keys[index.row()]]
        raise TypeError("Wrong index type for index.")


@dataclass
class AppData:
    config: Config

    encrypt_sender: str = ""
    encrypt_recipients: Tuple[str, ...] = ()
    encrypt_transfer_id: Optional[str] = None
    encrypt_purpose: Optional[Purpose] = None
    encrypt_compress: bool = True
    encrypt_output_suffix: str = ""
    encrypt_output_location: Path = field(default_factory=Path.home)
    encrypt_files: List[str] = field(default_factory=list)
    encrypt_verify_dtr: bool = True

    decrypt_decrypt_only: bool = False
    decrypt_output_location: Path = field(default_factory=Path.home)
    decrypt_files: List[str] = field(default_factory=list)

    transfer_protocol_name: str = "sftp"
    transfer_protocol_args: Dict = field(default_factory=dict)
    transfer_files: List[str] = field(default_factory=list)
    transfer_verify_dtr: bool = True

    priv_keys_model: KeyValueListModel = field(
        default_factory=KeyValueListModel)
    pub_keys_model: KeyValueListModel = field(
        default_factory=KeyValueListModel)
    default_key_index: Optional[int] = None

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if hasattr(self, '_listeners'):
            for callback in self._listeners[attr]:
                callback()

    def add_listener(self, attr, listener: Callable):
        self._listeners[attr].append(listener)

    def __post_init__(self):
        self._listeners = defaultdict(list) # pylint: disable=attribute-defined-outside-init
        if self.config.offline:
            self.encrypt_verify_dtr = self.transfer_verify_dtr = False
        if self.config.output_dir:
            self.encrypt_output_location = Path(self.config.output_dir)
            self.decrypt_output_location = Path(self.config.output_dir)
