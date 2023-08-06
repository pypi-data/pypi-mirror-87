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
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

from .models import Template
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.forms import check_duplicate_identifier
from kadi.lib.forms import DynamicMultiSelectField
from kadi.lib.forms import DynamicSelectField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import SelectField
from kadi.lib.forms import TagsField
from kadi.lib.forms import validate_identifier
from kadi.lib.licenses.models import License
from kadi.lib.tags.models import Tag
from kadi.modules.records.models import Record


class BaseTemplateForm(KadiForm):
    """Base form class for use in creating or updating templates.

    :param template: (optional) A template used for prefilling the form.
    """

    title = StringField(
        _l("Title"),
        filters=[strip, normalize],
        validators=[
            DataRequired(),
            Length(max=Template.Meta.check_constraints["title"]["length"]["max"]),
        ],
    )

    identifier = StringField(
        _l("Identifier"),
        filters=[lower, strip],
        validators=[
            DataRequired(),
            Length(max=Template.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
        description=_l("Unique identifier of this template."),
    )

    def __init__(self, *args, template=None, data=None, **kwargs):
        if template is not None:
            if data is not None:
                data["title"] = template.title
                data["identifier"] = template.identifier
            else:
                data = {"title": template.title, "identifier": template.identifier}

        super().__init__(*args, data=data, **kwargs)


class NewTemplateFormMixin:
    """Mixin class for forms used in creating new templates."""

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(identifier, Template)


class EditTemplateFormMixin:
    """Mixin class for forms used in editing existing templates."""

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(identifier, Template, exclude=self.template)


class BaseRecordTemplateForm(BaseTemplateForm):
    """Base form class for use in creating or updating record templates.

    :param template: (optional) See :class:`BaseTemplateForm`.
    """

    record_title = StringField(
        _l("Title"),
        filters=[strip, normalize],
        validators=[
            Length(max=Record.Meta.check_constraints["title"]["length"]["max"])
        ],
    )

    record_identifier = StringField(
        _l("Identifier"),
        filters=[lower, strip],
        validators=[
            Length(max=Record.Meta.check_constraints["identifier"]["length"]["max"])
        ],
        description=_l("Unique identifier of a record."),
    )

    record_type = DynamicSelectField(
        _l("Type"),
        filters=[strip, normalize],
        validators=[Length(max=Record.Meta.check_constraints["type"]["length"]["max"])],
        description=_l("Optional type of a record, e.g. dataset, device, etc."),
    )

    record_description = LFTextAreaField(
        _l("Description"),
        validators=[
            Length(max=Record.Meta.check_constraints["description"]["length"]["max"])
        ],
    )

    record_license = DynamicSelectField(
        _l("License"),
        description=_l(
            "Specifying an optional license can determine the conditions for the"
            " correct reuse of data and metadata when the record is published or simply"
            " shared with other users. A license can also be uploaded as a file, in"
            " which case one of the 'Other' licenses can be chosen."
        ),
    )

    record_tags = TagsField(
        _l("Tags"),
        max_len=Tag.Meta.check_constraints["name"]["length"]["max"],
        description=_l("An optional list of keywords further describing the record."),
    )

    def __init__(self, *args, template=None, **kwargs):
        data = None

        if template is not None:
            data = {
                "record_title": template.data.get("title", ""),
                "record_identifier": template.data.get("identifier", ""),
                "record_description": template.data.get("description", ""),
            }

        super().__init__(*args, template=template, data=data, **kwargs)

        if self.is_submitted():
            # Make sure to convert empty string data into None to keep missing type
            # values consistent.
            if not self.record_type.data:
                self.record_type.data = None

            if self.record_type.data is not None:
                self.record_type.initial = (
                    self.record_type.data,
                    self.record_type.data,
                )

            if self.record_license.data is not None:
                license = License.query.filter_by(name=self.record_license.data).first()
                if license is not None:
                    self.record_license.initial = (license.name, license.title)

            self.record_tags.initial = [
                (tag, tag) for tag in sorted(self.record_tags.data)
            ]

        elif template is not None:
            if template.data.get("type") is not None:
                self._fields["record_type"].initial = (
                    template.data["type"],
                    template.data["type"],
                )

            if template.data.get("license") is not None:
                license = License.query.filter_by(name=template.data["license"]).first()
                if license is not None:
                    self._fields["record_license"].initial = (
                        license.name,
                        license.title,
                    )

            self._fields["record_tags"].initial = [
                (tag, tag) for tag in sorted(template.data.get("tags", []))
            ]

    def validate_record_identifier(self, record_identifier):
        # pylint: disable=missing-function-docstring
        if record_identifier.data:
            validate_identifier(self, record_identifier)

    def validate_record_license(self, record_license):
        # pylint: disable=missing-function-docstring
        if (
            record_license.data is not None
            and License.query.filter_by(name=record_license.data).first() is None
        ):
            raise ValidationError(_("Not a valid license."))


class NewRecordTemplateForm(BaseRecordTemplateForm, NewTemplateFormMixin):
    """A form for use in creating new record templates."""

    submit = SubmitField(_l("Create template"))


class EditRecordTemplateForm(BaseRecordTemplateForm, EditTemplateFormMixin):
    """A form for use in updating record templates.

    :param template: The template to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    def __init__(self, template, *args, **kwargs):
        self.template = template
        super().__init__(*args, template=template, **kwargs)


class NewExtrasTemplateForm(BaseTemplateForm, NewTemplateFormMixin):
    """A form for use in creating new extras templates."""

    submit = SubmitField(_l("Create template"))


class EditExtrasTemplateForm(BaseTemplateForm, EditTemplateFormMixin):
    """A form for use in updating extras templates.

    :param template: The template to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    def __init__(self, template, *args, **kwargs):
        self.template = template
        super().__init__(*args, template=template, **kwargs)


class AddPermissionsForm(KadiForm):
    """A form for use in adding user or group roles to a record."""

    users = DynamicMultiSelectField(_l("Users"), coerce=int)

    groups = DynamicMultiSelectField(_l("Groups"), coerce=int)

    role = SelectField(
        _l("Role"),
        choices=[(r, r.capitalize()) for r, _ in Template.Meta.permissions["roles"]],
    )

    submit = SubmitField(_l("Add permissions"))

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators=extra_validators)

        if success and (self.users.data or self.groups.data):
            return True

        return False
