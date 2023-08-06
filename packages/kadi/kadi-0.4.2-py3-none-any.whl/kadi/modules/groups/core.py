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
from elasticsearch_dsl import Q
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .models import Group
from .utils import delete_group_image
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import update_object
from kadi.lib.resources.utils import search_resources
from kadi.lib.revisions.core import create_revision
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.utils import add_role
from kadi.modules.permissions.utils import delete_permissions
from kadi.modules.permissions.utils import setup_permissions


def create_group(
    *,
    identifier,
    title,
    creator=None,
    description="",
    state="active",
    visibility="private",
):
    """Create a new group.

    This will also create all default permissions of the group.

    :param identifier: See :attr:`.Group.identifier`.
    :param title: See :attr:`.Group.title`.
    :param creator: (optional) The user that created the group. Defaults to the current
        user.
    :param description: (optional) See :attr:`.Group.description`.
    :param state: (optional) See :attr:`.Group.state`.
    :param visibility: (optional) See :attr:`.Group.visibility`.
    :return: The created group  or ``None`` if the group could not be created.
    """
    creator = creator if creator is not None else current_user

    group = Group.create(
        creator=creator,
        identifier=identifier,
        title=title,
        description=description,
        plain_description=strip_markdown(description),
        state=state,
        visibility=visibility,
    )

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    setup_permissions("group", group.id)
    add_role(creator, "group", group.id, "admin")

    create_revision(group, user=creator)

    return group


def update_group(group, **kwargs):
    r"""Update an existing group.

    :param group: The group to update.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the group was updated successfully, ``False`` otherwise.
    """
    if group.state != "active":
        return False

    update_object(group, **kwargs)

    if "description" in kwargs:
        group.plain_description = strip_markdown(kwargs["description"])

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    create_revision(group)

    return True


def delete_group(group):
    """Delete an existing group.

    This will perform a soft deletion, i.e. the groups's state will be set to
    ``"deleted"``.

    :param group: The group to delete.
    """
    group.state = "deleted"
    create_revision(group)


def restore_group(group):
    """Restore a deleted group.

    :param group: The group to restore.
    """
    if group.state == "deleted":
        group.state = "active"
        create_revision(group)


def purge_group(group):
    """Purge an existing group.

    This will completely delete the group from the database.

    :param group: The group to purge.
    """
    group.revisions.delete(synchronize_session="fetch")

    delete_permissions("group", group.id)
    delete_group_image(group)

    db.session.delete(group)


def search_groups(
    query, page=1, per_page=10, sort="_score", highlight=False, groups_query=None
):
    """Convenience function to search for and filter groups.

    Uses :func:`kadi.lib.resources.utils.search_resources`.

    :param query: The search query as string to search for the title, identifier and
        plain description of the group.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param highlight: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param groups_query: (optional) The base query to filter the search results with.
        Defaults to a query containing all groups the current user has permission to
        read.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    if not groups_query:
        groups_query = get_permitted_objects(current_user, "read", "group").active()

    group_ids = groups_query.with_entities(Group.id)
    group_ids = [group_id[0] for group_id in group_ids]

    if query:
        query = Q("multi_match", query=query, fields=["*"], fuzziness="AUTO")

    return search_resources(
        Group,
        query=query,
        page=page,
        per_page=per_page,
        sort=sort,
        filter_ids=group_ids,
        highlight=highlight,
    )
