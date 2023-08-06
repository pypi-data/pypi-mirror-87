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

from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

from .blueprint import bp
from .core import create_record
from .core import delete_record as _delete_record
from .core import search_records
from .core import update_record
from .extras import parse_extra_formdata
from .extras import parse_extra_search_queries
from .files import delete_file as _delete_file
from .files import update_file
from .forms import AddPermissionsForm
from .forms import EditFileForm
from .forms import EditRecordForm
from .forms import LinkCollectionsForm
from .forms import LinkRecordForm
from .forms import NewRecordForm
from .models import File
from .models import Record
from .models import RecordLink
from .tasks import start_publish_record_task
from .utils import get_export_data
from kadi.ext.db import db
from kadi.lib.forms import field_to_dict
from kadi.lib.publications import get_publication_providers
from kadi.lib.resources.views import add_links
from kadi.lib.resources.views import add_roles
from kadi.lib.resources.views import copy_roles
from kadi.lib.tags.models import Tag
from kadi.lib.tasks.models import Task
from kadi.lib.utils import create_pagination
from kadi.lib.utils import find_dict_in_list
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.templates.models import Template


@bp.route("")
@login_required
@paginated(page_max=100)
@qparam("query", "")
@qparam("sort", "_score")
@qparam("tag", [], multiple=True)
@qparam("tag_limit", 25, type=int)
@qparam("type", [], multiple=True)
@qparam("type_limit", 25, type=int)
@qparam("mimetype", [], multiple=True)
@qparam("mimetype_limit", 25, type=int)
@qparam("extras", "[]", parse=parse_extra_search_queries)
def records(page, per_page, qparams):
    """Record overview page.

    Allows users to search and filter for records or create new ones.
    """
    records_query = get_permitted_objects(current_user, "read", "record").active()

    search_results, total_records = search_records(
        qparams["query"],
        extras=qparams["extras"],
        sort=qparams["sort"],
        tags=qparams["tag"],
        record_types=qparams["type"],
        mimetypes=qparams["mimetype"],
        page=page,
        per_page=per_page,
        records_query=records_query,
        highlight=True,
    )
    pagination = create_pagination(total_records, page, per_page)

    tags = (
        records_query.join(Record.tags)
        .group_by(Tag.name)
        .with_entities(Tag.name, db.func.count(Tag.name).label("count"))
        .order_by(db.desc("count"))
    )

    total_tags = tags.count()

    tag_limit = qparams["tag_limit"]
    if tag_limit > 0:
        tags = tags.limit(tag_limit)
    else:
        qparams["tag_limit"] = 0

    tags = tags.all()

    record_types = (
        records_query.filter(Record.type != None)
        .group_by(Record.type)
        .with_entities(Record.type, db.func.count(Record.type).label("count"))
        .order_by(db.desc("count"))
    )

    total_record_types = record_types.count()

    record_type_limit = qparams["type_limit"]
    if record_type_limit > 0:
        record_types = record_types.limit(record_type_limit)
    else:
        qparams["type_limit"] = 0

    record_types = record_types.all()

    mimetypes = (
        records_query.join(Record.files)
        .filter(File.state == "active")
        .group_by(File.mimetype)
        .with_entities(File.mimetype, db.func.count(File.mimetype).label("count"))
        .order_by(db.desc("count"))
    )

    total_mimetypes = mimetypes.count()

    mimetype_limit = qparams["mimetype_limit"]
    if mimetype_limit > 0:
        mimetypes = mimetypes.limit(mimetype_limit)
    else:
        qparams["mimetype_limit"] = 0

    mimetypes = mimetypes.all()

    query_params = {
        **qparams,
        "page": page,
        "per_page": per_page,
        "extras": json.dumps(qparams["extras"], separators=(",", ":")),
    }

    return render_template(
        "records/records.html",
        title=_("Records"),
        records=search_results,
        total_records=total_records,
        mimetypes=mimetypes,
        total_mimetypes=total_mimetypes,
        tags=tags,
        total_tags=total_tags,
        record_types=record_types,
        total_record_types=total_record_types,
        pagination=pagination,
        query_params=query_params,
        js_resources={
            "new_record_endpoint": url_for("records.new_record"),
            "extras_search_enabled": bool(qparams["extras"]),
            "per_page": per_page,
        },
    )


@bp.route("/new", methods=["GET", "POST"])
@permission_required("create", "record", None)
@qparam("collection", None, type=int)
@qparam("record", None, type=int)
@qparam("template", None, type=int)
def new_record(qparams):
    """Page to create a new record."""
    copied_record = None
    linked_collection = None
    record_template = None
    extra_metadata = []

    if request.method == "GET":
        # Directly link a record with a collection.
        if qparams["collection"] is not None:
            linked_collection = Collection.query.get(qparams["collection"])

        # Copy a record's metadata.
        if qparams["record"] is not None:
            copied_record = Record.query.get(qparams["record"])
            if copied_record is not None and has_permission(
                current_user, "read", "record", copied_record.id
            ):
                extra_metadata = copied_record.extras

        # Use a record template.
        if qparams["template"] is not None:
            record_template = Template.query.get(qparams["template"])
            if (
                record_template is not None
                and record_template.type == "record"
                and has_permission(current_user, "read", "template", record_template.id)
            ):
                extra_metadata = record_template.data.get("extras", [])

    form = NewRecordForm(
        record=copied_record, collection=linked_collection, template=record_template
    )

    if request.method == "POST":
        parsed_extras = parse_extra_formdata()
        extra_metadata = parsed_extras.formdata

        if form.validate() and parsed_extras.is_valid:
            record = create_record(
                identifier=form.identifier.data,
                title=form.title.data,
                type=form.type.data,
                description=form.description.data,
                license=form.license.data,
                visibility=form.visibility.data,
                extras=parsed_extras.values,
                tags=form.tags.data,
            )

            if record:
                add_links(Collection, record.collections, form.linked_collections.data)
                copy_roles(record, form.copy_permission.data)
                db.session.commit()

                flash(_("Record created successfully."), "success")
                return redirect(url_for("records.add_files", id=record.id))

        flash(_("Error creating record."), "danger")

    return render_template(
        "records/new_record.html",
        title=_("New record"),
        form=form,
        js_resources={
            "extras": extra_metadata,
            "title_field": field_to_dict(form.title),
        },
    )


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@permission_required("update", "record", "id")
def edit_record(id):
    """Page to edit an existing record."""
    record = Record.query.get_active_or_404(id)
    form = EditRecordForm(record)
    extra_metadata = record.extras

    if request.method == "POST":
        parsed_extras = parse_extra_formdata()
        extra_metadata = parsed_extras.formdata

        if form.validate() and parsed_extras.is_valid:
            if update_record(
                record,
                identifier=form.identifier.data,
                title=form.title.data,
                type=form.type.data,
                description=form.description.data,
                license=form.license.data,
                visibility=form.visibility.data,
                extras=parsed_extras.values,
                tags=form.tags.data,
            ):
                db.session.commit()

                flash(_("Changes saved successfully."), "success")
                return redirect(url_for("records.view_record", id=record.id))

        flash(_("Error editing record."), "danger")

    return render_template(
        "records/edit_record.html",
        title=_("Edit"),
        form=form,
        record=record,
        js_resources={
            "extras": extra_metadata,
            "title_field": field_to_dict(form.title),
        },
    )


@bp.route("/<int:id>")
@permission_required("read", "record", "id")
def view_record(id):
    """Page to view a record."""
    record = Record.query.get_active_or_404(id)
    return render_template(
        "records/view_record.html",
        record=record,
        publication_providers=get_publication_providers(),
        js_resources={
            "title": record.title,
            "identifier": record.identifier,
            "extras": record.extras,
            "download_files_endpoint": url_for(
                "api.download_record_files", id=record.id
            ),
            "get_files_endpoint": url_for(
                "api.get_files", id=record.id, _internal=True
            ),
            "new_template_endpoint": url_for("api.new_template"),
        },
    )


@bp.route("/<int:id>/export/<export_type>")
@permission_required("read", "record", "id")
def export_record(id, export_type):
    """Page to view the exported data of a record.

    Currently only ``json`` is supported as export type.
    """
    record = Record.query.get_active_or_404(id)

    if export_type == "json":
        title = "JSON"
    else:
        abort(404)

    data = get_export_data(record, export_type)

    return render_template(
        "records/export_record.html",
        title=title,
        record=record,
        export_type=export_type,
        data=data,
    )


@bp.route("/<int:id>/publish/<provider>", methods=["GET", "POST"])
@permission_required("read", "record", "id")
def publish_record(id, provider):
    """Page to publish a record using a given provider."""
    record = Record.query.get_active_or_404(id)

    publication_providers = get_publication_providers()
    publication_provider = find_dict_in_list(publication_providers, "name", provider)

    if publication_provider is None:
        abort(404)

    if request.method == "POST":
        endpoint = url_for("records.publish_record", id=record.id, provider=provider)

        if not publication_provider["is_connected"]:
            return redirect(endpoint)

        task = Task.query.filter(
            Task.name == "kadi.records.publish_record",
            Task.state.in_(["pending", "running"]),
            Task.user_id == current_user.id,
        ).first()

        if task:
            flash(_("A publishing task is already in progress."), "info")
            return redirect(endpoint)

        task = start_publish_record_task(record, provider)

        if not task:
            flash(_("Error starting publishing task."), "danger")
        else:
            flash(_("Publishing task started successfully."), "success")

    return render_template(
        "records/publish_record.html", record=record, provider=publication_provider
    )


@bp.route("/<int:id>/links", methods=["GET", "POST"])
@permission_required("link", "record", "id")
@qparam("tab", "records")
def manage_links(id, qparams):
    """Page to link a record to other records or collections."""
    record = Record.query.get_active_or_404(id)

    record_form = LinkRecordForm(_suffix="record")
    collections_form = LinkCollectionsForm(_suffix="collections")

    if qparams["tab"] == "records" and record_form.validate_on_submit():
        linked_record = Record.query.get(record_form.record.data)
        if (
            linked_record is not None
            and linked_record != record
            and has_permission(current_user, "link", "record", linked_record.id)
        ):
            RecordLink.create(
                name=record_form.name.data,
                record_from=record,
                record_to=linked_record,
            )
            db.session.commit()
            flash(_("Changes saved successfully."), "success")

        # Redirect to easily clear the form.
        return redirect(url_for("records.manage_links", id=record.id))

    if collections_form.validate_on_submit():
        add_links(Collection, record.collections, collections_form.collections.data)
        db.session.commit()
        flash(_("Changes saved successfully."), "success")

    return render_template(
        "records/manage_links.html",
        title=_("Links"),
        record_form=record_form,
        collections_form=collections_form,
        record=record,
    )


@bp.route("/<int:id>/permissions", methods=["GET", "POST"])
@permission_required("permissions", "record", "id")
def manage_permissions(id):
    """Page to manage access permissions of a record."""
    record = Record.query.get_active_or_404(id)

    form = AddPermissionsForm()
    if form.validate_on_submit():
        add_roles(User, form.users.data, record, form.role.data)
        add_roles(Group, form.groups.data, record, form.role.data)
        db.session.commit()
        flash(_("Changes saved successfully."), "success")

    return render_template(
        "records/manage_permissions.html",
        title=_("Permissions"),
        form=form,
        record=record,
    )


@bp.route("/<int:id>/files")
@permission_required("update", "record", "id")
def add_files(id):
    """Page to add files to a record."""
    record = Record.query.get_active_or_404(id)
    return render_template("records/add_files.html", title=_("Files"), record=record)


@bp.route("/<int:record_id>/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
def view_record_revision(record_id, revision_id):
    """Page to view a specific revision of a record."""
    record = Record.query.get_active_or_404(record_id)
    revision = Record._revision_class.query.get_or_404(revision_id)

    if record.id != revision.record_id:
        abort(404)

    return render_template(
        "records/view_revision.html",
        title=_("Revision"),
        record=record,
        revision=revision,
    )


@bp.route("/<int:record_id>/files/revisions/<int:revision_id>")
@permission_required("read", "record", "record_id")
def view_file_revision(record_id, revision_id):
    """Page to view a specific file revision of a record."""
    record = Record.query.get_active_or_404(record_id)
    revision = File._revision_class.query.get_or_404(revision_id)

    if record.id != revision.file.record_id:
        abort(404)

    return render_template(
        "records/view_revision.html",
        title=_("Revision"),
        record=record,
        revision=revision,
    )


@bp.route("/<int:id>/delete", methods=["POST"])
@permission_required("delete", "record", "id")
def delete_record(id):
    """Endpoint to delete an existing record.

    Does basically the same as the corresponding API endpoint.
    """
    record = Record.query.get_active_or_404(id)

    _delete_record(record)
    db.session.commit()

    flash(_("Record deleted successfully."), "success")
    return redirect(url_for("records.records"))


@bp.route("/<int:record_id>/files/<uuid:file_id>")
@permission_required("read", "record", "record_id")
def view_file(record_id, file_id):
    """Page to view a file of a record."""
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    return render_template(
        "records/view_file.html",
        record=record,
        file=file,
        js_resources={
            "get_file_preview_endpoint": url_for(
                "api.get_file_preview", record_id=record.id, file_id=file.id
            )
        },
    )


@bp.route("/<int:record_id>/files/<uuid:file_id>/edit", methods=["GET", "POST"])
@permission_required("update", "record", "record_id")
def edit_file(record_id, file_id):
    """Page to edit an existing file of a record."""
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    form = EditFileForm(file)
    if form.validate_on_submit():
        if update_file(file, name=form.name.data, mimetype=form.mimetype.data):
            db.session.commit()

            flash(_("Changes saved successfully."), "success")
            return redirect(
                url_for("records.view_file", record_id=record.id, file_id=file.id)
            )

        flash(_("Error editing file."), "danger")

    return render_template(
        "records/edit_file.html", title=_("Edit"), form=form, record=record, file=file
    )


@bp.route("/<int:record_id>/files/<uuid:file_id>/delete", methods=["POST"])
@permission_required("update", "record", "record_id")
def delete_file(record_id, file_id):
    """Endpoint to delete an existing file.

    Does basically the same as the corresponding API endpoint.
    """
    record = Record.query.get_active_or_404(record_id)
    file = File.query.get_active_or_404(file_id)

    if file.record != record:
        abort(404)

    _delete_file(file)
    db.session.commit()

    flash(_("File deleted successfully."), "success")
    return redirect(url_for("records.view_record", id=record.id, tab="files"))
