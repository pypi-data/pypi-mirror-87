from typing import List

from . import workflow
from ..core.crypt import (request_key_signature, verify_key_length,
                          search_pub_key, GPGStore)
from ..core.error import UserError
from ..utils.log import create_logger


logger = create_logger(__name__)


@workflow(logger, UserError)
def request_sigs(key_ids: List[str], *, portal_pgpkey_endpoint_url: str,
                 gpg_store: GPGStore):
    """Requests signatures"""
    keys = frozenset(search_pub_key(k, gpg_store, sigs=False) for k in key_ids)
    for key in keys:
        verify_key_length(key)
    for key in keys:
        logger.info("Sending a request for '%s'", key.key_id)
        request_key_signature(key.key_id, portal_pgpkey_endpoint_url)
