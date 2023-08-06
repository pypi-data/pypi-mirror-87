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
from functools import wraps

from flask import abort
from flask_login import current_user
from flask_login import login_required

from .models import Permission
from .models import Role
from kadi.lib.cache import memoize_request
from kadi.lib.db import get_class_by_tablename
from kadi.lib.utils import get_proxied_object
from kadi.lib.utils import rgetattr
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.groups.utils import get_user_groups


def _get_permissions(subject, action, object_name, check_groups=True):
    subject = get_proxied_object(subject)

    group_permissions_query = None
    if isinstance(subject, User) and check_groups:
        group_ids_query = get_user_groups(subject).with_entities(Group.id)

        # Fine granular permissions for the user's groups.
        group_permissions_query = (
            Permission.query.join(User.groups)
            .join(Group.permissions)
            .filter(
                Group.id.in_(group_ids_query),
                Permission.action == action,
                Permission.object == object_name,
            )
        )

        # Role permissions for the user's groups.
        group_permissions_query = group_permissions_query.union(
            Permission.query.join(User.groups)
            .join(Group.roles)
            .join(Role.permissions)
            .filter(
                Group.id.in_(group_ids_query),
                Permission.action == action,
                Permission.object == object_name,
            )
        )

    # Fine granular permissions.
    permissions_query = subject.permissions.filter(
        Permission.action == action, Permission.object == object_name
    )

    # Role permissions.
    permissions_query = permissions_query.union(
        Permission.query.join(subject.__class__.roles)
        .join(Role.permissions)
        .filter(
            Permission.action == action,
            Permission.object == object_name,
            subject.__class__.id == subject.id,
        )
    )

    if group_permissions_query:
        permissions_query = permissions_query.union(group_permissions_query)

    return permissions_query


@memoize_request
def has_permission(subject, action, object_name, object_id, check_groups=True):
    """Check if a user or group has permission to perform a specific action.

    Includes all fine granular permissions as well as all permissions from the roles of
    the user or group.

    :param subject: The user or group object.
    :param action: The action to check for.
    :param object_name: The type of object.
    :param object_id: The ID of a specific object or ``None`` for a global permission.
    :param check_groups: (optional) Flag indicating whether the groups of a user should
        be checked as well for their permissions.
    :return: ``True`` if permission is granted, ``False`` otherwise or if the object
        instance to check does not exist.
    """

    # Check if the object class exists.
    model = get_class_by_tablename(object_name)
    if not model:
        return False

    permissions = _get_permissions(
        subject, action, object_name, check_groups=check_groups
    )

    # Check global actions.
    if permissions.filter_by(object_id=None).first() is not None:
        return True

    if object_id is None:
        return False

    # Check if the object instance exists.
    object_instance = model.query.get(object_id)
    if not object_instance:
        return False

    # Check default permissions.
    default_permissions = rgetattr(object_instance, "Meta.permissions", {}).get(
        "default_permissions", {}
    )

    if action in default_permissions:
        for attr, val in default_permissions[action].items():
            if getattr(object_instance, attr, None) == val:
                return True

    # Finally check regular permissions.
    return permissions.filter_by(object_id=object_id).first() is not None


def get_permitted_objects(subject, action, object_name, check_groups=True):
    """Get all objects a user or group has a specific permission for.

    Includes all fine granular permissions as well as all permissions from the roles of
    the user or group.

    :param subject: The user or group object.
    :param action: The action to check for.
    :param object_name: The type of object.
    :param check_groups: (optional) Flag indicating whether the groups of a user should
        be checked as well for their permissions.
    :return: The permitted objects as query or ``None`` if the type of object does not
        exist.
    """

    # Check if the object class exists.
    model = get_class_by_tablename(object_name)
    if not model:
        return None

    permissions = _get_permissions(
        subject, action, object_name, check_groups=check_groups
    )

    # Check global actions.
    if permissions.filter_by(object_id=None).first():
        return model.query

    # Get objects with fitting default permissions.
    default_permissions = rgetattr(model, "Meta.permissions", {}).get(
        "default_permissions", {}
    )

    default_objects_query = None
    if action in default_permissions:
        attrs = []
        for attr, val in default_permissions[action].items():
            attrs.append(getattr(model, attr, None) == val)
        if attrs:
            default_objects_query = model.query.filter(*attrs)

    # Get objects for regular permissions.
    object_ids = permissions.with_entities(Permission.object_id)
    objects_query = model.query.filter(model.id.in_(object_ids))

    if default_objects_query:
        objects_query = objects_query.union(default_objects_query)

    return objects_query


def permission_required(action, object_name, object_id_identifier, status_code=403):
    """Decorator to add access restrictions to a view function.

    If a user is not authenticated, the decorater will behave the same as Flask-Login's
    ``login_required`` decorator. Uses :func:`has_permission` to check for access
    permission. If the object or object instance to check do not exist, the request will
    automatically get aborted with a 404 status code.

    :param action: The action to check for.
    :param object_name: The type of object.
    :param object_id_identifier: The name of the variable to use as ``object_id``, which
        needs to be part of the keyword arguments of the decorated function. May also be
        ``None``.
    :param status_code: (optional) The status code to use if no permission was granted.
    """

    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            object_id = None
            if object_id_identifier is not None:
                object_id = kwargs[object_id_identifier]

            # Always return 404 if the model or object do not exist.
            model = get_class_by_tablename(object_name)
            if model is None or (
                object_id is not None and not model.query.get(object_id)
            ):
                abort(404)

            if not has_permission(
                current_user, action, object_name, object_id=object_id
            ):
                abort(status_code)

            return func(*args, **kwargs)

        return login_required(decorated_view)

    return decorator
