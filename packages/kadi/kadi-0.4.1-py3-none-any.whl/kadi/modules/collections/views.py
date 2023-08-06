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
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

from .blueprint import bp
from .core import create_collection
from .core import delete_collection as _delete_collection
from .core import search_collections
from .core import update_collection
from .forms import AddCollectionPermissionsForm
from .forms import AddRecordsPermissionsForm
from .forms import EditCollectionForm
from .forms import LinkRecordsForm
from .forms import NewCollectionForm
from .models import Collection
from .utils import get_export_data
from kadi.ext.db import db
from kadi.lib.forms import field_to_dict
from kadi.lib.resources.views import add_links
from kadi.lib.resources.views import add_roles
from kadi.lib.resources.views import copy_roles
from kadi.lib.resources.views import remove_roles
from kadi.lib.tags.models import Tag
from kadi.lib.utils import create_pagination
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.models import Record


@bp.route("")
@login_required
@paginated(page_max=100)
@qparam("query", "")
@qparam("sort", "_score")
@qparam("tag", [], multiple=True)
@qparam("tag_limit", 25, type=int)
def collections(page, per_page, qparams):
    """Collection overview page.

    Allows users to search and filter for collections or create new ones.
    """
    collections_query = get_permitted_objects(
        current_user, "read", "collection"
    ).active()

    search_results, total_collections = search_collections(
        qparams["query"],
        sort=qparams["sort"],
        tags=qparams["tag"],
        page=page,
        per_page=per_page,
        collections_query=collections_query,
        highlight=True,
    )

    pagination = create_pagination(total_collections, page, per_page)

    tags = (
        collections_query.join(Collection.tags)
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

    return render_template(
        "collections/collections.html",
        title=_("Collections"),
        collections=search_results,
        total_collections=total_collections,
        tags=tags,
        total_tags=total_tags,
        pagination=pagination,
        query_params={"page": page, "per_page": per_page, **qparams},
        js_resources={"per_page": per_page},
    )


@bp.route("/new", methods=["GET", "POST"])
@permission_required("create", "collection", None)
@qparam("collection", None, type=int)
def new_collection(qparams):
    """Page to create a new collection."""
    copied_collection = None

    # Copy a collections's metadata.
    if request.method == "GET" and qparams["collection"] is not None:
        copied_collection = Collection.query.get(qparams["collection"])

    form = NewCollectionForm(collection=copied_collection)

    if request.method == "POST":
        if form.validate():
            collection = create_collection(
                identifier=form.identifier.data,
                title=form.title.data,
                description=form.description.data,
                visibility=form.visibility.data,
                tags=form.tags.data,
            )

            if collection:
                add_links(Record, collection.records, form.linked_records.data)
                copy_roles(collection, form.copy_permission.data)
                db.session.commit()

                flash(_("Collection created successfully."), "success")
                return redirect(
                    url_for("collections.view_collection", id=collection.id)
                )

        flash(_("Error creating collection."), "danger")

    return render_template(
        "collections/new_collection.html",
        title=_("New collection"),
        form=form,
        js_resources={"title_field": field_to_dict(form.title)},
    )


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@permission_required("update", "collection", "id")
def edit_collection(id):
    """Page to edit an existing collection."""
    collection = Collection.query.get_active_or_404(id)
    form = EditCollectionForm(collection)

    if request.method == "POST":
        if form.validate():
            if update_collection(
                collection,
                title=form.title.data,
                identifier=form.identifier.data,
                description=form.description.data,
                visibility=form.visibility.data,
                tags=form.tags.data,
            ):
                db.session.commit()

                flash(_("Changes saved successfully."), "success")
                return redirect(
                    url_for("collections.view_collection", id=collection.id)
                )

        flash(_("Error editing collection."), "danger")

    return render_template(
        "collections/edit_collection.html",
        title=_("Edit"),
        form=form,
        collection=collection,
        js_resources={"title_field": field_to_dict(form.title)},
    )


@bp.route("/<int:id>")
@permission_required("read", "collection", "id")
def view_collection(id):
    """Page to view a collection."""
    collection = Collection.query.get_active_or_404(id)
    return render_template(
        "collections/view_collection.html",
        collection=collection,
        js_resources={
            "new_record_endpoint": url_for(
                "records.new_record", collection=collection.id
            )
        },
    )


@bp.route("/<int:id>/export/<export_type>")
@permission_required("read", "collection", "id")
def export_collection(id, export_type):
    """Page to view the exported data of a collection.

    Currently only ``json`` is supported as export type.
    """
    collection = Collection.query.get_active_or_404(id)

    if export_type == "json":
        title = "JSON"
    else:
        abort(404)

    data = get_export_data(collection, export_type)

    return render_template(
        "collections/export_collection.html",
        title=title,
        collection=collection,
        export_type=export_type,
        data=data,
    )


@bp.route("/<int:id>/links", methods=["GET", "POST"])
@permission_required("link", "collection", "id")
def manage_links(id):
    """Page to link a collection to records."""
    collection = Collection.query.get_active_or_404(id)

    form = LinkRecordsForm()
    if form.validate_on_submit():
        add_links(Record, collection.records, form.records.data)
        db.session.commit()
        flash(_("Changes saved successfully."), "success")

    return render_template(
        "collections/manage_links.html",
        title=_("Links"),
        form=form,
        collection=collection,
    )


@bp.route("/<int:id>/permissions", methods=["GET", "POST"])
@permission_required("permissions", "collection", "id")
@qparam("tab", "collection")
def manage_permissions(id, qparams):
    """Page to manage access permissions of a collection."""
    collection = Collection.query.get_active_or_404(id)

    collection_form = AddCollectionPermissionsForm(_suffix="collection")
    records_form = AddRecordsPermissionsForm(_suffix="records")

    if qparams["tab"] == "collection" and collection_form.validate_on_submit():
        add_roles(
            User, collection_form.users.data, collection, collection_form.role.data
        )
        add_roles(
            Group, collection_form.groups.data, collection, collection_form.role.data
        )
        flash(_("Changes saved successfully."), "success")
        db.session.commit()

    elif records_form.validate_on_submit():
        record_ids = (
            get_permitted_objects(current_user, "permissions", "record")
            .active()
            .with_entities(Record.id)
        )
        records = collection.records.filter(Record.id.in_(record_ids))

        for record in records:
            # Always remove the roles first, which easily allows changing existing roles
            # as well.
            remove_roles(User, records_form.users.data, record)
            remove_roles(Group, records_form.groups.data, record)

            if records_form.role.data:
                add_roles(User, records_form.users.data, record, records_form.role.data)
                add_roles(
                    Group, records_form.groups.data, record, records_form.role.data
                )

        flash(_("Changes saved successfully."), "success")
        db.session.commit()

    return render_template(
        "collections/manage_permissions.html",
        title=_("Permissions"),
        collection_form=collection_form,
        records_form=records_form,
        collection=collection,
    )


@bp.route("/<int:collection_id>/revisions/<int:revision_id>")
@permission_required("read", "collection", "collection_id")
def view_revision(collection_id, revision_id):
    """Page to view a specific revision of a collection."""
    collection = Collection.query.get_active_or_404(collection_id)
    revision = Collection._revision_class.query.get_or_404(revision_id)

    if collection.id != revision.collection_id:
        abort(404)

    return render_template(
        "collections/view_revision.html",
        title=_("Revision"),
        collection=collection,
        revision=revision,
    )


@bp.route("/<int:id>/delete", methods=["POST"])
@permission_required("delete", "collection", "id")
def delete_collection(id):
    """Endpoint to delete an existing collection.

    Does basically the same as the corresponding API endpoint.
    """
    collection = Collection.query.get_active_or_404(id)

    _delete_collection(collection)
    db.session.commit()

    flash(_("Collection deleted successfully."), "success")
    return redirect(url_for("collections.collections"))
