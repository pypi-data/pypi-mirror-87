# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import hashlib
import os

import magic
from jinja2.filters import do_filesizeformat

from .core import BaseStorage
from kadi.lib.exceptions import KadiChecksumMismatchError
from kadi.lib.exceptions import KadiFilesizeExceededError
from kadi.lib.exceptions import KadiFilesizeMismatchError
from kadi.lib.utils import get_truth


class LocalStorage(BaseStorage):
    """Storage provider that uses the local file system.

    :param max_size: (optional) See :class:`.BaseStorage`.
    :param buffer_size: (optional) The buffer size in bytes to use in memory when
        reading files.
    """

    def __init__(self, max_size=None, buffer_size=16384):
        super().__init__(max_size=max_size)
        self.buffer_size = buffer_size

    @staticmethod
    def filepath_from_name(filename, dir_len=2, num_dirs=3):
        r"""Create a path from a filename.

        Splits up a filename ``"abcdefg"`` into the file path ``"ab/cd/ef/g"``, assuming
        default argument values. Useful to avoid storing lots of files in the same
        directory.

        :param filename: The name of the file.
        :param dir_len: (optional) Length of each directory.
        :param num_dirs: (optional) Number of directories.
        :return: The file path or the original filename, if its length is smaller than
            or equals ``dir_len`` \* ``num_dirs``.
        """
        if dir_len < 1 or num_dirs < 1 or len(filename) <= dir_len * num_dirs:
            return filename

        dirs = [filename[i : i + dir_len] for i in range(0, len(filename), dir_len)]

        filepath = os.path.join(*dirs[0:num_dirs], filename[num_dirs * dir_len :])

        return filepath

    @staticmethod
    def remove_empty_parent_dirs(path, num_dirs=1):
        """Remove empty parent directories given a file name.

        Especially useful in tandem with :meth:`filepath_from_name` to remove unneeded
        directories.

        :param path: The file name to use as base.
        :param num_dirs: (optional) The maximum number of parent directories to remove.
        """
        iteration = 0
        current_dir = os.path.dirname(path)

        while os.path.isdir(current_dir) and not os.listdir(current_dir):
            if iteration >= num_dirs:
                break

            try:
                os.rmdir(current_dir)
                current_dir = os.path.dirname(current_dir)
                iteration += 1
            except OSError:
                break

    def open(self, filename, mode="rb", encoding=None):
        """Open a file in a specific mode.

        :param filename: The name of the file.
        :param mode: (optional) The file mode to open the file with.
        :param encoding: (optional) The encoding of the file to use in text mode.
            Defaults to ``"utf-8"``.
        :return: The open file object.
        """
        return open(filename, mode=mode, encoding=encoding)

    def close(self, file):
        """Close an open file.

        :param file: The file to close.
        """
        file.close()

    def _copy_file_content(self, dst, file, mode):
        if mode == "a":
            current_size = self._get_size(dst)
        else:
            current_size = 0

        with open(dst, mode + "b") as file_dst:
            buf = file.read(self.buffer_size)

            while buf:
                current_size += len(buf)
                if self.max_size and current_size > self.max_size:
                    msg = f"File is larger than {do_filesizeformat(self.max_size)}."
                    raise KadiFilesizeExceededError(msg)

                file_dst.write(buf)
                buf = file.read(self.buffer_size)

    def save(self, dst, file_or_src, append=False):
        """Save a file or file-like object in a specific location.

        :param dst: The destination of the new file.
        :param file_or_src: A file-like object to save or the name of an existing file
            to copy instead.
        :param append: (optional) Flag to indicate if an existing file should be
            overwritten or appended to.
        :raises KadiFilesizeExceededError: If the maximum file size was the storage was
            configured with is exceeded.
        """
        mode = "a" if append else "w"
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        if isinstance(file_or_src, str):
            with open(file_or_src, "rb") as file:
                self._copy_file_content(dst, file, mode)
        else:
            self._copy_file_content(dst, file_or_src, mode)

    def move(self, src, dst):
        """Move a file to a specific location.

        :param src: The source path of the file.
        :param dst: The destination path of the file.
        """
        try:
            # Try renaming the file first, which only works if both files are on the
            # same file system.
            os.rename(src, dst)
        except OSError:
            self.save(dst, src)
            self.delete(src)

    def delete(self, filename):
        """Delete a file if it exists.

        :param filename: The name of the file.
        """
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

    def get_mimetype(self, filename):
        """Get the MIME type of a file.

        Will get the MIME type based on magic numbers inside the file's content (using
        libmagic), so the passed filename needs to actually exist and point to a
        readable file.

        :param filename: The name of the file.
        :return: The MIME type of the file.
        """
        return magic.from_file(filename, mime=True)

    def get_size(self, filename):
        """Get the size of a file.

        :param filename: The name of the file.
        :return: The size of the file in bytes.
        """
        return os.path.getsize(filename)

    def _get_size(self, filename):
        try:
            return self.get_size(filename)
        except FileNotFoundError:
            return 0

    def validate_size(self, filename, size, op="=="):
        """Validate the size of a file.

        :param filename: The name of the file.
        :param size: The size to compare the file with.
        :param op: (optional) The operator to use for comparison. See ``op`` in
            :func:`kadi.lib.utils.get_truth` for possible values.
        :raises KadiFilesizeMismatchError: If the validation failed.
        """
        filesize = self._get_size(filename)

        if not get_truth(filesize, op, size):
            msg = f"File size mismatch ({filesize} {op} {size})."
            raise KadiFilesizeMismatchError(msg)

    def get_checksum(self, filename):
        """Get the MD5 checksum of a file.

        :param filename: The name of the file.
        :return: The MD5 checksum as string in hex representation.
        """
        checksum = hashlib.md5()

        with open(filename, "rb") as file:
            buf = file.read(self.buffer_size)
            while buf:
                checksum.update(buf)
                buf = file.read(self.buffer_size)

        return checksum.hexdigest()

    def verify_checksum(self, filename, expected):
        """Verify the checksum of a file.

        :param filename: The name of the file.
        :param expected: The excepted checksum as string in hex representation.
        :raises KadiChecksumMismatchError: If the checksums did not match.
        """
        checksum = self.get_checksum(filename)

        if checksum != expected:
            msg = f"File checksum mismatch (expected: {expected}, actual: {checksum})."
            raise KadiChecksumMismatchError(msg)
