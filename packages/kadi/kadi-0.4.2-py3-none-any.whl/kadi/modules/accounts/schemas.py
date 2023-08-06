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
from marshmallow import fields
from marshmallow import post_dump

from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for


class IdentitySchema(KadiSchema):
    """Schema to represent identities.

    See :class:`.Identity`.
    """

    type = fields.String(dump_only=True, data_key="identity_type")

    displayname = fields.String(dump_only=True)

    username = fields.String(dump_only=True)

    identity_name = fields.Method("_get_identity_name")

    email = fields.Method("_get_email")

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "email" in data and data["email"] is None:
            del data["email"]

        return data

    def _get_identity_name(self, obj):
        return obj.Meta.identity_type["name"]

    def _get_email(self, obj):
        if obj.user == current_user or not obj.user.email_is_private:
            return obj.email

        return None


class UserSchema(KadiSchema):
    """Schema to represent users.

    See :class:`.User`.
    """

    id = fields.Integer(required=True)

    about = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    state = fields.String(dump_only=True)

    identity = fields.Nested(IdentitySchema, dump_only=True)

    _links = fields.Method("_generate_links")

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_user", id=obj.id),
            "identities": url_for("api.get_user_identities", id=obj.id),
            "records": url_for("api.get_user_records", id=obj.id),
            "collections": url_for("api.get_user_collections", id=obj.id),
            "groups": url_for("api.get_user_groups", id=obj.id),
            "templates": url_for("api.get_user_templates", id=obj.id),
        }

        if obj.image_name:
            links["image"] = url_for("api.preview_user_image", id=obj.id)

        if self._internal:
            links["view"] = url_for("accounts.view_user", id=obj.id, _external=True)

        return links
