import re
import os
import io
from datetime import datetime
from typing import Optional, List, Callable, Tuple
from pathlib import Path, PurePosixPath
from contextlib import contextmanager

from paramiko import RSAKey, DSSKey, ECDSAKey, Ed25519Key, \
    Transport, ssh_exception, SSHClient, AutoAddPolicy, SSHException, Agent

from ..utils.progress import ProgressInterface
from ..utils.log import create_logger
from ..utils.config import get_config_file
from ..core.error import UserError
from .defs import ENVELOPE_DIR_FMT


logger = create_logger(__name__)


def upload(files: List[str],  # nosec (False Positive: pkey_password_encoding)
           host: str,
           username: str,
           destination_dir: str,
           two_factor_callback: Callable,
           envelope_dir: Optional[str] = None,
           pkey: Optional[str] = None,
           pkey_password: Optional[str] = None,
           pkey_password_encoding: str = "utf_8",
           jumphost: Optional[str] = None,
           progress: Optional[ProgressInterface] = None):
    if envelope_dir is None:
        envelope_dir = datetime.now().strftime(ENVELOPE_DIR_FMT)
    progress_callback = progress and (lambda x, y: progress.update(x / y))
    remote_dir = PurePosixPath(destination_dir) / envelope_dir
    try:
        with sftp_connection(host=host, username=username, pkey=pkey,
                             jumphost=jumphost,
                             pkey_password=pkey_password,
                             pkey_password_encoding=pkey_password_encoding,
                             two_factor_callback=two_factor_callback) as sftp:
            try:
                sftp.mkdir(str(remote_dir))
            except FileNotFoundError as e:
                raise UserError("Remote destination directory does not exist: "
                                f"{destination_dir}") from e
            except PermissionError as e:
                raise UserError("You don not have enough permissions to write "
                                f"to the remote directory: {destination_dir}"
                                ) from e
            for tar in files:
                remotepath = str(remote_dir / Path(tar).name)
                remotepath_part = remotepath + ".part"
                status = sftp.put(localpath=os.path.realpath(tar),
                                  remotepath=remotepath_part,
                                  callback=progress_callback,
                                  confirm=True)
                remote_size = status.st_size
                local_size = os.path.getsize(os.path.realpath(tar))

                if local_size != remote_size:
                    raise UserError(
                        f"Incomplete file transfer: '{tar}'\n"
                        f"Remote: {remote_size}\nLocal: {local_size}")

                try:
                    sftp.posix_rename(remotepath_part, remotepath)
                except IOError as e:
                    raise UserError(format(e)) from e
            with io.BytesIO(b"") as fl:
                sftp.putfo(fl=fl,
                           remotepath=str(remote_dir / "done.txt"),
                           callback=progress_callback,
                           confirm=True)
    except ssh_exception.AuthenticationException as e:
        raise UserError(format(e)) from e


@contextmanager
def sftp_connection(host: str,  # nosec
                    username: str,
                    two_factor_callback: Callable,
                    pkey: Optional[str] = None,
                    pkey_password: Optional[str] = None,
                    pkey_password_encoding: str = "utf_8",
                    jumphost: Optional[str] = None):
    key = pkey and private_key_from_file(
        str(Path(pkey).expanduser()), pkey_password,
        encoding=pkey_password_encoding)
    if jumphost is not None:
        pw = two_factor_callback()
        sock = proxy_socket(host, jumphost, username, pkey=key, password=pw)
    else:
        sock = host
    trans = Transport(sock)
    trans.connect()
    try:
        auth(trans, username, key, two_factor_callback)
        try:
            sftp_client = trans.open_sftp_client()
            yield sftp_client
        finally:
            sftp_client.close()
    finally:
        trans.close()


def auth(trans, username, key,
         two_factor_callback: Callable):
    allowed_types = set()
    if key:
        allowed_types = trans.auth_publickey(username, key)
    else:
        try:
            allowed_types = auth_from_agent(trans, username)
        except SSHException:
            trans.auth_timeout = 120
            trans.auth_interactive(username, auth_handler)
    two_factor = bool(set(allowed_types) & _TWO_FACTOR_TYPES)
    if two_factor:
        f2_code = two_factor_callback()
        trans.auth_password(username, f2_code)


def proxy_socket(host, jumphost, username, **kwargs):
    tunnel = SSHClient()
    tunnel.set_missing_host_key_policy(AutoAddPolicy())
    tunnel.connect(jumphost, username=username, allow_agent=True,
                   **kwargs)
    return tunnel.get_transport().open_channel("direct-tcpip",
                                               parse_host(host),
                                               parse_host(jumphost))


def parse_host(host: str) -> Tuple[str, int]:
    try:
        _host, port = host.split(":")
        return _host, int(port)
    except ValueError:
        return host, 22


def auth_handler(_title, _instructions, prompt_list):
    if prompt_list:
        auth_url = re.findall(r'(https?://\S+)', prompt_list[0][0])
        if auth_url:
            logger.info("Authenticate at: %s", auth_url[0])
    resp = ['' for _ in prompt_list]
    return resp


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def private_key_from_file(path, password, encoding="utf_8"):
    errors = []
    pass_bytes = None if password is None else password.encode(encoding)
    for pkey_class in (RSAKey, DSSKey, ECDSAKey, Ed25519Key):
        try:
            return pkey_class.from_private_key_file(path, pass_bytes)
        except (SSHException, ValueError) as e:
            errors.append(e)
    if password is not None and not is_ascii(password):
        errors = [(
            "Your ssh secret key's password seems to contain "
            "some non-ascii characters.\n"
            "Either change your password ("
            "`ssh-keygen -f <path to your private key> -p`)"
            " or make sure the config option "
            "`ssh_password_encoding` is set to the same "
            "encoding, your key has been created with."
            "Your config file is here:\n" +
            get_config_file() +
            "\nThe encoding is usually `utf_8` on linux "
            "/ mac and `cp437` on windows for keys generated "
            "with ssh-keygen")] + errors
    raise UserError("Could not load private key:\n" +
                    "\n".join(format(e) for e in errors))


def auth_from_agent(transport, username):
    agent = Agent()
    try:
        for key in agent.get_keys():
            try:
                logger.debug("Trying SSH agent key %s", key.get_fingerprint())
                # for 2-factor auth a successfully auth'd key password
                # will return an allowed 2fac auth method
                return transport.auth_publickey(username, key)
            except SSHException:
                pass
    finally:
        agent.close()
    raise SSHException("Could not load key from ssh agent")


_TWO_FACTOR_TYPES = {"keyboard-interactive", "password"}
