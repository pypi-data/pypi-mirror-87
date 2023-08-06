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

from .models import Collection
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import update_object
from kadi.lib.resources.utils import search_resources
from kadi.lib.revisions.core import create_revision
from kadi.lib.tags.models import Tag
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.utils import add_role
from kadi.modules.permissions.utils import delete_permissions
from kadi.modules.permissions.utils import setup_permissions


def create_collection(
    *,
    identifier,
    title,
    creator=None,
    description="",
    tags=None,
    state="active",
    visibility="private",
):
    """Create a new collection.

    This will also create all default permissions of the collection.

    :param identifier: See :attr:`.Collection.identifier`.
    :param title: See :attr:`.Collection.title`.
    :param creator: (optional) The user that created the collection. Defaults to the
        current user.
    :param description: (optional) See :attr:`.Collection.description`.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :param state: (optional) See :attr:`.Collection.state`.
    :param visibility: (optional) See :attr:`.Collection.visibility`.
    :return: The created collection or ``None`` if the collection could not be created.
    """
    creator = creator if creator is not None else current_user

    collection = Collection.create(
        creator=creator,
        identifier=identifier,
        title=title,
        description=description,
        plain_description=strip_markdown(description),
        state=state,
        visibility=visibility,
    )

    if tags is not None:
        collection.set_tags(tags)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    setup_permissions("collection", collection.id)
    add_role(creator, "collection", collection.id, "admin")

    create_revision(collection, user=creator)

    return collection


def update_collection(collection, tags=None, **kwargs):
    r"""Update an existing collection.

    :param collection: The collection to update.
    :param tags: (optional) A list of tag names to tag the collection with. See also
        :class:`.Tag`.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the collection was updated successfully, ``False`` otherwise.
    """
    if collection.state != "active":
        return False

    update_object(collection, **kwargs)

    if "description" in kwargs:
        collection.plain_description = strip_markdown(kwargs["description"])

    if tags is not None:
        collection.set_tags(tags)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    create_revision(collection)

    return True


def delete_collection(collection):
    """Delete an existing collection.

    This will perform a soft deletion, i.e. the collections's state will be set to
    ``"deleted"``.

    :param collection: The collection to delete.
    """
    collection.state = "deleted"
    create_revision(collection)


def restore_collection(collection):
    """Restore a deleted collection.

    :param collection: The collection to restore.
    """
    if collection.state == "deleted":
        collection.state = "active"
        create_revision(collection)


def purge_collection(collection):
    """Purge an existing collection.

    This will completely delete the collection from the database.

    :param collection: The collection to purge.
    """
    collection.records = []

    collection.revisions.delete(synchronize_session="fetch")

    delete_permissions("collection", collection.id)

    db.session.delete(collection)


def search_collections(
    query,
    page=1,
    per_page=10,
    sort="_score",
    tags=None,
    highlight=False,
    collections_query=None,
):
    """Convenience function to search for and filter collections.

    Uses :func:`kadi.lib.resources.utils.search_resources`.

    :param query: The search query as string to search for the title, identifier and
        plain description of the collection.
    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param highlight: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param tags: (optional) A list of tag names to filter the collections with before
        searching. All given tags are filtered using an *OR* operation.
    :param collections_query: (optional) The base query to filter the search results
        with. Defaults to a query containing all collections the current user has
        permission to read.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    if not collections_query:
        collections_query = get_permitted_objects(
            current_user, "read", "collection"
        ).active()

    if tags:
        collections_query = collections_query.join(Collection.tags).filter(
            Tag.name.in_(tags)
        )

    collection_ids = collections_query.with_entities(Collection.id)
    collection_ids = [collection_id[0] for collection_id in collection_ids]

    if query:
        query = Q("multi_match", query=query, fields=["*"], fuzziness="AUTO")

    return search_resources(
        Collection,
        query=query,
        page=page,
        per_page=per_page,
        sort=sort,
        filter_ids=collection_ids,
        highlight=highlight,
    )
