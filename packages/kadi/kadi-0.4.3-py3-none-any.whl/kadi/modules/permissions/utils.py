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
from flask import current_app

from .models import Permission
from .models import Role
from kadi.ext.db import db
from kadi.lib.db import get_class_by_tablename
from kadi.lib.db import TimestampMixin
from kadi.lib.utils import rgetattr
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group


def setup_system_role(role_name):
    """Setup a system role with corresponding global permissions.

    Will create the given system role as defined in ``SYSTEM_ROLES`` in the
    application's configuration as well as all global permissions of the listed objects,
    which have to be specified in a ``Meta.permissions`` attribute in each corresponding
    model.

    **Example:**

    .. code-block:: python3

        class Foo:
            class Meta:
                permissions = {
                    "global_actions": [
                        ("create", "Create objects."),
                        ("read", "Read all objects."),
                    ],
                }

    :param role_name: The name of the system role to initialize.
    :return: The created (or possibly already existing) role object or ``None`` if the
        given role is invalid.
    """
    system_roles = current_app.config["SYSTEM_ROLES"]

    if role_name not in system_roles:
        return None

    role = Role.query.filter_by(name=role_name, object=None, object_id=None).first()

    if role is None:
        role = Role.create(name=role_name)

    for object_name, global_actions in system_roles[role_name].items():
        model = get_class_by_tablename(object_name)
        if model is None:
            continue

        model_actions = rgetattr(model, "Meta.permissions", {}).get(
            "global_actions", []
        )
        model_actions = [action_description[0] for action_description in model_actions]

        for action in global_actions:
            if action in model_actions:
                permission = Permission.query.filter_by(
                    action=action, object=object_name, object_id=None
                ).first()

                if permission is None:
                    permission = Permission.create(action=action, object=object_name)

                if permission not in role.permissions:
                    role.permissions.append(permission)

    return role


def setup_permissions(object_name, object_id):
    """Setup the default permissions of an object.

    The default actions and roles and have to be specified in a ``Meta.permissions``
    attribute in each model.

    **Example:**

    .. code-block:: python3

        class Foo:
            class Meta:
                permissions = {
                    "actions": [
                        ("read", "Read this object."),
                        ("update", "Edit this object."),
                    ],
                    "roles": [("admin", ["read", "update"])],
                }

    :param object_name: The type of object the permissions refer to.
    :param object_id: The ID of the object.
    :return: ``True`` if the permissions were set up successfully, ``False`` otherwise.
    """
    model = get_class_by_tablename(object_name)
    if model is None:
        return False

    permissions = {}
    for action, _ in model.Meta.permissions["actions"]:
        permission = Permission.create(
            action=action, object=object_name, object_id=object_id
        )

        permissions[action] = permission

    for name, actions in model.Meta.permissions["roles"]:
        role = Role.create(name=name, object=object_name, object_id=object_id)

        for action in actions:
            role.permissions.append(permissions[action])

    return True


def delete_permissions(object_name, object_id):
    """Delete all permissions of an object.

    :param object_name: The type of object the permissions refer to.
    :param object_id: The ID of the object.
    """
    roles = Role.query.filter(Role.object == object_name, Role.object_id == object_id)

    for role in roles:
        role.permissions = []
        role.users = []
        role.groups = []

    roles.delete(synchronize_session="fetch")

    permissions = Permission.query.filter(
        Permission.object == object_name, Permission.object_id == object_id
    )

    for permission in permissions:
        permission.roles = []
        permission.users = []
        permission.groups = []

    permissions.delete(synchronize_session="fetch")


def add_role(subject, object_name, object_id, role_name, update_timestamp=True):
    """Add an existing role to a user or group.

    :param subject: The user or group.
    :param object_name: The type of object the role refers to.
    :param object_id: The ID of the object.
    :param role_name: The name of the role.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`TimestampMixin` in that case.
    :return: ``True`` if the role was added successfully, ``False`` if the subject
        already has a role related to the given object or if the object does not exist.
    :raises ValueError: If no role with the given arguments exists.
    """
    model = get_class_by_tablename(object_name)
    obj = model.query.get(object_id)

    if model is None or obj is None:
        return False

    roles = subject.roles.filter_by(object=object_name, object_id=object_id)

    if roles.count() > 0:
        return False

    role = Role.query.filter_by(
        object=object_name, object_id=object_id, name=role_name
    ).first()

    if not role:
        raise ValueError("Specified role does not exist.")

    subject.roles.append(role)

    if update_timestamp and isinstance(obj, TimestampMixin):
        obj.update_timestamp()

    return True


def remove_role(subject, object_name, object_id, update_timestamp=True):
    """Remove an existing role of a user or group.

    Generally, only one role should exist per object instance which is why no role name
    needs to be given. As in certain circumstances (e.g. merging two users) a subject
    may have different roles, all roles related to the given object will be removed.

    :param subject: The user or group.
    :param object_name: The type of object the role refers to.
    :param object_id: The ID of the object.
    :param update_timestamp: (optional) Flag indicating whether the timestamp of the
        underlying object should be updated or not. The object needs to implement
        :class:`TimestampMixin` in that case.
    :return: ``True`` if the role was removed successfully, ``False`` if there was no
        role to remove or if the object does not exist.
    """
    model = get_class_by_tablename(object_name)
    obj = model.query.get(object_id)

    if model is None or obj is None:
        return False

    roles = subject.roles.filter_by(object=object_name, object_id=object_id)

    if roles.count() == 0:
        return False

    for role in roles:
        subject.roles.remove(role)

    if update_timestamp and isinstance(obj, TimestampMixin):
        obj.update_timestamp()

    return True


def get_user_roles(object_name, object_id=None):
    """Get all users and roles for a specific object or object type.

    :param object_name: The type of the object.
    :param object_id: (optional) The ID of a specific object.
    :return: The users and corresponding roles of the object(s) as query object.
    """
    user_roles_query = (
        db.session.query(User, Role).join(User.roles).filter(Role.object == object_name)
    )

    if object_id:
        user_roles_query = user_roles_query.filter(Role.object_id == object_id)

    return user_roles_query


def get_group_roles(object_name, object_id=None):
    """Get all groups and roles for a specific object or object type.

    Note that inactive groups will be filtered out.

    :param object_name: The type of the object.
    :param object_id: (optional) The ID of a specific object.
    :return: The groups and corresponding roles of the object(s) as query object.
    """
    group_roles_query = (
        db.session.query(Group, Role)
        .join(Group.roles)
        .filter(Role.object == object_name, Group.state == "active")
    )

    if object_id:
        group_roles_query = group_roles_query.filter(Role.object_id == object_id)

    return group_roles_query


def get_object_roles(object_name):
    """Get all possible roles and corresponding permissions of an object type.

    :param object_name: The type of the object.
    :return: A list of dictionaries in the following form:

        .. code-block:: python3

            [
                {
                    "name": "admin",
                    "permissions": [
                        {
                            "action": "read,
                            "description": "Read this resource.",
                        }
                    ]
                }
            ]
    """
    model = get_class_by_tablename(object_name)
    roles = [
        {
            "name": role,
            "permissions": [
                {
                    "action": action,
                    "description": get_action_description(action, object_name),
                }
                for action in actions
            ],
        }
        for role, actions in rgetattr(model, "Meta.permissions", {}).get("roles", [])
    ]

    return roles


def get_action_description(action, object_name):
    """Get the description of an action corresponding to a specific permission.

    :param action: The name of the action.
    :param object_name: The type of the object the action belongs to.
    :return: The description or ``None`` if no suitable action or no model corresponding
        to the object type could be found.
    """
    model = get_class_by_tablename(object_name)
    actions = rgetattr(model, "Meta.permissions", {}).get("actions", [])

    for object_action, description in actions:
        if object_action == action:
            return description

    return None
