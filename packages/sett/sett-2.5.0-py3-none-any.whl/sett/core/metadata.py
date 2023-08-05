import json
from dataclasses import dataclass
from urllib.error import HTTPError

from libbiomedit import metadata as _metadata

from .error import UserError
from .request import post

# Reexports
alnum_str = _metadata.alnum_str
METADATA_FILE = _metadata.METADATA_FILE
Purpose = _metadata.Purpose
HexStr1024 = _metadata.HexStr1024
HexStr256 = _metadata.HexStr256


@dataclass(frozen=True)
class MetaData(_metadata.MetaData):
    """Wrapper around libbiomedit.metadata.MetaData throwing UserError"""
    @classmethod
    def from_dict(cls, d: dict):
        try:
            return super().from_dict(d)
        except ValueError as e:
            raise UserError(format(e)) from e


load_metadata = MetaData.from_dict


def verify_transfer(metadata: MetaData,
                    filename: str,
                    portal_endpoint_url: str) -> str:
    """Verify transfer_id using external API.

    Return project_id for a valid transfer_id.
    """
    data = json.dumps({
        "file_name": filename,
        "metadata": json.dumps(MetaData.asdict(metadata))
    }).encode()
    try:
        response = post(portal_endpoint_url, data)
        return json.loads(response)["project_id"]
    except HTTPError as e:
        raise UserError(json.loads(e.read())[0]) from e
