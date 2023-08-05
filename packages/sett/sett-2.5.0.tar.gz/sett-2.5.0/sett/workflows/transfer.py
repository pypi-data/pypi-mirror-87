from typing import List, Tuple, Callable, Dict, Optional
import json

from . import workflow
from ..utils.config import Config
from ..utils.log import create_logger
from ..utils.progress import ProgressInterface
from ..core.crypt import get_recipient_email, extract_pub_key_ids, \
    validated_keys_by_ids, gpg
from ..core.archive import check_tar, extract, METADATA_FILE, \
    DATA_FILE_ENCRYPTED
from ..core.metadata import load_metadata, verify_transfer
from ..core.error import UserError
from ..protocols import needs_argument


logger = create_logger(__name__)


@workflow(logger, (UserError, FileNotFoundError))
def transfer(files: List[str],
             *,
             protocol,
             two_factor_callback: Callable,
             protocol_args: dict,
             config: Config,
             dry_run: bool = False,
             verify_dtr: Optional[bool] = None,
             progress: ProgressInterface = None):
    """ Transfer file(s) to the selected recipient on the BiomedIT network.
    """

    logger.info("""Input summary:
    files to transfer: %s"
    dry run          : %s""",
                "\n\t".join(files), str(dry_run))

    with logger.log_task("Input files verification"):
        for tar in files:
            check_tar(tar)

    files_by_recipient: Dict[Tuple[gpg.Key, ...], List[str]] = {}
    with logger.log_task("Extracting destination for each file to transfer"):
        for tar in files:
            logger.info("\t-> %s", tar)
            with extract(open(tar, 'rb'), METADATA_FILE, DATA_FILE_ENCRYPTED) \
                    as (metadata, encrypted_file):
                metadata = json.load(metadata)
                keys = tuple(validated_keys_by_ids(
                    extract_pub_key_ids(encrypted_file),
                    config.gpg_store,
                    config.key_validation_authority_keyid,
                    config.keyserver_url))
            metadata = load_metadata(metadata)
            if verify_dtr is None:
                verify_dtr = metadata.transfer_id is not None
            if verify_dtr:
                if metadata.transfer_id is None:
                    raise UserError("DTR (Data Transfer Request) ID is "
                                    "missing in file metadata.")
                try:
                    project_id = verify_transfer(
                        metadata=metadata,
                        filename=tar,
                        portal_endpoint_url=config.dcc_portal_dpkg_endpoint_url)
                    logger.info("DTR ID '%s' is valid for project '%s'",
                                metadata.transfer_id, project_id)
                except RuntimeError as e:
                    raise UserError(format(e)) from e
            files_by_recipient.setdefault(keys, []).append(tar)

    if dry_run:
        logger.info("Dry run completed successfully")
        return

    for recipient_keys, r_files in files_by_recipient.items():
        emails = [get_recipient_email(k) for k in recipient_keys]
        if needs_argument(protocol, "recipients"):
            protocol_args["recipients"] = emails
        if needs_argument(protocol, "two_factor_callback"):
            protocol_args["two_factor_callback"] = two_factor_callback
        if needs_argument(protocol, "pkey_password_encoding"):
            protocol_args["pkey_password_encoding"] = config.ssh_password_encoding
        with logger.log_task("Transferring files encrypted for "
                             f"{', '.join(emails)}"):
            protocol(r_files, progress=progress, **protocol_args)
