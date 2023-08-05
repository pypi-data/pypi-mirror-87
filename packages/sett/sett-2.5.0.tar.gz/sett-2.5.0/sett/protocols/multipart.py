import mimetypes
import uuid
from typing import Tuple


def encode(name: str, filename: str, data: bytes, extra_data=()) -> Tuple[str, bytes]:
    boundary = uuid.uuid4().hex
    content_type = 'multipart/form-data; boundary={}'.format(boundary)
    boundary_b = boundary.encode()
    inner_content_type = (mimetypes.guess_type(
        filename)[0] or 'application/octet-stream').encode()
    name_b = name.encode()
    filename_b = filename.encode()
    boundary_token = b'--' + boundary_b + b'\r\n'
    return content_type, \
        b"".join(map(lambda key_val: boundary_token + encode_value(*key_val), extra_data)) \
        + b'--' + boundary_b + b'\r\n' \
        b'Content-Disposition: form-data; name="' + name_b + b'"; filename="' \
        + filename_b + b'"\r\n' \
        b'Content-Type: ' + inner_content_type + b'\r\n' \
        b'\r\n' \
        + data \
        + b'\r\n--' + boundary_b + b'--\r\n'


def encode_value(key: str, value) -> bytes:
    return b'Content-Disposition: form-data; name="' + key.encode() + b'"\r\n' \
        b'\r\n' \
        + str(value).encode() + b'\r\n'
