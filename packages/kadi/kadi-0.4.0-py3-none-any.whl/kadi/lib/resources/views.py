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
from flask_login import current_user

from .utils import add_link
from kadi.lib.exceptions import KadiPermissionError
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.utils import add_role
from kadi.modules.permissions.utils import get_group_roles
from kadi.modules.permissions.utils import get_user_roles
from kadi.modules.permissions.utils import remove_role


def add_links(model, relationship, resource_ids, user=None):
    """Convenience function to link multiple resources together.

    For ease of use in view functions. Uses :func:`kadi.lib.resources.utils.add_link`
    but silently ignores any errors.

    :param model: The model of which the resources to append are instances of, one of
        :class:`.Record` or :class:`.Collection`.
    :param relationship: The many-to-many relationship to append the new resources to.
    :param resource_ids: A list of resource IDs that should be linked referring to
        instances of the given model.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    """
    user = user if user is not None else current_user

    resources = model.query.filter(model.id.in_(resource_ids), model.state == "active")

    for resource in resources:
        try:
            add_link(relationship, resource, user=user)
        except KadiPermissionError:
            pass


def add_roles(model, subject_ids, resource, role_name):
    """Convenience function to add an existing role to users or groups.

    For ease of use in view functions. Uses
    :func:`kadi.modules.permissions.utils.add_role` but silently ignores any errors.

    :param model: The model of the subject, one of :class:`.User` or :class:`.Group`.
    :param subject_ids: A list of subject IDs that the role should be added to.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :param role_name: The name of the role to add.
    """
    subjects = model.query.filter(model.id.in_(subject_ids))

    # If the results contain the creator of a resource, nothing will happen as they have
    # a role already, so no special handling is needed.
    for subject in subjects:
        try:
            add_role(subject, resource.__tablename__, resource.id, role_name)
        except ValueError:
            pass


def remove_roles(model, subject_ids, resource):
    """Convenience function to remove roles of users or groups.

    For ease of use in view functions. Uses
    :func:`kadi.modules.permissions.utils.remove_role`. In case of users, the resource
    creator's role will always stay intact.

    :param model: The model of the subject, one of :class:`.User` or :class:`.Group`.
    :param subject_ids: A list of subject IDs that the role should be removed from.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    """
    subjects = model.query.filter(model.id.in_(subject_ids))

    for subject in subjects:
        if not isinstance(subject, User) or subject != resource.creator:
            remove_role(subject, resource.__tablename__, resource.id)


def copy_roles(resource, resource_id):
    """Convenience function to copy the roles of another resource.

    For ease of use in view functions. The creator of the new resource needs permission
    to read the resource to copy the roles from. Additionally, only group roles of
    groups that the creator can read are copied.

    :param resource: The resource the new roles refer to. An instance of
        :class:`.Record`, :class:`.Collection` or :class:`.Group`.
    :param resource_id: The ID of the resource to copy the roles from. The type of this
        object will always be the same than the one of ``resource``.
    """
    object_name = resource.__tablename__

    if resource_id is not None and has_permission(
        resource.creator, "read", object_name, resource_id
    ):
        user_roles_query = get_user_roles(object_name, object_id=resource_id)
        for user, role in user_roles_query:
            add_role(user, object_name, resource.id, role.name)

        # Limit the copied group roles to groups that the creator can at least read.
        group_ids = get_permitted_objects(
            resource.creator, "read", "group"
        ).with_entities(Group.id)
        group_roles_query = get_group_roles(object_name, object_id=resource_id).filter(
            Group.id.in_(group_ids)
        )
        for group, role in group_roles_query:
            add_role(group, object_name, resource.id, role.name)
