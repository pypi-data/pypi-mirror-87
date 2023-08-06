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

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import strip
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.modules.accounts.models import Identity
from kadi.modules.accounts.models import User
from kadi.modules.accounts.schemas import IdentitySchema
from kadi.modules.accounts.schemas import UserSchema
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.groups.models import Group
from kadi.modules.groups.schemas import GroupSchema
from kadi.modules.groups.utils import get_user_groups as _get_user_groups
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema
from kadi.modules.templates.models import Template
from kadi.modules.templates.schemas import TemplateSchema


route = partial(bp.route, methods=["GET"])


@route("/users")
@login_required
@scopes_required("user.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the users by their display name or username.",
)
@qparam(
    "inactive",
    "",
    description="Flag indicating whether inactive users should be returned as well."
    " Specifying any non-empty value will activate this flag.",
)
@status(
    200,
    "Return a paginated list of users, sorted by creation date in descending order.",
)
def get_users(page, per_page, qparams):
    """Get all users."""
    identity_queries = []
    for provider_config in current_app.config["AUTH_PROVIDERS"].values():
        model = provider_config["identity_class"]
        identities_query = model.query.filter(
            db.or_(
                model.displayname.ilike(f"%{qparams['filter']}%"),
                model.username.ilike(f"%{qparams['filter']}%"),
            ),
        ).with_entities(model.user_id.label("id"))

        identity_queries.append(identities_query)

    user_ids = identity_queries[0].union(*identity_queries[1:])

    # No need to filter out merged users, as they do not have any identities and
    # therefore should not appear here anyway.
    users_query = User.query.filter(User.id.in_(user_ids))
    if not qparams["inactive"]:
        users_query = users_query.filter(User.state == "active")

    paginated_users = users_query.order_by(User.created_at.desc()).paginate(
        page, per_page, False
    )

    data = {
        "items": UserSchema(many=True).dump(paginated_users.items),
        **create_pagination_data(
            paginated_users.total, page, per_page, "api.get_users", **qparams
        ),
    }

    return json_response(200, data)


@route("/users/me")
@login_required
@scopes_required("user.read")
@status(200, "Return the current user.")
def get_current_user():
    """Get the current user."""
    return json_response(200, UserSchema().dump(current_user))


@route("/users/<int:id>")
@login_required
@scopes_required("user.read")
@status(200, "Return the user.")
def get_user(id):
    """Get the user specified by the given *id*."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    return json_response(200, UserSchema().dump(user))


@route("/users/<int:id>/identities")
@login_required
@scopes_required("user.read")
@status(200, "Return a list of identities, sorted by type.")
def get_user_identities(id):
    """Get all identities of the user specified by the given *id*."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    identities = user.identities.order_by(Identity.type)
    return json_response(200, IdentitySchema(many=True).dump(identities))


@route("/users/<int:id>/records")
@login_required
@scopes_required("user.read", "record.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the records by their title or identifier.",
)
@qparam(
    "shared",
    "",
    description="Flag indicating whether records the current user created should be"
    " returned or records the current user shared with the specified user. Specifying"
    " any non-empty value will activate this flag.",
)
@status(
    200,
    "Return a list of paginated records, sorted by last modification date in descending"
    " order.",
)
def get_user_records(id, page, per_page, qparams):
    """Get all created or shared records of the user specified by the given *id*."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    resource_creator = user
    resource_viewer = current_user

    if qparams["shared"]:
        resource_creator = current_user
        resource_viewer = user

    record_ids = (
        get_permitted_objects(resource_viewer, "read", "record")
        .active()
        .with_entities(Record.id)
    )

    paginated_records = (
        resource_creator.records.filter(
            Record.id.in_(record_ids),
            db.or_(
                Record.title.ilike(f"%{qparams['filter']}%"),
                Record.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .order_by(Record.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": RecordSchema(many=True).dump(paginated_records.items),
        **create_pagination_data(
            paginated_records.total,
            page,
            per_page,
            "api.get_user_records",
            id=resource_creator.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/users/<int:id>/collections")
@login_required
@scopes_required("user.read", "collection.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the collections by their title or identifier.",
)
@qparam(
    "shared",
    "",
    description="Flag indicating whether collections the current user created should be"
    " returned or collections the current user shared with the specified user."
    " Specifying any non-empty value will activate this flag.",
)
@status(
    200,
    "Return a list of paginated collections, sorted by last modification date in"
    " descending order.",
)
def get_user_collections(id, page, per_page, qparams):
    """Get all created or shared collections of the user specified by the given *id*."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    resource_creator = user
    resource_viewer = current_user

    if qparams["shared"]:
        resource_creator = current_user
        resource_viewer = user

    collection_ids = (
        get_permitted_objects(resource_viewer, "read", "collection")
        .active()
        .with_entities(Collection.id)
    )

    paginated_collections = (
        resource_creator.collections.filter(
            Collection.id.in_(collection_ids),
            db.or_(
                Collection.title.ilike(f"%{qparams['filter']}%"),
                Collection.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .order_by(Collection.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": CollectionSchema(many=True).dump(paginated_collections.items),
        **create_pagination_data(
            paginated_collections.total,
            page,
            per_page,
            "api.get_user_collections",
            id=resource_creator.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/users/<int:id>/templates")
@login_required
@scopes_required("user.read", "template.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the templates by their title or identifier.",
)
@qparam(
    "shared",
    "",
    description="Flag indicating whether templates the current user created should be"
    " returned or templates the current user shared with the specified user. Specifying"
    " any non-empty value will activate this flag.",
)
@status(
    200,
    "Return a list of paginated templates, sorted by last modification date in"
    " descending order.",
)
def get_user_templates(id, page, per_page, qparams):
    """Get all created or shared templates of the user specified by the given *id*."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    resource_creator = user
    resource_viewer = current_user

    if qparams["shared"]:
        resource_creator = current_user
        resource_viewer = user

    template_ids = get_permitted_objects(
        resource_viewer, "read", "template"
    ).with_entities(Template.id)

    paginated_templates = (
        resource_creator.templates.filter(
            Template.id.in_(template_ids),
            db.or_(
                Template.title.ilike(f"%{qparams['filter']}%"),
                Template.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .order_by(Template.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": TemplateSchema(many=True).dump(paginated_templates.items),
        **create_pagination_data(
            paginated_templates.total,
            page,
            per_page,
            "api.get_user_templates",
            id=resource_creator.id,
            **qparams,
        ),
    }

    return json_response(200, data)


@route("/users/<int:id>/groups")
@login_required
@scopes_required("user.read", "group.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the groups by their title or identifier.",
)
@status(
    200,
    "Return a list of paginated groups, sorted by last modification date in descending"
    " order.",
)
def get_user_groups(id, page, per_page, qparams):
    """Get all groups the user specified by the given *id* is a member of."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    group_ids = get_permitted_objects(current_user, "read", "group").with_entities(
        Group.id
    )

    # Already filtered for active groups.
    paginated_groups = (
        _get_user_groups(user)
        .filter(
            Group.id.in_(group_ids),
            db.or_(
                Group.title.ilike(f"%{qparams['filter']}%"),
                Group.identifier.ilike(f"%{qparams['filter']}%"),
            ),
        )
        .order_by(Group.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": GroupSchema(many=True).dump(paginated_groups.items),
        **create_pagination_data(
            paginated_groups.total,
            page,
            per_page,
            "api.get_user_groups",
            id=user.id,
            **qparams,
        ),
    }

    return json_response(200, data)
