import enum
import io
import json
import os
import re
import urllib
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Union, Type, IO, Callable, cast
from functools import wraps, partial

import gpg_lite as gpg
from libbiomedit import crypt
from .error import UserError
from .request import urlopen

GPGStore = gpg.GPGStore
extract_pub_key_ids = gpg.extract_key_id
get_default_gpg_config_dir = gpg.get_default_gpg_config_dir

ExceptionType = Union[Type[BaseException], Tuple[Type[BaseException], ...]]


def to_user_error(error_types: ExceptionType):
    """A decorator to turn errors of type :error_types: into UserError"""
    def _to_user_error(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except error_types as e:
                raise UserError(format(e)) from e
        return wrapped
    return _to_user_error


def to_user_error_gen(error_types: ExceptionType):
    """A decorator to turn errors of type :error_types: into UserError"""
    def _to_user_error(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                yield from f(*args, **kwargs)
            except error_types as e:
                raise UserError(format(e)) from e
        return wrapped
    return _to_user_error


validate_pub_key = to_user_error(RuntimeError)(crypt.validate_pub_key)
validated_keys_by_ids = to_user_error_gen(
    (RuntimeError, gpg.cmd.GPGError))(
        partial(crypt.validated_keys_by_ids, url_opener=urlopen))
refresh_keys = to_user_error(
    (RuntimeError, gpg.cmd.GPGError))(
        partial(crypt.refresh_keys, url_opener=urlopen))
fingerprint2keyid = to_user_error(RuntimeError)(crypt.fingerprint2keyid)
verify_metadata_signature = to_user_error(
    RuntimeError)(
        partial(crypt.verify_metadata_signature, url_opener=urlopen))


@to_user_error(gpg.cmd.GPGError)
def search_keyserver(name: str, keyserver: str) -> List[gpg.KeyInfo]:
    """Search keyserver for keys maching the query"""
    return list(gpg.search_keys(name, keyserver, url_opener=urlopen))


@to_user_error(gpg.cmd.GPGError)
def import_keys(key_data: str, gpg_store: GPGStore):
    """Import keys from text"""
    return gpg_store.import_file(key_data.encode())


@to_user_error(gpg.cmd.GPGError)
def delete_keys(fingerprints: List[str],
                gpg_store: GPGStore):
    """Delete public key"""
    return gpg_store.delete_keys(*fingerprints)


@to_user_error(gpg.cmd.GPGError)
def create_revocation_certificate(fingerprint: str, passphrase: str,
                                  gpg_store: GPGStore) -> bytes:
    """Create a revocation certificate for the key"""
    return gpg_store.gen_revoke(fingerprint, passphrase=passphrase)


def verify_key_length(key: gpg.Key, min_key_length: int = 4096):
    if key.key_length < min_key_length:
        raise UserError(f"Key {key.key_id} is shorter than the minimal "
                        f"required length of {min_key_length} bit")


def upload_keys(fingerprints: List[str], keyserver: str,
                gpg_store: GPGStore):
    """Upload public key to keyserver"""
    try:
        gpg_store.send_keys(*fingerprints,
                            keyserver=keyserver, url_opener=urlopen)
    except urllib.error.URLError:
        raise KeyserverError(action="upload", keyserver=keyserver) from None


def download_keys(fingerprints: List[str], keyserver: str,
                  gpg_store: GPGStore):
    """Download public key to keyserver"""
    try:
        gpg_store.recv_keys(*fingerprints,
                            keyserver=keyserver, url_opener=urlopen)
    except urllib.error.URLError:
        raise KeyserverError(action='download', keyserver=keyserver) from None


def detach_sign_file(src: Union[bytes, IO[bytes]], signature_fingerprint: str,
                     passphrase: str, gpg_store: GPGStore) -> bytes:
    """Sign a file with a detached signature"""
    try:
        with gpg_store.detach_sig(src, passphrase,
                                  signature_fingerprint) as out:
            return out.read()
    except gpg.cmd.GPGError as e:
        raise UserError(f"File signing failed. {e}") from e


def check_password(user_fingerprint: str, passphrase: str,
                   gpg_store: GPGStore):
    """Check if key password is correct"""
    try:
        with gpg_store.detach_sig(b"test", passphrase, user_fingerprint):
            pass
    except gpg.cmd.GPGError:
        raise UserError("GPG password is incorrect") from None


class KeyType(enum.Enum):
    public = enum.auto()
    secret = enum.auto()


def open_gpg_dir(gpg_dir: str) -> GPGStore:
    """Open the database inside a GnuPG directory and return it as a gpg
    object.

    :param gpg_dir: path of the GnuPG directory to open.
    :return: a gnupg GPGStore
    :raises UserError:
    """
    if not Path(gpg_dir).is_dir():
        os.makedirs(gpg_dir, mode=0o700)

    try:
        return GPGStore(config_dir=gpg_dir)
    except ValueError:
        raise UserError(f'unable to open GnuPG directory [{gpg_dir}].') from None


def retrieve_keys(gpg_store: GPGStore,
                  sender: str,
                  recipients: List[str],
                  validation_keyid: Optional[str] = None,
                  keyserver_url: Optional[str] = None,
                  with_refresh_keys: bool = True) -> Tuple[gpg.Key, List[gpg.Key]]:
    """Retrieve the following keys from the user's local GnuPG keyring:
     - public key of sender.
     - public key of recipient(s).
    Exactly one key must be found for each sender and recipient, otherwise an
    error is raised. A number of checks are also performed on the keys. The
    keys are then returned as a tuple with one sender key, and one or more
    recipient keys: (sender key, [recipient keys]).

    :param gpg_store: local GnuPG database as gpg-lite object.
    :param sender: fingerprint or email of data sender.
    :param recipients: fingerprint or email of data recipient(s). There can
        be one or more recipients.
    :param validation_keyid: fingerprint of validation key. Used to check that
        the retrieved key is signed by the validation key.
    :param keyserver_url: url of keyserver. Used for checking key origin.
    :param with_refresh_keys: if True, the found public keys are re-downloaded
        from the keyserver to make sure they are up-to-date.
    :return: tuple with one sender key, and one or more recipient keys.
    :raises UnpackError:
    """
    # Search public keys for sender and recipient(s).
    pub_keys = [search_pub_key(search_term=x, gpg_store=gpg_store, sigs=True)
                for x in [sender] + recipients]

    # If asked to do so, refresh keys by re-downloading them from keyserver.
    if with_refresh_keys:
        pub_keys = refresh_keys(keys=pub_keys,
                                gpg_store=gpg_store, sigs=True,
                                keyserver_url=keyserver_url)
    # Verify keys are signed and non-revoked.
    for key in pub_keys:
        validate_pub_key(key, validation_keyid, keyserver_url)

    # Split keys into sender and recipient(s) keys.
    sender_key, *recipient_keys = pub_keys

    # Verify a private key matching the user's public key exists. Note that
    # the key itself is not really needed because it shares the fingerprint
    # with the public key, but it has to be there.
    search_priv_key(search_term=sender_key.fingerprint, gpg_store=gpg_store)

    # Return the sender's public key, and one or more recipient public keys
    # as two separate objects.
    return (sender_key, recipient_keys)


def search_pub_key(search_term: str,
                   gpg_store: GPGStore,
                   sigs: bool = True) -> gpg.Key:
    """ Search for a single public key in the local keyring based on the input
    search term. If no or more than one key is matching the search term, an
    error is raised.

    :param gpg_store: key database as gnupg object.
    :param search_term: search term for the key, e.g. fingerprint or key owner
        email address.
    :param sigs: if True, return key with signatures.
    :return: GnuPG key matching the search term.
    :raises UnpackError:
    """
    keys = gpg_store.list_pub_keys(keys=(search_term,), sigs=sigs)
    try:
        key, = keys
    except ValueError:
        raise UnpackError(keys, key_type=KeyType.public,
                          search_value=search_term) from None
    return key


def search_priv_key(search_term: str,
                    gpg_store: GPGStore) -> gpg.Key:
    """Searches the user's local keyring for a secret key matching the search
    term. Raises an error if no or more than one key are found.
    """
    keys = gpg_store.list_sec_keys(keys=(search_term,))
    try:
        key, = keys
    except ValueError:
        raise UnpackError(keys, key_type=KeyType.secret,
                          search_value=search_term) from None
    return key


class UnpackError(UserError):
    """Error class that displays an error message for the cases when a search
    for a public/secret key on the user's local keyring does not yield exactly
    one match"""

    def __init__(self, keys, key_type: KeyType,
                 search_value: str):
        if not keys:
            msg_start = f'No {key_type.name} key'
        else:
            msg_start = f'Multiple {key_type.name} keys'
        super().__init__(msg_start + f" matching: {search_value}")


def assert_key_is_not_revoked(key: gpg.Key):
    """Check if a GnuPG key is revoked

    :param key: Key to check
    :raises UserError:
    """
    if key.validity is gpg.Validity.revoked:
        raise UserError(f"{key.uids[0]} key has been revoked")


def encrypt_and_sign(source: Callable,
                     output: Callable,
                     gpg_store: GPGStore,
                     recipients_fingerprint: List[str],
                     signature_fingerprint: Optional[str] = None,
                     passphrase: Optional[str] = None,
                     always_trust: bool = True):
    """Encrypt input data with a GnuPG public key and sign it with a GnuPG
    private key.

    In this function, the compression level of the "encrypt()" method is set
    to 0 as we are only encrypting data that has already been compressed, or
    has explicitely been requeseted by the user not to be compressed.

    There is no check of the validity of the sender and recipient keys, as it
    is assumed that this is already done earlier.

    :param source: callable writing data to encrypt.
    :param output: callable reading encrypted data.
    :param gpg_store: directory containing GnuPG keyrings as gnupg object.
    :param recipients_fingerprint: fingerprint of public key(s) with which
        the data should be encrypted.
    :param signature_fingerprint: fingerprint of private key with which the
        data should be signed. If the parameter value is set to None the
        encrypted file is not signed.
    :param passphrase: password associated to 'signature_fingerprint'. This
        parameter value can be set to None if the encrypted file should not be
        signed.
    :param always_trust: if False, the encryption key must be signed by the
        local user.
    :raises UserError:
    """
    try:
        # Note: gpg.CompressAlgo.NONE evaluates to "uncompressed", which
        # tells GnuPG to not compress the input data.
        gpg_store.encrypt(
            source=source,
            recipients=recipients_fingerprint,
            output=output,
            passphrase=passphrase,
            trust_model=gpg.TrustModel.always if always_trust
                        else gpg.TrustModel.pgp,
            sign=signature_fingerprint,
            compress_algo=gpg.CompressAlgo.NONE)
    except gpg.cmd.GPGError:
        raise UserError("Encryption failed. "
                        "Maybe you entered a wrong passphrase.") from None


def get_recipient_email(key: gpg.Key) -> str:
    try:
        email = key.uids[0].email
    except (IndexError, UnpackError):
        raise UserError(f"Could not determine email address "
                        f"for GPG key {key.key_id}.") from None
    if not email:
        raise UserError(f"GPG key [{key.key_id}] does not contain a valid "
                        f"email address.")
    return email


def decrypt(source: Union[io.FileIO, Callable],
            output: Union[str, Callable],
            gpg_store: GPGStore,
            passphrase: Optional[str]) -> List[str]:
    """Decrypt data.

    :param source: data to encrypt.
    :param output: encrypted data.
    :param gpg_store: directory containing GnuPG keyrings as gnupg object.
    :param passphrase: password associated to 'signature_fingerprint'. This
        parameter value can be set to None if the encrypted file should not be
        signed.
    :return: fingerprint or keyid of the signee's key.
    :raises UserError:
    """
    try:
        if isinstance(output, str):
            with open(output, "wb") as fout:
                sender_fprs = gpg_store.decrypt(
                    source=source,
                    output=cast(io.FileIO, fout),
                    passphrase=passphrase)
        else:
            sender_fprs = gpg_store.decrypt(
                source=source,
                output=output,
                passphrase=passphrase)
    except gpg.cmd.GPGError as e:
        raise UserError("Failed to decrypt. Error message from gpg:\n" +
                        format(e)) from e
    if not sender_fprs:
        warnings.warn("Encrypted package is not signed by the sender")
    elif len(sender_fprs) > 1:
        warnings.warn("Encrypted package has multiple signatures. "
                      "This is not compliant with the BiomedIT Protocol")
    return sender_fprs


def create_key(full_name: str, email: str, pwd: str,
               pwd_repeat: str, gpg_store: GPGStore, key_type: str = "RSA",
               key_length: int = 4096) -> gpg.Key:
    """Create a new public/private key"""
    min_pwd_len = 10
    if len(full_name) < 5:
        raise UserError("Full name must be at least 5 characters long.")
    if not re.search(r"[^@]+@[^@]+\.[^@]+", email):
        raise UserError("Invalid email address.")
    if pwd != pwd_repeat:
        raise UserError("Password do not match.")
    if len(pwd) < min_pwd_len:
        raise UserError("Password is too short (min length: "
                        f"{min_pwd_len})")
    fingerprint = gpg_store.gen_key(
        key_type=key_type, key_length=key_length, full_name=full_name,
        email=email, passphrase=pwd)
    pkey = gpg_store.list_sec_keys((fingerprint,))
    if not pkey:
        raise UserError(f"No private keys found for: {fingerprint}")
    if len(pkey) > 1:
        raise UserError(f"Multiple private keys found for: {fingerprint}")
    return pkey[0]


class KeyserverError(UserError):
    """Error class that displays an error message when the keyserver cannot
    be reached.
    :param action: either "download" or "upload".
    :param keyserver: URL of keyserver.
    """

    def __init__(self, action: str, keyserver: str):
        super().__init__(
            f'Key {action} failed as sett could not connect to the keyserver.\n'
            f'A possible cause for this is that the keyserver is temporarily '
            f'unavailable.\n'
            f'Please try to connect to [{keyserver}] using your web browser to '
            f'confirm whether the keyserver is available or not.\n'
            f'If the issue persists, please contact the DCC.')


def request_key_signature(keyid: str, signing_endpoint: str) -> bool:
    """Request key signature"""
    try:
        if not signing_endpoint.lower().startswith('http'):
            raise ValueError(f"Invalid scheme: '{signing_endpoint}'")
        data = f"pgpkey_id={keyid}".encode()
        with urlopen(signing_endpoint, data):  # nosec
            return True
    except urllib.error.HTTPError as e:
        raise UserError(json.loads(e.read())[0]) from e
    except urllib.error.URLError:
        raise UserError("Could not connect to the server.") from None
