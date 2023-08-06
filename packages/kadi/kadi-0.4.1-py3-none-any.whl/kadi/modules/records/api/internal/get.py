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
from functools import partial

from flask import abort
from flask import current_app
from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.web import download_string
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.files import (
    download_temporary_file as _download_temporary_file,
)
from kadi.modules.records.files import get_archive_contents
from kadi.modules.records.files import get_preview_type
from kadi.modules.records.files import get_text_contents
from kadi.modules.records.files import preview_file as _preview_file
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import TemporaryFile
from kadi.modules.records.utils import get_export_data


route = partial(bp.route, methods=["GET"])


@route("/records/<int:id>/export/<export_type>", v=None)
@permission_required("read", "record", "id")
@internal_endpoint
def download_record_export(id, export_type):
    """Export and download a record in a specific format.

    Currently only ``json`` is supported as export type.
    """
    record = Record.query.get_active_or_404(id)

    if export_type == "json":
        filename = record.identifier + ".json"
        mimetype = "application/json"
    else:
        abort(404)

    data = get_export_data(record, export_type)
    return download_string(data, filename, mimetype)


@route("/records/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
@qparam("exclude", [], multiple=True, type=int)
@qparam("action", ["read"], multiple=True)
def select_records(qparams):
    """Search records in dynamic selections.

    See :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    return get_selected_resources(
        Record,
        page=qparams["page"],
        term=qparams["term"],
        exclude=qparams["exclude"],
        actions=qparams["action"],
    )


@route("/records/select/types", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
def select_record_types(qparams):
    """Search record types in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Only the types of
    records the current user has read permission for are returned.
    """
    record_types = (
        get_permitted_objects(current_user, "read", "record")
        .filter(
            Record.state == "active",
            Record.type != None,
            Record.type.like(f"%{qparams['term']}%"),
        )
        .with_entities(Record.type)
        .distinct()
        .order_by(Record.type)
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": record_types.has_next}}
    for record_type in record_types.items:
        data["results"].append({"id": record_type[0], "text": record_type[0]})

    return json_response(200, data)


@route("/records/<int:record_id>/files/<uuid:file_id>/preview", v=None)
@permission_required("read", "record", "record_id")
@internal_endpoint
def get_file_preview(record_id, file_id):
    """Get the preview data of a file.

    The actual preview data may either consist of a URL or the preview data itself,
    depending on the preview type. In the first case, a browser may be able to directly
    preview the file using the returned URL.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    preview_type = get_preview_type(file)
    if preview_type is None:
        abort(404)

    data = {"type": preview_type}

    if preview_type in ["image", "pdf"]:
        if file.size > current_app.config["PREVIEW_MAX_SIZE"]:
            abort(404)

        data["data"] = url_for("api.preview_file", record_id=record.id, file_id=file.id)
    elif preview_type == "archive":
        data["data"] = get_archive_contents(file)
    else:
        # We found textual data as a fallback.
        data["data"] = get_text_contents(file, encoding=preview_type.split(";")[1])

    return json_response(200, data)


@route("/records/<int:record_id>/files/<uuid:file_id>/preview/file", v=None)
@permission_required("read", "record", "record_id")
@internal_endpoint
def preview_file(record_id, file_id):
    """Download a file for direct preview in the browser."""
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record or file.size > current_app.config["PREVIEW_MAX_SIZE"]:
        abort(404)

    preview_type = get_preview_type(file, use_fallback=False)
    if preview_type in ["image", "pdf"]:
        response = _preview_file(file)

        if response is not None:
            return response

    abort(404)


@route("/records/<int:record_id>/temporary_files/<uuid:temporary_file_id>", v=None)
@permission_required("read", "record", "record_id")
@internal_endpoint
def download_temporary_file(record_id, temporary_file_id):
    """Download a temporary file."""
    record = Record.query.get_active_or_404(record_id)
    temporary_file = TemporaryFile.query.get_active_or_404(temporary_file_id)

    if temporary_file.record != record:
        abort(404)

    response = _download_temporary_file(temporary_file)
    if response is not None:
        return response

    abort(404)
