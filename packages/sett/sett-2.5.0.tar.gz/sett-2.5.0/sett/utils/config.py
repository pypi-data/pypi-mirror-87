import os
import platform
import json
from typing import Tuple, Dict, Any, Optional
import tempfile

import dataclasses
from dataclasses import dataclass

from libbiomedit.lib.deserialize import deserialize

from .log import exception_to_message, get_default_log_dir, create_logger
from ..core.crypt import open_gpg_dir, get_default_gpg_config_dir
from ..core.error import UserError
from .. import APP_NAME_SHORT


CONFIG_FILE_NAME = "config.json"

conf_sub_dir_by_os: Dict[str, Tuple[str, ...]] = {
    "Linux": (".config",),
    "Darwin": (".config",),
    "Windows": ("AppData", "Roaming")
}

logger = create_logger(__name__)


@dataclass(frozen=True)
class Connection:
    """dataclass holding config fo a connection (sftp / liquid files)"""
    protocol: str
    parameters: Dict[str, Any]


TMP_DIR = tempfile.gettempdir()


@dataclass
class Config:
    """dataclass holding config data"""

    dcc_portal_url: str = "https://portal.dcc.sib.swiss"
    keyserver_url: Optional[str] = 'keyserver.dcc.sib.swiss'
    gpg_config_dir: str = get_default_gpg_config_dir()
    key_validation_authority_keyid: Optional[str] = "881685B5EE0FCBD3"
    sign_encrypted_data: bool = True
    always_trust_recipient_key: bool = True
    repo_url: str = "https://pypi.org"
    check_version: bool = True
    offline: bool = False
    log_dir: str = get_default_log_dir()
    log_max_file_number: int = 1000
    connections: Dict[str, Connection] = dataclasses.field(
        default_factory=lambda: {})
    temp_dir: str = TMP_DIR
    output_dir: Optional[str] = None
    ssh_password_encoding: str = "utf_8"
    default_sender: Optional[str] = None
    gui_quit_confirmation: bool = True
    compression_level: int = 5

    def __post_init__(self):
        for url in ('dcc_portal_url', 'repo_url'):
            setattr(self, url, getattr(self, url).rstrip('/'))

    @property
    def dcc_portal_pgpkey_endpoint_url(self) -> str:
        return self.dcc_portal_url + "/backend/pgpkey/sign-request/"

    @property
    def dcc_portal_dpkg_endpoint_url(self) -> str:
        return self.dcc_portal_url + "/backend/data-package/check/"

    @property
    def gpg_store(self):
        return exception_to_message(
            UserError, logger)(open_gpg_dir)(self.gpg_config_dir)


@exception_to_message(logger=logger)
def load_config() -> Config:
    """Loads the config, returning a Config object"""
    cfg_dct = sys_config_dict()
    cfg_dct.update(load_config_dict(get_config_file()))
    return deserialize(Config)(cfg_dct)


def create_config() -> str:
    """Creates a new config file in the home directories config folder
    :return: The path of the created file"""
    config_dir = get_config_dir()
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    config_file = get_config_file()

    with open(config_file, 'w') as f:
        json.dump(config_to_dict(default_config()),
                  f, indent=2, sort_keys=True)
    return config_file


def config_to_dict(config: Config) -> dict:
    """Converts a Config object into a dict"""
    return dataclasses.asdict(config)


def default_config() -> Config:
    """Creates a new Config object with default values"""
    return deserialize(Config)(sys_config_dict())


def sys_config_dict() -> dict:
    """On linux only: try to load global sys config.
    If the env variable `SYSCONFIG` is set search there, else in
    `/etc/{APP_NAME_SHORT}`"""
    if platform.system() == "Linux":
        sys_cfg_dir = os.environ.get("SYSCONFIG", os.path.join(
            "/etc", APP_NAME_SHORT))
        return load_config_dict(os.path.join(sys_cfg_dir, CONFIG_FILE_NAME))
    return {}


def load_config_dict(path: str) -> dict:
    """Load raw config as a dict"""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_config_file() -> str:
    """user platform specific config file"""
    return os.path.join(get_config_dir(), CONFIG_FILE_NAME)


def get_config_dir() -> str:
    """user platform specific config direcory"""
    return os.path.join(
        os.path.expanduser("~"),
        *conf_sub_dir_by_os[platform.system()],
        APP_NAME_SHORT)
