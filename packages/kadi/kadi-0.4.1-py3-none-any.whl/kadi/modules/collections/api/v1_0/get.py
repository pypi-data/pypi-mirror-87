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
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.collections.core import search_collections
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema


route = partial(bp.route, methods=["GET"])


@route("/collections")
@login_required
@scopes_required("collection.read")
@paginated(page_max=100)
@qparam("query", "", description="The search query.")
@qparam("sort", "_score", description="The order of the search results.")
@qparam("tag", [], multiple=True, description="Tags to filter the collections with.")
@status(200, "Return a paginated list of collections.")
def get_collections(page, per_page, qparams):
    """Get all collections or search and filter for specific collections.

    See :func:`kadi.modules.collections.core.search_collections` for a more detailed
    explanation of the query parameters.
    """
    collections, total_collections = search_collections(
        qparams["query"],
        sort=qparams["sort"],
        tags=qparams["tag"],
        page=page,
        per_page=per_page,
    )

    data = {
        "items": CollectionSchema(many=True).dump(collections),
        "_actions": {"new_collection": url_for("api.new_collection")},
        **create_pagination_data(
            total_collections, page, per_page, "api.get_collections", **qparams
        ),
    }

    return json_response(200, data)


@route("/collections/<int:id>")
@permission_required("read", "collection", "id")
@scopes_required("collection.read")
@status(200, "Return the collection.")
def get_collection(id):
    """Get the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)
    return json_response(200, CollectionSchema().dump(collection))


@route("/collections/identifier/<identifier:identifier>")
@login_required
@scopes_required("collection.read")
@status(200, "Return the collection.")
def get_collection_by_identifier(identifier):
    """Get the collection specified by the given *identifier*."""
    collection = Collection.query.filter_by(
        identifier=identifier, state="active"
    ).first_or_404()

    if not has_permission(current_user, "read", "collection", object_id=collection.id):
        abort(403)

    return json_response(200, CollectionSchema().dump(collection))


@route("/collections/<int:id>/records")
@permission_required("read", "collection", "id")
@scopes_required("collection.read", "record.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the records by their title or identifier.",
)
@qparam(
    "action",
    [],
    multiple=True,
    description="Further actions the current user needs permission to perform in the"
    " linked records.",
)
@status(200, "Return a paginated list of records, sorted by title in ascending order.")
def get_collection_records(id, page, per_page, qparams):
    """Get the records the collection specified by the given *id* contains."""
    collection = Collection.query.get_active_or_404(id)

    paginated_records = (
        get_linked_resources(Record, collection.records, actions=qparams["action"])
        .filter(
            db.or_(
                Record.title.ilike(f"%{qparams['filter']}%"),
                Record.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .paginate(page, per_page, False)
    )

    data = {
        "items": RecordSchema(many=True, linked_collection=collection).dump(
            paginated_records.items
        ),
        **create_pagination_data(
            paginated_records.total,
            page,
            per_page,
            "api.get_collection_records",
            id=collection.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/collections/<int:id>/roles/users")
@permission_required("read", "collection", "id")
@scopes_required("collection.read", "user.read")
@paginated
@qparam("exclude", [], multiple=True, type=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of user roles, sorted by role name and then by user ID in"
    " ascending order. The creator will always be listed first.",
)
def get_collection_user_roles(id, page, per_page, qparams):
    """Get the user roles of the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)

    items, total = get_resource_user_roles(
        collection, page=page, per_page=per_page, exclude=qparams["exclude"]
    )
    data = {
        "items": items,
        **create_pagination_data(
            total, page, per_page, "api.get_collection_user_roles", id=collection.id
        ),
    }

    return json_response(200, data)


@route("/collections/<int:id>/roles/groups")
@permission_required("read", "collection", "id")
@scopes_required("collection.read", "group.read")
@paginated
@status(
    200,
    "Return a paginated list of group roles, sorted by role name and then by group ID"
    " in ascending order.",
)
def get_collection_group_roles(id, page, per_page):
    """Get the group roles of the collection specified by the given *id*.

    If a user can manage permissions in this collection, all group roles are returned.
    However, groups that a user can normally not read include only a limited subset of
    attributes.
    """
    collection = Collection.query.get_active_or_404(id)

    items, total = get_resource_group_roles(collection, page=page, per_page=per_page)
    data = {
        "items": items,
        **create_pagination_data(
            total, page, per_page, "api.get_collection_group_roles", id=collection.id
        ),
    }

    return json_response(200, data)


@route("/collections/<int:id>/revisions")
@permission_required("read", "collection", "id")
@scopes_required("collection.read")
@paginated
@status(
    200,
    "Return a paginated list of revisions, sorted by revision timestamp in descending"
    " order.",
)
def get_collection_revisions(id, page, per_page):
    """Get the revisions of the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)

    paginated_revisions = (
        collection.revisions.join(Revision)
        .order_by(Revision.timestamp.desc())
        .paginate(page, per_page, False)
    )

    schema = ObjectRevisionSchema(
        many=True,
        schema=CollectionSchema,
        api_endpoint="api.get_collection_revision",
        view_endpoint="collections.view_revision",
        endpoint_args={"collection_id": collection.id},
    )

    data = {
        "items": schema.dump(paginated_revisions.items),
        **create_pagination_data(
            paginated_revisions.total,
            page,
            per_page,
            "api.get_collection_revisions",
            id=collection.id,
        ),
    }

    return json_response(200, data)


@route("/collections/<int:collection_id>/revisions/<int:revision_id>")
@permission_required("read", "collection", "collection_id")
@scopes_required("collection.read")
@status(200, "Return the revision.")
def get_collection_revision(collection_id, revision_id):
    """Get a revision.

    Will return the revision specified by the given *revision_id* of the collection
    specified by the given *collection_id*.
    """
    collection = Collection.query.get_active_or_404(collection_id)
    revision = Collection._revision_class.query.get_or_404(revision_id)

    if collection.id != revision.collection_id:
        abort(404)

    schema = ObjectRevisionSchema(
        schema=CollectionSchema,
        api_endpoint="api.get_collection_revision",
        view_endpoint="collections.view_revision",
        endpoint_args={"collection_id": collection.id},
    )

    return json_response(200, schema.dump(revision))
