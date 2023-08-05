import io
import json
import os
from functools import partial
from pathlib import Path
from typing import List, Optional, Callable, Tuple, Union

from . import workflow
from ..utils.config import Config
from ..utils.log import create_logger
from ..core.archive import write_tar, ArchiveInMemoryFile, ArchiveFile, \
    ArchiveFileBase, METADATA_FILE, METADATA_FILE_SIG, \
    DATA_FILE_ENCRYPTED, CHECKSUM_FILE, \
    CONTENT_FOLDER
from ..core.filesystem import search_files_recursively, \
    check_file_read_permission, form_output_tar_name, delete_files
from ..core.crypt import retrieve_keys, encrypt_and_sign, \
    detach_sign_file, check_password
from ..core.checksum import write_checksums, compute_checksum_on_write
from ..core.error import UserError
from ..core.metadata import MetaData, alnum_str, Purpose, HexStr1024, \
    HexStr256, verify_transfer
from ..utils.progress import ProgressInterface, subprogress, progress_file_iter

DATE_FMT_FILENAME = "%Y%m%dT%H%M%S"
logger = create_logger(__name__)
output_name_str = alnum_str(min_length=1, max_length=50, allow_dots=True)


def path_str(directory: bool = False, writable: bool = False) -> Callable:
    """Generate a 'type definition' function that will check that a string is
    a valid path (file or directory).
    :param directory: if True, the path must be a directory.
    :param writable: if True, the user must have write access to the path.
    :returns: type check function.
    :raises ValueError:
    """
    def _path_str(path_to_check):
        path = Path(path_to_check)
        if not path.exists():
            raise ValueError(f"Invalid path: '{path_to_check}'. "
                             f"Path does not exist.")
        if directory and not path.is_dir():
            raise ValueError(f"Invalid path: '{path_to_check}'. "
                             f"Path is not a directory.")
        if writable and not os.access(path.as_posix(), os.W_OK):
            raise ValueError(f"Invalid path: '{path_to_check}'. "
                             f"Path is not writable.")
        return path_to_check
    return _path_str


output_path_str = path_str(directory=True, writable=True)


def check_arg_value(arg_value: Union[str, int],
                    arg_name: str,
                    arg_type: Callable) -> None:
    """Verify that the value of variable arg_value that is named arg_name is
    following type arg_type. arg_type is a function that does a check
    of the type of the variable.
    """
    try:
        arg_type(arg_value)
    except ValueError as e:
        raise UserError(f"Invalid value for argument '{arg_name}': {e}") from e


def check_integer_in_range(min_value: int, max_value: int) -> Callable:
    """Generate a function that will check that its input value is an integer,
    and that this integer is in the range [min_value:max_value].
    """
    def _integer_in_range(value_to_check: Union[int, str]) -> None:
        try:
            value_to_check = int(value_to_check)
        except ValueError as e:
            raise ValueError("value must be an integer") from e

        if value_to_check < min_value or value_to_check > max_value:
            raise ValueError(f"value must be in the range "
                             f"[{min_value}-{max_value}]")
    return _integer_in_range

check_compression_level = check_integer_in_range(min_value=0, max_value=9)


# pylint: disable=too-many-statements
@workflow(logger, (UserError, FileNotFoundError, PermissionError))
def encrypt(files: List[str],
            *,
            config: Config,
            recipient: List[str],
            dtr_id: Optional[int] = None,
            sender: Optional[str] = None,
            passphrase: Optional[str] = None,
            output_name: Optional[str] = None,
            dry_run: bool = False,
            offline: bool = False,
            verify_dtr: bool = True,
            compression_level: Optional[int] = None,
            purpose: Optional[Purpose] = None,
            progress: ProgressInterface = None) -> None:
    """Compress and encrypt files and/or directories.
    """

    # Retrive non-specified, optional argument values from config.
    if sender is None:
        sender = config.default_sender or config.gpg_store.default_key()
        if sender is None:
            raise UserError("Sender not specified with no default sender.")
    if compression_level is None:
        compression_level = config.compression_level
    check_arg_value(arg_value=compression_level,
                    arg_name="compression level",
                    arg_type=check_compression_level)

    if not files:
        raise UserError("Empty file list")

    files_to_encrypt = list(search_files_recursively(files))

    with logger.log_task("Input data check"):
        check_file_read_permission(files_to_encrypt)
        # Retrieve the lowest common directory of all input files/directories.
        root_dir = os.path.commonpath([Path(x).absolute().parent.as_posix()
                                       for x in files])
        if dtr_id is None and verify_dtr:
            raise UserError("DTR (Data Transfer Request) ID is missing.")
        if output_name:
            check_arg_value(Path(output_name).name,
                            "output name", output_name_str)
            check_arg_value(Path(output_name).parent.as_posix(),
                            "path in output name", output_path_str)

    with logger.log_task("Retrieve sender and recipient GnuPG keys"):
        # Retrieve the sender's public and private keys, as well as the
        # recipient's public key. Here is what these keys are needed for:
        #  - sender private key: needed to sign the encrypted data.
        #  - sender public key : will be checked to make sure it is signed by
        #       the DCC. Only private keys with a matching public key that is
        #       signed by the DCC will be allowed to be used.
        #  - recipient public key: needed to encrypt the data.
        #
        # The sender/recipient information can be either an email, a keyID or
        # a full fingerprint.
        sender_pub_key, recipients_pub_key = retrieve_keys(
            gpg_store=config.gpg_store,
            sender=sender,
            recipients=recipient,
            validation_keyid=config.key_validation_authority_keyid,
            keyserver_url=config.keyserver_url,
            with_refresh_keys=not offline)
        logger.info("found the following keys:\n%s\n%s",
                    f"sender key: {sender_pub_key.uids[0]}, "
                    f"key ID: {sender_pub_key.key_id}",
                    '\n'.join([f"recipient key: {key.uids[0]}, "
                               f"key ID: {key.key_id}"
                               for key in recipients_pub_key]))

        if dtr_id is not None:
            if purpose is None:
                raise UserError("DTR ID specified but `purpose` is missing")
            if not offline and verify_dtr:
                try:
                    project_id = verify_transfer(
                        metadata=MetaData(
                            transfer_id=dtr_id,
                            sender=HexStr1024(sender_pub_key.fingerprint),
                            recipients=[HexStr1024(key.fingerprint)
                                        for key in recipients_pub_key],
                            checksum=HexStr256("0"*64),
                            purpose=purpose),
                        filename="missing",
                        portal_endpoint_url=config.dcc_portal_dpkg_endpoint_url)
                    logger.info("DTR ID '%s' is valid for project '%s'",
                                dtr_id, project_id)
                except RuntimeError as e:
                    raise UserError(format(e)) from e
    if dry_run:
        logger.info("dry run completed successfully.")
        return

    # Check if gpg key password is correct
    if config.sign_encrypted_data:
        check_password(sender_pub_key.fingerprint,
                       enforce_passphrase(passphrase),
                       config.gpg_store)

    archive_paths = [os.path.join(
        CONTENT_FOLDER,
        os.path.relpath(f, start=root_dir)) for f in files_to_encrypt]

    with logger.log_task("Compute sha256 checksum on input files"):
        # Write input file checksums to a file that will be added to the
        # encrypted .tar.gz archive. This information must be encrypted as
        # file names sometimes contain information about their content.
        with subprogress(progress,
                         step_completion_increase=0.2) as scaled_progress:
            checksums = write_checksums(
                zip(archive_paths,
                    progress_file_iter(files=files_to_encrypt,
                                       mode='rb',
                                       progress=scaled_progress)))

    with logger.log_task("Compress and encrypt input data "
                         "[this can take a while]"):
        # Encryption is done with the recipient's public key and the optional
        # signing with the user's (i.e sender) private key. The user's private
        # key passphrase is needed to sign the encrypted file.
        encrypted_file = os.path.join(config.temp_dir, DATA_FILE_ENCRYPTED)
        encrypted_checksum_buf = io.StringIO()
        with subprogress(progress,
                         step_completion_increase=0.75) as scaled_progress:
            # Create a tar archive containing all input files
            archive_content: Tuple[ArchiveFileBase, ...] = \
                ((ArchiveInMemoryFile(CHECKSUM_FILE, checksums),) +
                tuple(ArchiveFile(a_path, f) for a_path, f in zip(
                    archive_paths, progress_file_iter(files=files_to_encrypt,
                                                      mode='rb',
                                                      progress=scaled_progress)))
                )
            with open(encrypted_file, "wb") as fout:
                encrypt_and_sign(
                    source=partial(write_tar,
                                   archive_content,
                                   compress_level=compression_level,
                                   compress_algo='gz'),
                    output=partial(compute_checksum_on_write,
                                   fout=fout,
                                   checksum_buffer=encrypted_checksum_buf),
                    gpg_store=config.gpg_store,
                    recipients_fingerprint=[key.fingerprint
                                            for key in recipients_pub_key],
                    signature_fingerprint=sender_pub_key.fingerprint if
                        config.sign_encrypted_data else None,
                    passphrase=enforce_passphrase(passphrase) if
                        config.sign_encrypted_data else None,
                    always_trust=config.always_trust_recipient_key)
        encrypted_checksum = encrypted_checksum_buf.read()

    try:
        with logger.log_task("Generate metadata file"):
            # Create a dictionary with all the info we want to store in the
            # .json file, then pass this dictionary to json.dump that will
            # convert it to a json file.
            # Use indent=4 to make the output file easier on the eye.
            metadata = MetaData(transfer_id=dtr_id,
                                sender=HexStr1024(sender_pub_key.fingerprint),
                                recipients=[HexStr1024(key.fingerprint)
                                            for key in recipients_pub_key],
                                purpose=purpose,
                                checksum=HexStr256(encrypted_checksum),
                                compression_algorithm='gzip' if
                                    compression_level > 0 else '')
            metadata_bytes = json.dumps(
                MetaData.asdict(metadata), indent=4).encode()
            metadata_signature_bytes = b""
            if config.sign_encrypted_data:
                metadata_signature_bytes = detach_sign_file(
                    metadata_bytes,
                    sender_pub_key.fingerprint,
                    enforce_passphrase(passphrase),
                    config.gpg_store)

        with logger.log_task("Generate final tarball"):
            # The default value for the output name is based on date and time
            # when the script is being run.
            # Example output name is "20191011T145012".
            output_name = form_output_tar_name(
                output_name or metadata.timestamp.strftime(DATE_FMT_FILENAME))  # pylint: disable=no-member
            in_memory_files = ((METADATA_FILE, metadata_bytes),
                               (METADATA_FILE_SIG, metadata_signature_bytes))
            with subprogress(progress,
                             step_completion_increase=0.05) as scaled_progress:
                archive_content = (
                    tuple(ArchiveInMemoryFile(path, content)
                          for path, content in in_memory_files) +
                    tuple(ArchiveFile(os.path.relpath(
                            f.name, start=config.temp_dir), f)
                          for f in progress_file_iter(
                            files=[encrypted_file],
                            mode='rb',
                            progress=scaled_progress))
                    )
                write_tar(content=archive_content,
                          output=output_name,
                          compress_level=0)
    finally:
        delete_files(encrypted_file)

    logger.info("Completed data encryption: %s", output_name)

def enforce_passphrase(passphrase: Optional[str]) -> str:
    if passphrase is None:
        raise ValueError("No password given")
    return passphrase
