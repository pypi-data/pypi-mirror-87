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
from kadi.lib.revisions.models import Revision
from kadi.lib.revisions.schemas import ObjectRevisionSchema
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.accounts.models import User
from kadi.modules.groups.core import search_groups
from kadi.modules.groups.models import Group
from kadi.modules.groups.schemas import GroupSchema
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.core import permission_required
from kadi.modules.permissions.models import Role
from kadi.modules.permissions.schemas import UserRoleSchema
from kadi.modules.permissions.utils import get_object_roles
from kadi.modules.permissions.utils import get_user_roles


route = partial(bp.route, methods=["GET"])


@route("/groups")
@login_required
@scopes_required("group.read")
@paginated(page_max=100)
@qparam("query", "", description="The search query.")
@qparam("sort", "_score", description="The order of the search results.")
@status(200, "Return a paginated list of groups.")
def get_groups(page, per_page, qparams):
    """Get all groups or search and filter for specific groups.

    See :func:`kadi.modules.groups.core.search_groups` for a more detailed explanation
    of the query parameters.
    """
    groups, total_groups = search_groups(
        qparams["query"], sort=qparams["sort"], page=page, per_page=per_page
    )

    data = {
        "items": GroupSchema(many=True).dump(groups),
        "_actions": {"new_group": url_for("api.new_group")},
        **create_pagination_data(
            total_groups, page, per_page, "api.get_groups", **qparams
        ),
    }

    return json_response(200, data)


@route("/groups/<int:id>")
@permission_required("read", "group", "id")
@scopes_required("group.read")
@status(200, "Return the group.")
def get_group(id):
    """Get the group specified by the given *id*."""
    group = Group.query.get_active_or_404(id)
    return json_response(200, GroupSchema().dump(group))


@route("/groups/identifier/<identifier:identifier>")
@login_required
@scopes_required("group.read")
@status(200, "Return the group.")
def get_group_by_identifier(identifier):
    """Get the group specified by the given *identifier*."""
    group = Group.query.filter_by(identifier=identifier, state="active").first_or_404()

    if not has_permission(current_user, "read", "group", object_id=group.id):
        abort(403)

    return json_response(200, GroupSchema().dump(group))


@route("/groups/<int:id>/members")
@permission_required("read", "group", "id")
@scopes_required("group.read", "user.read")
@paginated
@qparam("exclude", [], multiple=True, type=int, description="User IDs to exclude.")
@status(
    200,
    "Return a paginated list of members, sorted by role name and then by user ID in"
    " ascending order. The creator will always be listed first.",
)
def get_group_members(id, page, per_page, qparams):
    """Get the members of the group specified by the given *id*."""
    group = Group.query.get_active_or_404(id)

    when = []
    for index, role in enumerate(get_object_roles("group")):
        when.append((role["name"], index))

    paginated_user_roles = (
        get_user_roles("group", object_id=id)
        .filter(User.id.notin_(qparams["exclude"]))
        .order_by(
            (User.id == group.creator.id).desc(),
            db.case(when, value=Role.name).desc(),
            User.id,
        )
        .paginate(page, per_page, False)
    )

    data = {
        "items": UserRoleSchema(group=group).dump_from_iterable(
            paginated_user_roles.items
        ),
        **create_pagination_data(
            paginated_user_roles.total,
            page,
            per_page,
            "api.get_group_members",
            id=group.id,
        ),
    }

    return json_response(200, data)


@route("/groups/<int:id>/revisions")
@permission_required("read", "group", "id")
@scopes_required("group.read")
@paginated
@status(
    200,
    "Return a paginated list of revisions, sorted by revision timestamp in descending"
    " order.",
)
def get_group_revisions(id, page, per_page):
    """Get the revisions of the group specified by the given *id*."""
    group = Group.query.get_active_or_404(id)

    paginated_revisions = (
        group.revisions.join(Revision)
        .order_by(Revision.timestamp.desc())
        .paginate(page, per_page, False)
    )

    schema = ObjectRevisionSchema(
        many=True,
        schema=GroupSchema,
        api_endpoint="api.get_group_revision",
        view_endpoint="groups.view_revision",
        endpoint_args={"group_id": group.id},
    )

    data = {
        "items": schema.dump(paginated_revisions.items),
        **create_pagination_data(
            paginated_revisions.total,
            page,
            per_page,
            "api.get_group_revisions",
            id=group.id,
        ),
    }

    return json_response(200, data)


@route("/groups/<int:group_id>/revisions/<int:revision_id>")
@permission_required("read", "group", "group_id")
@scopes_required("group.read")
@status(200, "Return the revision.")
def get_group_revision(group_id, revision_id):
    """Get a revision.

    Will return the revision specified by the given *revision_id* of the group specified
    by the given *group_id*.
    """
    group = Group.query.get_active_or_404(group_id)
    revision = Group._revision_class.query.get_or_404(revision_id)

    if group.id != revision.group_id:
        abort(404)

    schema = ObjectRevisionSchema(
        schema=GroupSchema,
        api_endpoint="api.get_group_revision",
        view_endpoint="groups.view_revision",
        endpoint_args={"group_id": group.id},
    )

    return json_response(200, schema.dump(revision))
