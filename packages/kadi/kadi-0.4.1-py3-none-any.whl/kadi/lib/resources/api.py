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
from flask import render_template
from flask_login import current_user

from .utils import add_link as _add_link
from .utils import remove_link as _remove_link
from kadi.ext.db import db
from kadi.lib.api.core import json_error_response
from kadi.lib.api.core import json_response
from kadi.lib.exceptions import KadiPermissionError
from kadi.lib.utils import get_proxied_object
from kadi.modules.accounts.models import User
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.permissions.models import Role
from kadi.modules.permissions.schemas import GroupRoleSchema
from kadi.modules.permissions.schemas import UserRoleSchema
from kadi.modules.permissions.utils import add_role as _add_role
from kadi.modules.permissions.utils import get_group_roles
from kadi.modules.permissions.utils import get_object_roles
from kadi.modules.permissions.utils import get_user_roles
from kadi.modules.permissions.utils import remove_role as _remove_role


def add_link(relationship, resource, user=None):
    """Convenience function to link two resources together.

    For ease of use in API endpoints. Uses :func:`kadi.lib.resources.utils.add_link`.

    Note that this function may issue one or more database commits.

    :param relationship: The many-to-many relationship to append the resource to.
    :param resource: The resource to link, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: A JSON response depending on the success of the operation.
    """
    user = user if user is not None else current_user

    try:
        if _add_link(relationship, resource, user=user):
            db.session.commit()
            return json_response(201)

        return json_error_response(409, description="Link already exists.")

    except KadiPermissionError as e:
        return json_error_response(403, description=str(e))


def remove_link(relationship, resource, user=None):
    """Convenience function to remove the link between two resources.

    For ease of use in API endpoints. Uses :func:`kadi.lib.resources.utils.remove_link`.

    Note that this function may issue one or more database commits.

    :param relationship: The many-to-many relationship to remove the resource from.
    :param resource: The resource to remove, an instance of :class:`.Record` or
        :class:`.Collection`.
    :param user: (optional) The user performing the operation. Defaults to the current
        user.
    :return: A JSON response depending on the success of the operation.
    """
    user = user if user is not None else current_user

    try:
        if _remove_link(relationship, resource, user=user):
            db.session.commit()
            return json_response(204)

        return json_error_response(404, description="Link does not exist.")

    except KadiPermissionError as e:
        return json_error_response(403, description=str(e))


def add_role(subject, resource, role_name):
    """Convenience function to add an existing role to a user or group.

    For ease of use in API endpoints. Uses
    :func:`kadi.modules.permissions.utils.add_role`.

    Note that this function may issue one or more database commits.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :param role_name: The name of the role to add.
    :return: A JSON response depending on the success of the operation.
    """
    try:
        if _add_role(subject, resource.__tablename__, resource.id, role_name):
            db.session.commit()
            return json_response(201)

        return json_error_response(
            409, description="A role for that resource already exists."
        )

    except ValueError:
        return json_error_response(
            400, description="A role with that name does not exist."
        )


def remove_role(subject, resource):
    """Convenience function to remove an existing role of a user or group.

    For ease of use in API endpoints. Uses
    :func:`kadi.modules.permissions.utils.remove_role`. If the given subject is the
    creator of the given resource, the role will not be removed.

    Note that this function may issue one or more database commits.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :return: A JSON response depending on the success of the operation.
    """
    subject = get_proxied_object(subject)

    if isinstance(subject, User) and subject == resource.creator:
        return json_error_response(409, description="Cannot remove the creator's role.")

    if _remove_role(subject, resource.__tablename__, resource.id):
        db.session.commit()
        return json_response(204)

    return json_error_response(404, description="Role does not exist.")


def change_role(subject, resource, role_name):
    """Convenience function to change an existing role of a user or group.

    For ease of use in API endpoints. If the given subject is the creator of the given
    resource, the role will not be changed. Uses
    :func:`kadi.modules.permissions.utils.remove_role` and
    :func:`kadi.modules.permissions.utils.add_role`.

    Note that this function may issue one or more database commits.

    :param subject: The user or group.
    :param resource: The resource the role refers to, an instance of :class:`.Record`,
        :class:`.Collection`, :class:`.Group` or :class:`.Template`.
    :param role_name: The name of the role to exchange.
    :return: A JSON response depending on the success of the operation.
    """
    subject = get_proxied_object(subject)

    if isinstance(subject, User) and subject == resource.creator:
        return json_error_response(409, description="Cannot change the creator's role.")

    if _remove_role(subject, resource.__tablename__, resource.id):
        try:
            _add_role(subject, resource.__tablename__, resource.id, role_name)
            db.session.commit()
            return json_response(200)

        except ValueError:
            return json_error_response(
                400, description="A role with that name does not exist."
            )

    return json_error_response(404, description="Role does not exist.")


def get_selected_resources(
    model, page=1, term="", exclude=None, actions=None, user=None
):
    """Convenience function to search resources for use in dynamic selections.

    For ease of use in API endpoints. Used in conjunction with "Select2" to dynamically
    populate and search through dropdown menus or similar fields.

    :param model: The resource model to search, one of :class:`.Record`,
        :class:`.Collection` or :class:`.Group`.
    :param page: (optional) The current page.
    :param term: (optional) The search term. Will be used to search the title and
        identifier of the resource (case insensitive).
    :param exclude: (optional) A list of one or multiple resource IDs to exclude in the
        results. Defaults to an empty list.
    :param actions: (optional) One or multiple actions to restrict the returned
        resources to specific permissions of the given user, see :class:`.Permission`.
        Defaults to ``["read"]``.
    :param user: (optional) The user performing the search. Defaults to the current
        user.
    :return: A JSON response containing the results in the following form, assuming the
        search results consist of a single :class:`.Record`:

        .. code-block:: js

            {
                "results": [
                    {
                        "id": 1,
                        "text": "@sample-record-1",
                        "body": "<optional HTML body>",
                    }
                ],
                "pagination": {"more": false},
            }
    """
    exclude = exclude if exclude is not None else []
    actions = actions if actions is not None else ["read"]
    user = user if user is not None else current_user

    queries = []
    for action in actions:
        resources_query = get_permitted_objects(user, action, model.__tablename__)

        if resources_query:
            queries.append(resources_query)

    paginated_resources = (
        queries[0]
        .intersect(*queries[1:])
        .filter(
            db.or_(model.title.ilike(f"%{term}%"), model.identifier.ilike(f"%{term}%")),
            model.id.notin_(exclude),
            model.state == "active",
        )
        .order_by(model.title)
        .paginate(page, 10, False)
    )

    data = {"results": [], "pagination": {"more": paginated_resources.has_next}}
    for resource in paginated_resources.items:
        data["results"].append(
            {
                "id": resource.id,
                "text": "@" + resource.identifier,
                "body": render_template(
                    "snippets/resources/select.html", resource=resource
                ),
            }
        )

    return json_response(200, data)


def get_resource_user_roles(resource, page=1, per_page=10, exclude=None):
    """Get the paginated user roles of a resource.

    :param resource: The resource to get the user roles of. One of :class:`.Record`,
        :class:`.Collection` or :class:`.Template`.
    :param page: (optional) The current page.
     :param per_page: (optional) Items per page.
    :param exclude: (optional) A list of user IDs to exclude in the results.
    :return: A tuple containing a list of deserialized user roles and the total amount
        of user roles.
    """
    exclude = exclude if exclude is not None else []
    object_name = resource.__class__.__tablename__

    when = []
    for index, role in enumerate(get_object_roles(object_name)):
        when.append((role["name"], index))

    paginated_user_roles = (
        get_user_roles(object_name, object_id=resource.id)
        .filter(User.id.notin_(exclude))
        .order_by(
            (User.id == resource.creator.id).desc(),
            db.case(when, value=Role.name).desc(),
            User.id,
        )
        .paginate(page, per_page, False)
    )

    items = UserRoleSchema(obj=resource).dump_from_iterable(paginated_user_roles.items)

    return items, paginated_user_roles.total


def get_resource_group_roles(resource, page=1, per_page=10, user=None):
    """Get the paginated group roles of a resource.

    This includes the special case of the given user not having read access to a group
    (any more) but wanting to change/remove permissions of the group (if the permissions
    of the user allow them to). Since such groups should still be listed, we include
    them using a limited subset of group attributes.

    :param resource: The resource to get the group roles of. One of :class:`.Record`,
        :class:`.Collection` or :class:`.Template`.
    :param page: (optional) The current page.
     :param per_page: (optional) Items per page.
    :param user: (optional) The user to check for any permissions regarding the
        resulting groups. Defaults to the current user.
    :return: A tuple containing a list of deserialized group roles and the total amount
        of user roles.
    """
    user = user if user is not None else current_user
    object_name = resource.__class__.__tablename__

    when = []
    for index, role in enumerate(get_object_roles(object_name)):
        when.append((role["name"], index))

    # Already filtered for active groups.
    group_roles_query = get_group_roles(object_name, object_id=resource.id)
    group_ids = get_permitted_objects(user, "read", "group").with_entities(Group.id)

    # Check whether we have the special case of including all group roles.
    include_all_groups = False
    if has_permission(user, "permissions", object_name, resource.id):
        include_all_groups = True
    else:
        group_roles_query = group_roles_query.filter(Group.id.in_(group_ids))

    paginated_group_roles = group_roles_query.order_by(
        db.case(when, value=Role.name).desc(), Group.id
    ).paginate(page, per_page, False)

    items = GroupRoleSchema(obj=resource).dump_from_iterable(
        paginated_group_roles.items
    )

    if include_all_groups:
        group_ids = {group.id for group in group_ids}

        for item in items:
            group = item["group"]

            if group["id"] not in group_ids:
                item["group"] = {
                    "id": group["id"],
                    "title": group["title"],
                    "identifier": group["identifier"],
                    "visibility": group["visibility"],
                }

    return items, paginated_group_roles.total
