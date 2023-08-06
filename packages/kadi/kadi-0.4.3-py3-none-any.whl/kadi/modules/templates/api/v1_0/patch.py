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
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import reqschema
from kadi.lib.api.utils import status
from kadi.lib.resources.api import change_role
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required
from kadi.modules.permissions.schemas import RoleSchema
from kadi.modules.templates.core import update_template
from kadi.modules.templates.models import Template
from kadi.modules.templates.schemas import TemplateSchema


route = partial(bp.route, methods=["PATCH"])


@route("/templates/<int:id>")
@permission_required("update", "template", "id")
@scopes_required("template.update")
@reqschema(
    TemplateSchema(exclude=["type"], partial=True),
    description="The new metadata and data of the template, depending on its type.",
    bind=False,
)
@status(200, "Return the updated template.")
def edit_template(id):
    """Update the template specified by the given *id*."""
    template = Template.query.get_or_404(id)

    data = TemplateSchema(
        previous_template=template, type=template.type, exclude=["type"], partial=True
    ).load_or_400()

    update_template(template, **data)
    db.session.commit()

    return json_response(200, TemplateSchema().dump(template))


@route("/templates/<int:template_id>/roles/users/<int:user_id>")
@permission_required("permissions", "template", "template_id")
@scopes_required("template.permissions")
@reqschema(RoleSchema(), description="The new user role.")
@status(200, "User role successfully changed.")
@status(409, "When trying to change the creator's role.")
def change_template_user_role(template_id, user_id, schema):
    """Change a user role of a template.

    Will change the role of the user specified by the given *user_id* of the template
    specified by the given *template_id*.
    """
    template = Template.query.get_or_404(template_id)
    user = User.query.get_or_404(user_id)

    return change_role(user, template, schema.load_or_400()["name"])


@route("/templates/<int:template_id>/roles/groups/<int:group_id>")
@permission_required("permissions", "template", "template_id")
@scopes_required("template.permissions")
@reqschema(RoleSchema(), description="The new group role.")
@status(200, "Group role successfully changed.")
def change_template_group_role(template_id, group_id, schema):
    """Change a group role of a template.

    Will change the role of the group specified by the given *group_id* of the template
    specified by the given *template_id*.
    """
    template = Template.query.get_or_404(template_id)
    group = Group.query.get_active_or_404(group_id)

    return change_role(group, template, schema.load_or_400()["name"])
