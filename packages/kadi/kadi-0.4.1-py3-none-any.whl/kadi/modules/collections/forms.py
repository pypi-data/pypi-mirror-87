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
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length

from .models import Collection
from kadi.ext.db import db
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.forms import check_duplicate_identifier
from kadi.lib.forms import DynamicMultiSelectField
from kadi.lib.forms import DynamicSelectField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import TagsField
from kadi.lib.forms import validate_identifier
from kadi.lib.tags.models import Tag
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.permissions.core import has_permission
from kadi.modules.records.models import Record


class BaseCollectionForm(KadiForm):
    """Base form class for use in creating or updating collections.

    :param collection: (optional) A collection used for prefilling the form.
    """

    title = StringField(
        _l("Title"),
        filters=[strip, normalize],
        validators=[
            DataRequired(),
            Length(max=Collection.Meta.check_constraints["title"]["length"]["max"]),
        ],
    )

    identifier = StringField(
        _l("Identifier"),
        filters=[strip, lower],
        validators=[
            DataRequired(),
            Length(
                max=Collection.Meta.check_constraints["identifier"]["length"]["max"]
            ),
            validate_identifier,
        ],
        description=_l("Unique identifier of this collection."),
    )

    description = LFTextAreaField(
        _l("Description"),
        validators=[
            Length(
                max=Collection.Meta.check_constraints["description"]["length"]["max"]
            )
        ],
    )

    visibility = SelectField(
        _l("Visibility"),
        choices=[
            (v, v.capitalize())
            for v in Collection.Meta.check_constraints["visibility"]["values"]
        ],
        description=_l(
            "Public visibility makes the content of this collection visible to every"
            " logged in user. Fine granular permissions can be specified later on."
        ),
    )

    tags = TagsField(
        _l("Tags"),
        max_len=Tag.Meta.check_constraints["name"]["length"]["max"],
        description=_l(
            "An optional list of keywords further describing the collection."
        ),
    )

    def __init__(self, *args, collection=None, **kwargs):
        data = None
        if collection is not None:
            data = {
                "title": collection.title,
                "identifier": collection.identifier,
                "description": collection.description,
                "visibility": collection.visibility,
            }

        super().__init__(*args, data=data, **kwargs)

        if self.is_submitted():
            self.tags.initial = [(tag, tag) for tag in sorted(self.tags.data)]
        elif collection is not None:
            self._fields["tags"].initial = [
                (tag.name, tag.name) for tag in collection.tags.order_by("name")
            ]


class NewCollectionForm(BaseCollectionForm):
    """A form for use in creating new collections.

    :param collection: (optional) See :class:`BaseCollectionForm`.
    :param user: (optional) A user that will be used for checking various permissions
        when prefilling the form. Defaults to the current user.
    """

    linked_records = DynamicMultiSelectField(
        _l("Linked records"),
        coerce=int,
        description=_l("Link this collection with one or multiple records."),
    )

    copy_permission = DynamicSelectField(
        _l("Permissions"),
        coerce=int,
        description=_l(
            "Copy the permissions of another collection. Note that only group roles of"
            " readable groups are copied."
        ),
    )

    submit = SubmitField(_l("Create Collection"))

    def __init__(self, *args, collection=None, user=None, **kwargs):
        user = user if user is not None else current_user

        # If the user has no permission to read the collection we just set it to None,
        # so it will also get passed like this to the base form.
        if collection is not None and not has_permission(
            user, "read", "collection", collection.id
        ):
            collection = None

        super().__init__(*args, collection=collection, **kwargs)

        permitted_records = (
            get_permitted_objects(user, "read", "record")
            .intersect(get_permitted_objects(user, "link", "record"))
            .filter(Record.state == "active")
            .with_entities(Record.id)
        )
        permitted_record_ids = [r.id for r in permitted_records]

        # Set the initial values of the dynamic selections based on the submitted form
        # data.
        if self.is_submitted():
            if self.linked_records.data:
                records = Record.query.filter(
                    db.and_(
                        Record.id.in_(permitted_record_ids),
                        Record.id.in_(self.linked_records.data),
                    )
                )
                self.linked_records.initial = [
                    (r.id, "@" + r.identifier) for r in records
                ]

            if self.copy_permission.data:
                collection = Collection.query.get(self.copy_permission.data)
                if collection is not None and has_permission(
                    user, "read", "collection", collection.id
                ):
                    self.copy_permission.initial = (
                        collection.id,
                        "@" + collection.identifier,
                    )

        # Set the initial values of the dynamic selections based on the given
        # arguments.
        elif collection is not None:
            records = collection.records.filter(Record.id.in_(permitted_record_ids))
            self._fields["linked_records"].initial = [
                (r.id, "@" + r.identifier) for r in records
            ]

            self._fields["copy_permission"].initial = (
                collection.id,
                "@" + collection.identifier,
            )

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(identifier, Collection)


class EditCollectionForm(BaseCollectionForm):
    """A form for use in editing existing collections.

    :param collection: The collection to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    def __init__(self, collection, *args, **kwargs):
        self.collection = collection
        super().__init__(*args, collection=collection, **kwargs)

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(identifier, Collection, exclude=self.collection)


class LinkRecordsForm(KadiForm):
    """A form for use in linking collections with records."""

    records = DynamicMultiSelectField(
        _l("Records"), validators=[DataRequired()], coerce=int
    )

    submit = SubmitField(_l("Link records"))


class AddPermissionsBaseForm(KadiForm):
    """Base form class for use in adding user or group roles concerning collections."""

    users = DynamicMultiSelectField(_l("Users"), coerce=int)

    groups = DynamicMultiSelectField(_l("Groups"), coerce=int)

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators=extra_validators)

        if success and (self.users.data or self.groups.data):
            return True

        return False


class AddCollectionPermissionsForm(AddPermissionsBaseForm):
    """A form for use in adding user or group roles to a collection."""

    role = SelectField(
        _l("Role"),
        choices=[(r, r.capitalize()) for r, _ in Collection.Meta.permissions["roles"]],
    )

    submit = SubmitField(_l("Add permissions"))


class AddRecordsPermissionsForm(AddPermissionsBaseForm):
    """A form for use in adding or removing user or group roles of linked records."""

    records = DynamicMultiSelectField(_l("Records"), coerce=int)

    role = SelectField(
        _l("Role"),
        choices=[("", "")]
        + [(r, r.capitalize()) for r, _ in Record.Meta.permissions["roles"]],
    )

    submit = SubmitField(_l("Apply permissions"))
