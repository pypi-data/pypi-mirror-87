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

from .files import remove_files
from .files import remove_temporary_files
from .models import File
from .models import Record
from .models import TemporaryFile
from .models import Upload
from .uploads import remove_uploads
from kadi.ext.db import db
from kadi.lib.conversion import strip_markdown
from kadi.lib.db import update_object
from kadi.lib.licenses.models import License
from kadi.lib.resources.utils import search_resources
from kadi.lib.revisions.core import create_revision
from kadi.lib.tags.models import Tag
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.utils import add_role
from kadi.modules.permissions.utils import delete_permissions
from kadi.modules.permissions.utils import setup_permissions


def create_record(
    *,
    identifier,
    title,
    creator=None,
    type=None,
    description="",
    license=None,
    extras=None,
    tags=None,
    state="active",
    visibility="private",
):
    """Create a new record.

    This will also create all default permissions of the record.

    :param identifier: See :attr:`.Record.identifier`.
    :param title: See :attr:`.Record.title`.
    :param creator: (optional) The user that created the record. Defaults to the
        current user.
    :param type: (optional) See :attr:`.Record.type`.
    :param description: (optional) See :attr:`.Record.description`.
    :param license: (optional) The name of the license to reference the record with. See
        also :class:`.License`.
    :param extras: (optional) See :attr:`.Record.extras`.
    :param tags: (optional) A list of tag names to tag the record with. See also
        :class:`.Tag`.
    :param state: (optional) See :attr:`.Record.state`.
    :param visibility: (optional) See :attr:`.Record.visibility`.
    :return: The created record or ``None`` if the record could not be created.
    """
    creator = creator if creator is not None else current_user
    license = License.query.filter_by(name=license).first()

    record = Record.create(
        creator=creator,
        identifier=identifier,
        title=title,
        type=type,
        description=description,
        plain_description=strip_markdown(description),
        license=license,
        extras=extras,
        state=state,
        visibility=visibility,
    )

    if tags is not None:
        record.set_tags(tags)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return None

    setup_permissions("record", record.id)
    add_role(creator, "record", record.id, "admin")

    create_revision(record, user=creator)

    return record


def update_record(record, tags=None, **kwargs):
    r"""Update an existing record.

    :param record: The record to update.
    :param tags: (optional) A list of tag names to tag the record with. See also
        :class:`.Tag`.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`. If the name of a license is given via
        ``license``, the reference to the license object will be updated accordingly.
    :return: ``True`` if the record was updated successfully, ``False`` otherwise.
    """
    if record.state != "active":
        return False

    if kwargs.get("license") is not None:
        kwargs["license"] = License.query.filter_by(name=kwargs["license"]).first()

    update_object(record, **kwargs)

    if "description" in kwargs:
        record.plain_description = strip_markdown(kwargs["description"])

    if tags is not None:
        record.set_tags(tags)

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    create_revision(record)

    return True


def delete_record(record):
    """Delete an existing record.

    This will perform a soft deletion, i.e. the records's state will be set to
    ``"deleted"``.

    :param record: The record to delete.
    """
    record.state = "deleted"
    create_revision(record)


def restore_record(record):
    """Restore a deleted record.

    :param record: The record to restore.
    """
    if record.state == "deleted":
        record.state = "active"
        create_revision(record)


def purge_record(record):
    """Purge an existing record.

    This will completely delete the record from the database including all its files.

    Note that this function may issue one or more database commits.

    :param record: The record to delete.
    """
    record.collections = []

    record.revisions.delete(synchronize_session="fetch")

    delete_permissions("record", record.id)
    remove_files(record.files)

    temporary_files = TemporaryFile.query.filter(TemporaryFile.record_id == record.id)
    remove_temporary_files(temporary_files)

    uploads = Upload.query.filter(Upload.record_id == record.id)
    remove_uploads(uploads)

    db.session.delete(record)


def _make_extra_key_query(extra_type, extra_key):
    should_query = []

    # Check if the value should be matched exactly.
    if extra_key.startswith('"') and extra_key.endswith('"') and len(extra_key) >= 2:
        extra_key = extra_key[1:-1]
    else:
        should_query.append(Q("match", **{f"extras_{extra_type}.key": extra_key}))

    should_query.append(Q("term", **{f"extras_{extra_type}.key.keyword": extra_key}))

    return Q("bool", should=should_query)


def _make_nested_extra_key_query(extra_type, extra_key):
    should_query = []

    # Check if the value should be matched exactly.
    if extra_key.startswith('"') and extra_key.endswith('"') and len(extra_key) >= 2:
        extra_key = extra_key[1:-1]
    else:
        should_query.append(
            Q(
                "nested",
                path=f"extras_{extra_type}",
                query=Q("match", **{f"extras_{extra_type}.key": extra_key}),
            )
        )

    should_query.append(
        Q(
            "nested",
            path=f"extras_{extra_type}",
            query=Q("term", **{f"extras_{extra_type}.key.keyword": extra_key}),
        )
    )

    return Q("bool", should=should_query)


def _dict_to_query(query_dict):
    extra_type = query_dict.get("type")
    extra_key = query_dict.get("key")

    if extra_type == "bool":
        bool_query = []
        bool_value = query_dict.get("bool")

        if bool_value in ["true", True]:
            bool_query.append(Q("term", extras_bool__value=True))
        elif bool_value in ["false", False]:
            bool_query.append(Q("term", extras_bool__value=False))

        if extra_key:
            bool_query.append(_make_extra_key_query("bool", extra_key))

        return Q("nested", path="extras_bool", query=Q("bool", must=bool_query))

    if extra_type == "date":
        date_query = []
        date_min = query_dict.get("date", {}).get("min")
        date_max = query_dict.get("date", {}).get("max")

        if date_min:
            date_query.append(Q("range", extras_date__value={"gt": date_min}))

        if date_max:
            date_query.append(Q("range", extras_date__value={"lt": date_max}))

        if extra_key:
            date_query.append(_make_extra_key_query("date", extra_key))

        return Q("nested", path="extras_date", query=Q("bool", must=date_query))

    if extra_type == "numeric":
        int_query = []
        float_query = []

        num_min = query_dict.get("numeric", {}).get("min")
        num_max = query_dict.get("numeric", {}).get("max")
        num_unit = query_dict.get("numeric", {}).get("unit")

        if num_min:
            int_query.append(Q("range", extras_int__value={"gt": num_min}))
            float_query.append(Q("range", extras_float__value={"gt": num_min}))

        if num_max:
            int_query.append(Q("range", extras_int__value={"lt": num_max}))
            float_query.append(Q("range", extras_float__value={"lt": num_max}))

        if num_unit:
            int_query.append(Q("match", extras_int__unit=num_unit))
            float_query.append(Q("match", extras_float__unit=num_unit))

        if extra_key:
            int_query.append(_make_extra_key_query("int", extra_key))
            float_query.append(_make_extra_key_query("float", extra_key))

        return Q(
            "bool",
            should=[
                Q("nested", path="extras_int", query=Q("bool", must=int_query)),
                Q("nested", path="extras_float", query=Q("bool", must=float_query)),
            ],
        )

    if extra_type == "str":
        str_query = []
        str_value = query_dict.get("str")

        if str_value:
            should_query = []

            # Check if the value should be matched exactly.
            if (
                str_value.startswith('"')
                and str_value.endswith('"')
                and len(str_value) >= 2
            ):
                str_value = str_value[1:-1]
            else:
                should_query.append(Q("match", extras_str__value=str_value))

            should_query.append(Q("term", extras_str__value__keyword=str_value))
            str_query.append(Q("bool", should=should_query))

        if extra_key:
            str_query.append(_make_extra_key_query("str", extra_key))

        return Q("nested", path="extras_str", query=Q("bool", must=str_query))

    if extra_key:
        return Q(
            "bool",
            should=[
                _make_nested_extra_key_query(extra_type, extra_key)
                for extra_type in ["bool", "date", "int", "float", "str"]
            ],
        )

    return None


def search_records(
    query,
    extras=None,
    page=1,
    per_page=10,
    sort="_score",
    highlight=False,
    tags=None,
    record_types=None,
    mimetypes=None,
    records_query=None,
):
    """Convenience function to search for and filter records.

    Uses :func:`kadi.lib.resources.utils.search_resources`.

    :param query: The search query as string to search for the title, identifier and
        plain description of the record.
    :param extras: (optional) A list of dictionaries to specifiy a search within the
        extra metadata. Each entry can contain a link, a key, a type and one or multiple
        values depending on the type. See also :attr:`.Record.extras`.

        **Example:**

        .. code-block:: python3

            [
                {
                    "link": "<link>", # One of "and" or "or"
                    "key": "<key>",
                    "type": "<type>", # One of "bool", "date", "numeric" or "str"
                    "bool": True, # One of True, "true", False or "false"
                    "date": {
                        "min": "2020-07-01T00:00:00.000Z",
                        "max": "2020-07-02T00:00:00.000Z",
                    },
                    "numeric": {"min": 0, "max": 1, "unit": "cm"},
                    "str": "string",
                }
            ]

    :param page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param per_page: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param sort: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param highlight: (optional) See :func:`kadi.lib.resources.utils.search_resources`.
    :param tags: (optional) A list of tag names to filter the records with before
        searching. All given tags are filtered using an *OR* operation.
    :param record_types: (optional) A list of record types to filter the records with
        before searching. All given types are filtered using an *OR* operation.
    :param mimetypes: (optional) A list of MIME types to filter the records with before
        searching based on a record's files. All given MIME types are filtered using an
        *OR* operation.
    :param records_query: (optional) The base query to filter the search results with.
        Defaults to a query containing all records the current user has permission to
        read.
    :return: The search results as returned by
        :func:`kadi.lib.resources.utils.search_resources`.
    """
    if not records_query:
        records_query = get_permitted_objects(current_user, "read", "record").active()

    if tags:
        records_query = records_query.join(Record.tags).filter(Tag.name.in_(tags))

    if record_types:
        records_query = records_query.filter(Record.type.in_(record_types))

    if mimetypes:
        records_query = records_query.join(Record.files).filter(
            File.mimetype.in_(mimetypes), File.state == "active"
        )

    record_ids = records_query.with_entities(Record.id)
    record_ids = [record_id[0] for record_id in record_ids]

    query_str = query
    if query_str:
        basic_fields = ["identifier", "title", "plain_description"]
        query = Q("multi_match", query=query_str, fields=basic_fields, fuzziness="AUTO")

    if extras:
        q_or_relations = []
        q_and_relations = []

        # Multiple queries with different link types are effectively combined as:
        # (Q1 AND Q2) OR (Q3 AND Q4). The first link type does not actually matter.
        for extra in extras:
            extra_query = _dict_to_query(extra)

            if extra_query:
                if extra.get("link") == "or":
                    if q_and_relations:
                        q_or_relations.append(Q("bool", must=q_and_relations))

                    q_and_relations = [extra_query]
                else:
                    q_and_relations.append(extra_query)

        q_or_relations.append(Q("bool", must=q_and_relations))
        extras_query = Q("bool", should=q_or_relations)

        # The general query string is combined using an AND operation if given.
        if query_str:
            query = Q("bool", must=[query, extras_query])
        else:
            query = extras_query

    return search_resources(
        Record,
        query=query,
        page=page,
        per_page=per_page,
        sort=sort,
        filter_ids=record_ids,
        highlight=highlight,
    )
