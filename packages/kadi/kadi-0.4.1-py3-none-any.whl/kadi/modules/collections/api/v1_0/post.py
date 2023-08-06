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

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import reqschema
from kadi.lib.api.utils import status
from kadi.lib.resources.api import add_link
from kadi.lib.resources.api import add_role
from kadi.modules.accounts.models import User
from kadi.modules.collections.core import create_collection
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required
from kadi.modules.permissions.schemas import GroupRoleSchema
from kadi.modules.permissions.schemas import UserRoleSchema
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema


route = partial(bp.route, methods=["POST"])


@route("/collections")
@permission_required("create", "collection", None)
@scopes_required("collection.create")
@reqschema(
    CollectionSchema(exclude=["id"]), description="The metadata of the new collection."
)
@status(201, "Return the new collection.")
@status(409, "A conflict occured while trying to create the collection.")
def new_collection(schema):
    """Create a new collection."""
    collection = create_collection(**schema.load_or_400())
    if not collection:
        return json_error_response(409, description="Error creating collection.")

    db.session.commit()

    return json_response(201, CollectionSchema().dump(collection))


@route("/collections/<int:id>/records")
@permission_required("link", "collection", "id")
@scopes_required("collection.link")
@reqschema(
    RecordSchema(only=["id"]), description="The record to add to the collection."
)
@status(201, "Record successfully added to collection.")
@status(409, "The link already exists.")
def add_collection_record(id, schema):
    """Add a record to the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)
    record = Record.query.get_active_or_404(schema.load_or_400()["id"])

    return add_link(collection.records, record)


@route("/collections/<int:id>/roles/users")
@permission_required("permissions", "collection", "id")
@scopes_required("collection.permissions")
@reqschema(
    UserRoleSchema(only=["user.id", "role.name"]),
    description="The user and corresponding role to add.",
)
@status(201, "User role successfully added to collection.")
@status(409, "A role for that user already exists.")
def add_collection_user_role(id, schema):
    """Add a user role to the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)
    data = schema.load_or_400()
    user = User.query.get_or_404(data["user"]["id"])

    return add_role(user, collection, data["role"]["name"])


@route("/collections/<int:id>/roles/groups")
@permission_required("permissions", "collection", "id")
@scopes_required("collection.permissions")
@reqschema(
    GroupRoleSchema(only=["group.id", "role.name"]),
    description="The group and corresponding role to add.",
)
@status(201, "Group role successfully added to collection.")
@status(409, "A role for that group already exists.")
def add_collection_group_role(id, schema):
    """Add a group role to the collection specified by the given *id*."""
    collection = Collection.query.get_active_or_404(id)
    data = schema.load_or_400()
    group = Group.query.get_active_or_404(data["group"]["id"])

    return add_role(group, collection, data["role"]["name"])
