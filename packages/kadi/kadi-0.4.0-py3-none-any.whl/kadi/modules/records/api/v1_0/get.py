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
import json
from functools import partial

from flask import abort
from flask import current_app
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import strip
from kadi.lib.resources.api import get_resource_group_roles
from kadi.lib.resources.api import get_resource_user_roles
from kadi.lib.resources.utils import get_linked_resources
from kadi.lib.revisions.models import Revision
from kadi.lib.revisions.schemas import ObjectRevisionSchema
from kadi.lib.tasks.models import Task
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.core import search_records
from kadi.modules.records.extras import parse_extra_search_queries
from kadi.modules.records.files import download_file as _download_file
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.models import RecordLink
from kadi.modules.records.models import Upload
from kadi.modules.records.schemas import FileSchema
from kadi.modules.records.schemas import RecordLinkSchema
from kadi.modules.records.schemas import RecordSchema
from kadi.modules.records.schemas import UploadSchema


route = partial(bp.route, methods=["GET"])


@route("/records")
@login_required
@scopes_required("record.read")
@paginated(page_max=100)
@qparam("query", "", description="The search query.")
@qparam(
    "extras",
    "[]",
    parse=parse_extra_search_queries,
    description="A list of encoded dictionaries to specify the search within the extra"
    " metadata of a record.",
)
@qparam("sort", "_score", description="The order of the search results.")
@qparam("tag", [], multiple=True, description="Tags to filter the records with.")
@qparam(
    "type", [], multiple=True, description="Record types to filter the records with."
)
@qparam(
    "mimetype", [], multiple=True, description="MIME types to filter the records with."
)
@status(200, "Return a paginated list of records.")
def get_records(page, per_page, qparams):
    """Get all records or search and filter for specific records.

    See :func:`kadi.modules.records.core.search_records` for a more detailed explanation
    of the query parameters.
    """
    records, total_records = search_records(
        qparams["query"],
        extras=qparams["extras"],
        sort=qparams["sort"],
        tags=qparams["tag"],
        record_types=qparams["type"],
        mimetypes=qparams["mimetype"],
        page=page,
        per_page=per_page,
    )

    data = {
        "items": RecordSchema(many=True).dump(records),
        "_actions": {"new_record": url_for("api.new_record")},
        **create_pagination_data(
            total_records,
            page,
            per_page,
            "api.get_records",
            **{
                **qparams,
                "extras": json.dumps(qparams["extras"], separators=(",", ":")),
            },
        ),
    }

    return json_response(200, data)


@route("/records/<int:id>")
@permission_required("read", "record", "id")
@scopes_required("record.read")
@status(200, "Return the record.")
def get_record(id):
    """Get the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)
    return json_response(200, RecordSchema().dump(record))


@route("/records/identifier/<identifier:identifier>")
@login_required
@scopes_required("record.read")
@status(200, "Return the record.")
def get_record_by_identifier(identifier):
    """Get the record specified by the given *identifier*."""
    record = Record.query.filter_by(
        identifier=identifier, state="active"
    ).first_or_404()

    if not has_permission(current_user, "read", "record", object_id=record.id):
        abort(403)

    return json_response(200, RecordSchema().dump(record))


@route("/records/<int:id>/records")
@permission_required("read", "record", "id")
@scopes_required("record.read")
@paginated
@qparam(
    "direction",
    "to",
    description="The direction of the record links. ``to`` will return (outgoing)"
    " records linked to from the current record, while ``from`` will return (incoming)"
    " records that link to the current record.",
)
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the record links by their name.",
)
@qparam(
    "action",
    [],
    multiple=True,
    description="Further actions the current user needs permission to perform in the"
    " linked records.",
)
@status(
    200,
    "Return a paginated list of record links, sorted by creation date in descending"
    " order.",
)
def get_record_links(id, page, per_page, qparams):
    """Get the record links of the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    filter_query = (
        get_permitted_objects(current_user, "read", "record")
        .active()
        .with_entities(Record.id)
    )

    for action in qparams["action"]:
        filter_query = (
            get_permitted_objects(current_user, action, "record")
            .with_entities(Record.id)
            .intersect(filter_query)
        )

    # Records linked to from the current record.
    if qparams["direction"] == "to":
        record_links = record.links_to.filter(RecordLink.record_to_id.in_(filter_query))
    # Records that link to the current record.
    else:
        record_links = record.linked_from.filter(
            RecordLink.record_from_id.in_(filter_query)
        )

    record_links = (
        record_links.filter(RecordLink.name.ilike(f"%{qparams['filter']}%"))
        .order_by(RecordLink.created_at.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": RecordLinkSchema(many=True).dump(record_links.items),
        **create_pagination_data(
            record_links.total,
            page,
            per_page,
            "api.get_record_links",
            id=record.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/records/<int:record_id>/records/<int:link_id>")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the record link.")
def get_record_link(record_id, link_id):
    """Get a record link.

    Will return the (outgoing) record link specified by the given *link_id* from the
    record specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    record_link = RecordLink.query.get_or_404(link_id)

    if record.id != record_link.record_from_id:
        abort(404)

    if not has_permission(
        current_user, "read", "record", object_id=record_link.record_to_id
    ):
        abort(403)

    return json_response(200, RecordLinkSchema().dump(record_link))


@route("/records/<int:id>/collections")
@permission_required("read", "record", "id")
@scopes_required("record.read", "collection.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the collections by their title or identifier.",
)
@qparam(
    "action",
    [],
    multiple=True,
    description="Further actions the current user needs permission to perform in the"
    " linked collections.",
)
@status(
    200, "Return a paginated list of collections, sorted by title in ascending order."
)
def get_record_collections(id, page, per_page, qparams):
    """Get the collections the record specified by the given *id* is part of."""
    record = Record.query.get_active_or_404(id)

    paginated_collections = (
        get_linked_resources(Collection, record.collections, actions=qparams["action"])
        .filter(
            db.or_(
                Collection.title.ilike(f"%{qparams['filter']}%"),
                Collection.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .paginate(page, per_page, False)
    )

    data = {
        "items": CollectionSchema(many=True, linked_record=record).dump(
            paginated_collections.items
        ),
        **create_pagination_data(
            paginated_collections.total,
            page,
            per_page,
            "api.get_record_collections",
            id=record.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/records/<int:id>/roles/users")
@permission_required("read", "record", "id")
@scopes_required("record.read", "user.read")
@paginated
@qparam("exclude", [], multiple=True, type=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of user roles, sorted by role name and then by user ID in"
    " ascending order. The creator will always be listed first.",
)
def get_record_user_roles(id, page, per_page, qparams):
    """Get the user roles of the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    items, total = get_resource_user_roles(
        record, page=page, per_page=per_page, exclude=qparams["exclude"]
    )
    data = {
        "items": items,
        **create_pagination_data(
            total, page, per_page, "api.get_record_user_roles", id=record.id
        ),
    }

    return json_response(200, data)


@route("/records/<int:id>/roles/groups")
@permission_required("read", "record", "id")
@scopes_required("record.read", "group.read")
@paginated
# @qparam("exclude", [], multiple=True, type=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of group roles, sorted by role name and then by group ID"
    " in ascending order.",
)
def get_record_group_roles(id, page, per_page):
    """Get the group roles of the record specified by the given *id*.

    If a user can manage permissions in this record, all group roles are returned.
    However, groups that a user can normally not read include only a limited subset of
    attributes.
    """
    record = Record.query.get_active_or_404(id)

    items, total = get_resource_group_roles(record, page=page, per_page=per_page)
    data = {
        "items": items,
        **create_pagination_data(
            total, page, per_page, "api.get_record_group_roles", id=record.id
        ),
    }

    return json_response(200, data)


@route("/records/<int:id>/revisions")
@permission_required("read", "record", "id")
@scopes_required("record.read")
@paginated
@status(
    200,
    "Return a paginated list of record revisions, sorted by revision timestamp in"
    " descending order.",
)
def get_record_revisions(id, page, per_page):
    """Get the record revisions of the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    paginated_revisions = (
        record.revisions.join(Revision)
        .order_by(Revision.timestamp.desc())
        .paginate(page, per_page, False)
    )

    schema = ObjectRevisionSchema(
        many=True,
        schema=RecordSchema,
        api_endpoint="api.get_record_revision",
        view_endpoint="records.view_record_revision",
        endpoint_args={"record_id": record.id},
    )

    data = {
        "items": schema.dump(paginated_revisions.items),
        **create_pagination_data(
            paginated_revisions.total,
            page,
            per_page,
            "api.get_record_revisions",
            id=record.id,
        ),
    }

    return json_response(200, data)


@route("/records/<int:record_id>/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the record revision.")
def get_record_revision(record_id, revision_id):
    """Get a record revision.

    Will return the record revision specified by the given *revision_id* of the record
    specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    revision = Record._revision_class.query.get_or_404(revision_id)

    if record.id != revision.record_id:
        abort(404)

    schema = ObjectRevisionSchema(
        schema=RecordSchema,
        api_endpoint="api.get_record_revision",
        view_endpoint="records.view_record_revision",
        endpoint_args={"record_id": record.id},
    )

    return json_response(200, schema.dump(revision))


@route("/records/<int:id>/files")
@permission_required("read", "record", "id")
@scopes_required("record.read")
@paginated
@qparam("filter", "", parse=strip, description="A query to filter the files by name.")
@status(
    200,
    "Return a paginated list of files, sorted by last modification date in descending"
    " order.",
)
def get_files(id, page, per_page, qparams):
    """Get the files of the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    paginated_files = (
        record.active_files.filter(File.name.ilike(f"%{qparams['filter']}%"))
        .order_by(File.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": FileSchema(many=True).dump(paginated_files.items),
        "_actions": {"new_upload": url_for("api.new_upload", id=record.id)},
        **create_pagination_data(
            paginated_files.total,
            page,
            per_page,
            "api.get_files",
            id=record.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/records/<int:record_id>/files/<uuid:file_id>")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the file.")
def get_file(record_id, file_id):
    """Get a file of a record.

    Will return the file specified by the given *file_id* of the record specified by the
    given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    return json_response(200, FileSchema().dump(file))


@route("/records/<int:record_id>/files/name/<path:filename>")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the file.")
def get_file_by_name(record_id, filename):
    """Get a file of a record by its name.

    Will return the file specified by the given *filename* of the record specified by
    the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.filter_by(name=filename, state="active").first_or_404()

    if file.record != record:
        abort(404)

    return json_response(200, FileSchema().dump(file))


@route("/records/<int:record_id>/files/<uuid:file_id>/download")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the file as attachment.")
def download_file(record_id, file_id):
    """Download a file.

    Will return the file specified by the given *file_id* of the record specified by the
    given *record_id* as attachment.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    response = _download_file(file)
    if response is not None:
        return response

    abort(404)


@route("/records/<int:id>/files/revisions")
@permission_required("read", "record", "id")
@scopes_required("record.read")
@paginated
@status(
    200,
    "Return a paginated list of file revisions, sorted by revision timestamp in"
    " descending order.",
)
def get_file_revisions(id, page, per_page):
    """Get the file revisions of the record specified by the given *id*."""
    record = Record.query.get_active_or_404(id)

    paginated_revisions = (
        File._revision_class.query.join(File)
        .join(Revision)
        .filter(File.record_id == record.id)
        .order_by(Revision.timestamp.desc())
        .paginate(page, per_page, False)
    )

    schema = ObjectRevisionSchema(
        many=True,
        schema=FileSchema,
        api_endpoint="api.get_file_revision",
        view_endpoint="records.view_file_revision",
        endpoint_args={"record_id": record.id},
    )

    data = {
        "items": schema.dump(paginated_revisions.items),
        **create_pagination_data(
            paginated_revisions.total,
            page,
            per_page,
            "api.get_file_revisions",
            id=record.id,
        ),
    }

    return json_response(200, data)


@route("/records/<int:record_id>/files/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
@scopes_required("record.read")
@status(200, "Return the file revision.")
def get_file_revision(record_id, revision_id):
    """Get a file revision.

    Will return the file revision specified by the given *revision_id* of the record
    specified by the given *record_id*.
    """
    record = Record.query.get_active_or_404(record_id)
    revision = File._revision_class.query.get_or_404(revision_id)

    if record.id != revision.file.record_id:
        abort(404)

    view_file_url = None
    file = File.query.get(revision.file.id)

    if file.state == "active":
        view_file_url = url_for(
            "records.view_file", record_id=record.id, file_id=file.id, _external=True
        )

    schema = ObjectRevisionSchema(
        schema=FileSchema,
        api_endpoint="api.get_file_revision",
        view_endpoint="records.view_file_revision",
        endpoint_args={"record_id": record.id},
        view_object_url=view_file_url,
    )

    return json_response(200, schema.dump(revision))


@route("/records/<int:id>/uploads")
@permission_required("update", "record", "id")
@scopes_required("record.update")
@status(
    200,
    "Return the uploads, sorted by creation date in ascending order. Additionally, the"
    " required size for uploading file chunks is returned as the ``_meta.chunk_size``"
    " property.",
)
def get_uploads(id):
    """Get all uploads of the record specified by the given *id*.

    Only uploads owned by the current user will be returned.
    """
    record = Record.query.get_active_or_404(id)
    uploads = current_user.uploads.filter(
        Upload.record_id == record.id, Upload.state != "inactive"
    ).order_by(Upload.created_at)

    data = {
        "items": UploadSchema(many=True).dump(uploads),
        "_actions": {"new_upload": url_for("api.new_upload", id=record.id)},
        "_meta": {"chunk_size": current_app.config["UPLOAD_CHUNK_SIZE"]},
    }

    return json_response(200, data)


@route("/records/<int:record_id>/uploads/<uuid:upload_id>")
@permission_required("update", "record", "record_id")
@scopes_required("record.update")
@status(
    200,
    "Return the upload and additional metadata in the ``_meta`` property, depending on"
    " the state of the upload.",
)
def get_upload_status(record_id, upload_id):
    """Get the status of an upload.

    Will return the status of the upload specified by the given *upload_id* of the
    record specified by the given *record_id*. Only the status of uploads owned by the
    current user can be queried.
    """
    record = Record.query.get_active_or_404(record_id)
    upload = Upload.query.get_or_404(upload_id)

    if upload.record != record or upload.creator != current_user:
        abort(404)

    data = UploadSchema().dump(upload)

    if upload.state != "active":
        task = Task.query.filter(
            Task.name == "kadi.records.merge_chunks",
            Task.arguments["args"][0].astext == str(upload.id),
        ).first()

        # If no task exists, the upload never got finished.
        if task is None:
            abort(404)

        if task.state in ["pending", "running"]:
            data["_meta"] = {"progress": task.progress}
        elif task.state == "failure":
            data["_meta"] = {"error": task.result["error"]}
        elif task.state == "success":
            file = File.query.get(task.result["file"])
            data["_meta"] = {"file": FileSchema().dump(file)}

    return json_response(200, data)
