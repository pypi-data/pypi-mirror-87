import io
import os
import hashlib
from pathlib import Path
from typing import Tuple, Iterable, IO
from .error import UserError


def compute_checksum_sha256(file_object: IO[bytes],
                            block_size: int = 65536) -> str:
    """Compute a sha256 checksum on a file by reading it by chunks of
    'block_size' bytes at a time.

    :param file_object: input file as a FileIO object.
    :param block_size: size of blocks (in bytes) to be returned by the
        generator function. The default block size is 2^16 = 65536 bytes.
    :return: checksum
    """
    hash_value = hashlib.sha256()
    block = file_object.read(block_size)
    while block:
        hash_value.update(block)
        block = file_object.read(block_size)
    return hash_value.hexdigest()


def compute_checksum_on_write(stream: IO[bytes],
                              fout: io.FileIO,
                              checksum_buffer: io.StringIO,
                              block_size: int = 65536) -> None:
    """Compute a sha256 checksum on stream while writing it to a file at the
    same time.

    :param stream: a stream of bytes to checksum and write to disk.
    :param fout: output file object.
    :param checksum_buffer: a buffer to store the checksum.
    :param block_size: size of blocks (in bytes) to be returned by the
        generator function. The default block size is 2^16 = 65536 bytes.
    """
    hash_value = hashlib.sha256()
    block = stream.read(block_size)
    while block:
        hash_value.update(block)
        fout.write(block)
        block = stream.read(block_size)
    checksum_buffer.write(hash_value.hexdigest())
    checksum_buffer.seek(0)


def write_checksums(entries: Iterable[Tuple[str, IO[bytes]]]) -> bytes:
    """Returns bytes string containing lines in the format
    `<checksum> <file name>`
    (can directly be used by shasum: sha256sum --check *.sha256)

    Note that **DOS** path separators will be replaced by **Unix** ones.

    :param entries: Tuples of the form (archive_path, file like object)
    :return: The bytes string containing file names and hashes
    Here is an example:

    a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd testDir/file1.fastq
    f8d2d394264823e711fgc34e4ac83f8cbc253c6we034f testDir/file2.fastq
    78f3b23fe49cf5f7f245ddf43v9788d9e62c0971fe5fb testDir/subdir2/file4.fastq
    :raises UserError: if backslash is used for archive name (on POSIX systems)
    """
    lines = []
    for archive_path, opener in entries:
        with opener as f_hash:
            checksum = compute_checksum_sha256(file_object=f_hash)
        if os.path.sep == '/' and '\\' in archive_path:
            raise UserError("On POSIX systems, backslashes are NOT allowed.")
        # Replace DOS path separators with Unix ones
        posix_path = Path(archive_path).as_posix()
        lines.append((
            f'{checksum} {posix_path}\n').encode())
    return b"".join(lines)


def verify_checksums(checksums: Iterable[Tuple[str, str]],
                     base_path: str) -> None:
    """Checks that the checksum values of files listed in the 'checksums'
    generator match their hash values (also provided in 'checksums'). The
    function raises an error if a mismatch is detected.

    :param checksums: tuples of type (checksum value, file path).
    :param base_path: path of the directory containing the files to check.
    :raises UserError:
    """
    for checksum, file_name in checksums:
        # Open file in read-only mode and verify its checksum is the same
        # as the one given in input_file. File name should be posix, just in case it is NOT...
        file_path = Path(base_path) / \
            Path(file_name.replace('\\', os.path.sep))
        with open(file_path, 'rb') as f:
            computed = compute_checksum_sha256(f)
            checksum = checksum.lower()
            if checksum != computed:
                raise UserError(f'Checksum mismatch for: {file_name}\nExpected: {checksum}'
                                f'\nGot: {computed}')


def read_checksum_file(f: IO[bytes]) -> Iterable[Tuple[str, str]]:
    """Reads lines from a file object and parses them in the form:
     a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd testDir/file1.fastq
     f8d2d394264823e711fgc34e4ac83f8cbc253c6we034f testDir/file2.fastq
     78f3b23fe49cf5f7f245ddf43v9788d9e62c0971fe5fb testDir/subdir2/file4.fastq

    The reason the input argument is a file object and not a file path is so
    that the function is more flexible and also allows to read input from
    a stream rather than an actual file.

    :param f: file object.
    :return: generator of tuples of the form (checksum value, file path).
    :raises UserError:
    """
    for line in f:
        # Split line into checksum and file name values. Each line must have
        # exactly 2 elements.
        try:
            checksum, file_name = line.decode().rstrip("\n\r").split(maxsplit=1)
        except ValueError:
            raise UserError("Input must have exactly 2 elements per line.") from None
        if os.path.isabs(file_name):
            raise UserError("Absolute path in checksum file")
        yield checksum, file_name
