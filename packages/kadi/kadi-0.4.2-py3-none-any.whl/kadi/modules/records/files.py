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
import os
from contextlib import contextmanager

import chardet
from flask import current_app
from flask import send_file
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .models import File
from .models import TemporaryFile
from .models import Upload
from .uploads import delete_upload
from .uploads import remove_uploads
from kadi.ext.db import db
from kadi.lib.archives import create_archive
from kadi.lib.archives import get_archive_contents as _get_archive_contents
from kadi.lib.db import update_object
from kadi.lib.revisions.core import create_revision
from kadi.lib.storage.core import create_filepath
from kadi.lib.storage.core import create_storage
from kadi.lib.storage.local import LocalStorage
from kadi.lib.utils import is_iterable


def update_file(file, **kwargs):
    r"""Update an existing file.

    :param file: The file to update.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the file was updated successfully, ``False`` otherwise.
    """
    if file.state != "active" or file.record.state != "active":
        return False

    update_object(file, **kwargs)

    # Update the record's timestamp as well.
    if db.session.is_modified(file):
        file.record.update_timestamp()

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    create_revision(file)

    return True


def delete_file(file, revision_user=None):
    """Delete an existing file.

    This will mark the file for deletion, i.e. the files's state will be set to
    ``"inactive"``.

    :param file: The file to delete.
    :param revision_user: (optional) The user that triggered the file deletion revision.
        Defaults to the current user.
    """
    file.state = "inactive"

    # Update the record's timestamp as well.
    if db.session.is_modified(file):
        file.record.update_timestamp()

    revision_user = revision_user if revision_user is not None else current_user
    create_revision(file, user=revision_user)

    # Check if there are any uploads attached to the file and mark them for deletion as
    # well.
    uploads = Upload.query.filter(Upload.file_id == file.id)
    for upload in uploads:
        delete_upload(upload)


def remove_files(files, delete_from_db=True):
    """Remove multiple files from storage.

    Note that this function may issue one or more database commits.

    :param files: A single :class:`.File` or an iterable of files.
    :param delete_from_db: (optional) A flag indicating whether the file should be
        deleted from the database as well, instead of just doing a soft deletion (i.e.
        setting the file's state to ``"deleted"``).
    """
    if not is_iterable(files):
        files = [files]

    for file in files:
        file.state = "inactive"
        db.session.commit()

        storage_type = file.storage_type
        filepath = create_filepath(str(file.id), storage_type=storage_type)

        storage = create_storage(storage_type=storage_type)
        storage.delete(filepath)

        if storage_type == "local":
            # Check if there are any uploads attached to the file and remove them as
            # well.
            uploads = Upload.query.filter(Upload.file_id == file.id)
            remove_uploads(uploads)

            storage.remove_empty_parent_dirs(filepath, num_dirs=3)

        if delete_from_db:
            file.revisions.delete(synchronize_session="fetch")
            db.session.delete(file)
        else:
            file.state = "deleted"

        db.session.commit()


@contextmanager
def open_file(file, mode="rb", encoding=None):
    """Context manager that yields an open file.

    Note that files should generally be treated as read-only, as changing them directly
    will not be reflected in the database.

    **Example:**

    .. code-block:: python3

        with open_file(file) as file_object:
            pass

    :param file: The :class:`.File` to open.
    :param mode: (optional) The mode to open the file with.
    """
    storage_type = file.storage_type

    filepath = create_filepath(str(file.id), storage_type=storage_type)
    storage = create_storage(storage_type=storage_type)

    file_object = storage.open(filepath, mode=mode, encoding=encoding)

    try:
        yield file_object
    finally:
        storage.close(file_object)


def download_file(file):
    """Send a file to a client as attachment for download.

    :param file: The :class:`.File` to download.
    :return: The response object or ``None`` if the given file could not be found or has
        an incompatible storage type.
    """
    if file.storage_type == "local":
        filepath = create_filepath(str(file.id), storage_type=file.storage_type)

        if not os.path.isfile(filepath):
            return None

        return send_file(
            filepath,
            mimetype=file.mimetype,
            attachment_filename=file.name,
            as_attachment=True,
        )

    return None


def preview_file(file):
    """Send a file to a client.

    Mostly useful to directly preview files using the browser. Note that this can
    potentially pose a security risk, so this should only be used for files that are
    safe for displaying. Uses the content-based MIME type of the file to set the content
    type of the response (see :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to send to the client.
    :return: The response object or ``None`` if the given file could not be found has an
        incompatible storage type.
    """

    if file.storage_type == "local":
        filepath = create_filepath(str(file.id), storage_type=file.storage_type)

        if not os.path.isfile(filepath):
            return None

        return send_file(filepath, mimetype=file.magic_mimetype)

    return None


def get_preview_type(file, use_fallback=True):
    """Get the preview type of a file.

    Compares the MIME types specified in ``PREVIEW_MIMETYPES`` in the application's
    configuration with the content-based MIME type of the file to get the corresponding
    preview type if one exists (see :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to get the preview type of.
    :param use_fallback: (optional) Flag indicating whether the file should be checked
        for textual data as fallback by trying to detect its encoding.
    :return: The preview type or ``None`` if no preview type exists. In case the file
        was detected to have textual content, the preview type will also include the
        encoding in the form of ``"text;<encoding>"``.
    """
    preview_mimetypes = current_app.config["PREVIEW_MIMETYPES"]

    for preview_type, mimetypes in preview_mimetypes.items():
        if file.magic_mimetype in mimetypes:
            return preview_type

    if use_fallback:
        with open_file(file, mode="rb") as f:
            # Chardet can be pretty slow, so we try to limit the bytes read.
            encoding = chardet.detect(f.read(16384))["encoding"]

        if encoding is not None:
            try:
                # If an encoding was found, we try to actually read something from the
                # file using that encoding.
                with open_file(file, mode="r", encoding=encoding) as f:
                    f.read(1)
                    return "text;" + encoding
            except UnicodeDecodeError:
                pass

    return None


def get_archive_contents(file):
    """Get information about the contents contained in an archive.

    Uses :func:`kadi.lib.archives.get_archive_contents`. Also uses the content-based
    MIME type of the file to specify the type of archive (see
    :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to get the preview type of.
    :return: The list of archive contents or ``None`` if the given file has an
        incompatible storage type.
    """
    if file.storage_type == "local":
        filepath = create_filepath(str(file.id), storage_type=file.storage_type)
        return _get_archive_contents(filepath, file.magic_mimetype)

    return None


def get_text_contents(file, length=16384, encoding=None):
    """Get the text contents of a file if possible.

    :param file: The :class:`.File` to get the preview type of.
    :param length: (optional) The number of characters to use for detecting the encoding
        and for the result.
    :param encoding: (optional) The encoding of the file. Defaults to ``"utf-8"``.
    :return: The truncated text contents or ``None`` if the file did not contain text or
        the encoding was not valid.
    """
    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            text = f.read(length)
            return text + " ..." if len(text) == length else text
    except UnicodeDecodeError:
        pass

    return None


def package_files(record, creator, task=None):
    """Package multiple local files of a record together in a ZIP archive.

    Note that this function may issue one or more database commits.

    Uses :func:`kadi.lib.archives.create_archive`.

    :param record: The record the files belong to.
    :param creator: The user that will be set as the creator of the archive.
    :param task: (optional) A :class:`.Task` object that can be provided if this
        function is executed in a task.
    :return: The archive as a :class:`TemporaryFile` object or ``None`` if the archive
        was not packaged successfully.
    """
    files = record.active_files.filter(File.storage_type == "local")
    size = files.with_entities(db.func.sum(File.size)).scalar() or 0

    archive = TemporaryFile.create(
        record=record, creator=creator, name=f"{record.identifier}.zip", size=size
    )
    db.session.commit()

    filepath = create_filepath(str(archive.id))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    entries = [
        {"path": create_filepath(str(file.id)), "name": file.name, "size": file.size}
        for file in files
    ]

    def callback(count, current_size):
        if task:
            if task.is_revoked:
                return False

            task.update_progress(current_size / size * 100)
            db.session.commit()

        return True

    if create_archive(filepath, entries, callback):
        archive.state = "active"
        db.session.commit()
        return archive

    return None


def download_temporary_file(temporary_file):
    """Send a temporary file to a client as attachment for download.

    :param temporary_file: The :class:`.TemporaryFile` to download.
    :return: The response object or ``None`` if the given temporary file could not be
        found.
    """
    filepath = create_filepath(str(temporary_file.id))

    if not os.path.isfile(filepath):
        return None

    return send_file(
        filepath,
        mimetype=temporary_file.mimetype,
        attachment_filename=temporary_file.name,
        as_attachment=True,
    )


def remove_temporary_files(temporary_files):
    """Remove multiple temporary files from storage.

    Note that this function may issue one or more database commits.

    :param temporary_files: A single :class:`.TemporaryFile` or an iterable of temporary
        files.
    """
    if not is_iterable(temporary_files):
        temporary_files = [temporary_files]

    for temporary_file in temporary_files:
        temporary_file.state = "inactive"
        db.session.commit()

        storage = LocalStorage()
        filepath = create_filepath(str(temporary_file.id))

        storage.delete(filepath)
        storage.remove_empty_parent_dirs(filepath, num_dirs=3)

        db.session.delete(temporary_file)
        db.session.commit()
