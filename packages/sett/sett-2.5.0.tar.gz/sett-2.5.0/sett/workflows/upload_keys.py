from typing import List

from . import workflow
from ..core.crypt import (upload_keys as crypt_upload_keys, verify_key_length,
                          search_pub_key, GPGStore)
from ..core.error import UserError
from ..utils.log import create_logger


logger = create_logger(__name__)


@workflow(logger, UserError)
def upload_keys(key_ids: List[str], *, keyserver: str, gpg_store: GPGStore):
    """Upload keys"""
    keys = frozenset(search_pub_key(k, gpg_store, sigs=False) for k in key_ids)
    for key in keys:
        verify_key_length(key)
    if keys:
        logger.info("Uploading keys '%s'", ", ".join(k.key_id for k in keys))
        crypt_upload_keys([k.fingerprint for k in keys],
                          keyserver=keyserver, gpg_store=gpg_store)
