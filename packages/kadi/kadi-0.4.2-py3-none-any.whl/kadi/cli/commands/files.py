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
import glob
import itertools
import os
import re
import shutil

import click
from flask import current_app

from kadi.cli.main import kadi
from kadi.cli.utils import check_env
from kadi.cli.utils import echo
from kadi.cli.utils import success
from kadi.cli.utils import warning
from kadi.ext.db import db
from kadi.lib.storage.local import LocalStorage
from kadi.lib.tasks.models import Task
from kadi.modules.records.files import remove_files
from kadi.modules.records.files import remove_temporary_files
from kadi.modules.records.files import remove_uploads
from kadi.modules.records.models import File
from kadi.modules.records.models import TemporaryFile
from kadi.modules.records.models import Upload


@kadi.group()
def files():
    """Utility commands for local file management."""


def _remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        # Normally there should be only folders, but we check for files anyway just in
        # case.
        os.remove(path)


@files.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def clean(i_am_sure):
    """Remove all files in the configured local storage paths.

    Besides the record files stored in STORAGE_PATH, this command will also delete all
    general user uploads stored in MISC_UPLOADS_PATH.

    Should only be run while the application and celery are not running.
    """
    storage_path = current_app.config["STORAGE_PATH"]
    misc_uploads_path = current_app.config["MISC_UPLOADS_PATH"]

    if not i_am_sure:
        warning(
            f"This will remove all data in '{storage_path}' and '{misc_uploads_path}'."
            " If you are sure you want to do this, use the flag --i-am-sure."
        )
        return

    for item in os.listdir(storage_path):
        _remove_path(os.path.join(storage_path, item))

    for item in os.listdir(misc_uploads_path):
        _remove_path(os.path.join(misc_uploads_path, item))

    success("Storage cleaned successfully.")


def _collect_files():
    """Collect all information of files stored in STORAGE_PATH and the database.

    Collects all local files, temporary files, uploads and chunks from the file system
    and database. The information will be returned in the following form:

    "<obj_uuid>": {
        "obj": <database_object>,
        "path": "<storage_path>",
        "chunks": {
            "<chunk_index>": {
                "obj": <chunk_object>,
                "path": "<storage_path>",
            }
        },
    }
    """
    files = {}

    # Collect all information from the file system.
    filename_re = re.compile(
        "^([0-9a-f]{{2}}{sep}[0-9a-f]{{2}}{sep}[0-9a-f]{{2}}{sep}[0-9a-f]{{2}}"
        "-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})(-[0-9]+)?$".format(
            sep=os.sep
        )
    )

    storage_path = current_app.config["STORAGE_PATH"]
    search_path = os.path.join(storage_path, "**", "*")

    for item in glob.iglob(search_path, recursive=True):
        if os.path.isfile(item):
            filename = os.path.relpath(item, storage_path)

            match = filename_re.match(filename)
            # This should normally not happen, but we check for it just in case.
            if match is None:
                warning(f"Ignoring unexpected data '{item}'.")
                continue

            obj_uuid = match.group(1).replace(os.sep, "")

            if obj_uuid not in files:
                files[obj_uuid] = {"obj": None, "path": None, "chunks": {}}

            # Matched a file or upload.
            if match.group(2) is None:
                files[obj_uuid]["path"] = item

            # Matched a chunk.
            else:
                index = int(match.group(2)[1:])
                files[obj_uuid]["chunks"][index] = {"obj": None, "path": item}

    # Add all information from the database.
    for obj in itertools.chain(
        File.query.filter_by(storage_type="local"), TemporaryFile.query, Upload.query
    ):
        obj_uuid = str(obj.id)

        if obj_uuid not in files:
            files[obj_uuid] = {"obj": None, "path": None, "chunks": {}}

        files[obj_uuid]["obj"] = obj

        if isinstance(obj, Upload):
            for chunk in obj.chunks:
                if chunk.index not in files[obj_uuid]["chunks"]:
                    files[obj_uuid]["chunks"][chunk.index] = {"obj": None, "path": None}

                files[obj_uuid]["chunks"][chunk.index]["obj"] = chunk

    return files


def _resolve_inconsistency(data, resolve=False, verbose=True, msg=None):
    if verbose and msg is not None:
        echo(msg)

    if resolve:
        if isinstance(data, str):
            if verbose:
                echo("Deleting data...")

            storage = LocalStorage()
            storage.delete(data)
            storage.remove_empty_parent_dirs(data, num_dirs=3)
        else:
            if verbose:
                echo("Deleting database object and corresponding data...")

            if isinstance(data, File):
                remove_files(data)

            elif isinstance(data, TemporaryFile):
                remove_temporary_files(data)

            elif isinstance(data, Upload):
                remove_uploads(data)


@files.command()
@click.option(
    "-r",
    "--resolve",
    is_flag=True,
    help="Resolve all inconsistencies by removing all inconsistent data from the"
    " database and/or the file storage.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Print information about any inconsistent data.",
)
def check(resolve, verbose):
    """Check the configured local storage path for inconsistencies.

    Each file that matches the pattern of locally stored files in STORAGE_PATH will be
    checked for existence in the database, while each local file, temporary file, upload
    or chunk from the database will be checked for the corresponding data in the file
    storage, taking into account the different states each object can be in.

    Should only be run while the application and Celery are not running.
    """
    files = _collect_files()
    num_inconsistencies = 0

    for obj_uuid, file_dict in files.items():
        obj = file_dict["obj"]
        file_path = file_dict["path"]

        # The file exists in the database.
        if obj is not None:
            if isinstance(obj, File):
                file = obj

                # If an active file exists in storage, we validate its integrity by
                # verifying its size and checksum. Otherwise there is an inconsistency.
                if file.state == "active":
                    if file_path is not None:
                        try:
                            storage = LocalStorage()
                            storage.validate_size(file_path, file.size)
                            storage.verify_checksum(file_path, file.checksum)
                        except Exception:
                            num_inconsistencies += 1
                            _resolve_inconsistency(
                                file,
                                resolve=resolve,
                                verbose=verbose,
                                msg="> Mismatched size or checksum for active file"
                                f" object with ID '{obj_uuid}' and path '{file_path}'.",
                            )
                    else:
                        num_inconsistencies += 1
                        _resolve_inconsistency(
                            file,
                            resolve=resolve,
                            verbose=verbose,
                            msg="> Found orphaned active file object with ID"
                            f" '{obj_uuid}'.",
                        )

                # Inactive files will be handled by the periodic cleanup task
                # eventually.
                elif file.state == "inactive":
                    pass

                # Deleted file objects should not have any data associated with them
                # anymore.
                elif file.state == "deleted" and file_path is not None:
                    num_inconsistencies += 1
                    _resolve_inconsistency(
                        file,
                        resolve=resolve,
                        verbose=verbose,
                        msg=f"> Found deleted file object with ID '{file.id}' and"
                        f" path '{file_path}'.",
                    )

            elif isinstance(obj, TemporaryFile):
                temporary_file = obj

                # Active temporary files should exist in storage.
                if temporary_file.state == "active" and file_path is None:
                    num_inconsistencies += 1
                    _resolve_inconsistency(
                        temporary_file,
                        resolve=resolve,
                        verbose=verbose,
                        msg="> Found orphaned temporary file object with ID"
                        f" '{obj_uuid}'.",
                    )

                # Inactive temporary files will be handled by the periodic cleanup task
                # eventually.
                elif temporary_file.state == "inactive":
                    pass

            elif isinstance(obj, Upload):
                upload = obj

                # Inconsistent chunks of active uploads are already handled below. The
                # chunks themselves are not validated, since this will already happen
                # once an upload is finished anyway.
                if upload.state == "active":
                    pass

                # Inactive uploads will be handled by the periodic cleanup task
                # eventually.
                elif upload.state == "inactive":
                    pass

                # If an upload is still processing, check if the task is still pending.
                # In case it is, it is up to the task to decide if the processing should
                # complete or not, otherwise the task may have been canceled forcefully.
                elif upload.state == "processing":
                    task = Task.query.filter(
                        Task.name == "kadi.records.merge_chunks",
                        Task.arguments["args"][0].astext == obj_uuid,
                    ).first()

                    if task.state != "pending":
                        num_inconsistencies += 1
                        _resolve_inconsistency(
                            upload,
                            resolve=resolve,
                            verbose=verbose,
                            msg=f"> Found processing upload object with ID '{obj_uuid}'"
                            " and non-pending task.",
                        )

                        if resolve:
                            # Attempt to revoke the task as well.
                            task.revoke()

        # The file only exists in the file storage.
        elif file_path is not None:
            num_inconsistencies += 1
            _resolve_inconsistency(
                file_path,
                resolve=resolve,
                verbose=verbose,
                msg=f"> Found orphaned file data with path '{file_path}'.",
            )

        # We always check for any orphaned chunks, no matter the state of the upload.
        # This also handles the case of chunks of an upload only existing in the file
        # storage.
        for chunk_index, chunk_dict in file_dict["chunks"].items():
            chunk = chunk_dict["obj"]
            chunk_path = chunk_dict["path"]

            # Found chunk data in the file system without corresponding chunk object in
            # the database.
            if chunk is None and chunk_path is not None:
                num_inconsistencies += 1
                # This will still work even if the chunk data was deleted in a previous
                # step already.
                _resolve_inconsistency(
                    chunk_path,
                    resolve=resolve,
                    verbose=verbose,
                    msg=f"> Found orphaned chunk data with path '{chunk_path}'.",
                )

            # Found an active chunk object in the database without corresponding chunk
            # data in the file system.
            elif chunk is not None and chunk.state == "active" and chunk_path is None:
                num_inconsistencies += 1
                if verbose:
                    echo(
                        f"> Found orphaned chunk object for file with ID '{obj_uuid}'"
                        f" with index '{chunk_index}'."
                    )

                if resolve:
                    if verbose:
                        echo("Deleting chunk object...")

                    # This still works even if the chunk object was deleted in a
                    # previous step already.
                    db.session.delete(chunk)

        if resolve:
            db.session.commit()

    success("Files checked successfully.")

    if not resolve:
        msg = (
            f"Found {num_inconsistencies}"
            f" {'inconsistencies' if num_inconsistencies != 1 else 'inconsistency'}."
        )

        if num_inconsistencies > 0:
            warning(msg)

            if verbose:
                echo("Rerun with -r to automatically resolve all inconsistencies.")
            else:
                echo(
                    "Rerun with -v to get more information or with -r to automatically"
                    " resolve all inconsistencies."
                )
        else:
            echo(msg)
    else:
        success("Inconsistencies resolved successfully.")
