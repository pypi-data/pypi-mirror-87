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
from marshmallow import fields
from marshmallow.validate import Length

from .models import Workflow
from kadi.lib.conversion import normalize
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import NonEmptyString
from kadi.lib.web import url_for


class WorkflowSchema(KadiSchema):
    """Schema to represent workflows.

    See :class:`.Workflow`.
    """

    id = fields.Integer(dump_only=True)

    name = NonEmptyString(
        required=True,
        filters=[normalize],
        validate=Length(max=Workflow.Meta.check_constraints["name"]["length"]["max"]),
    )

    data = fields.Dict(required=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_workflow", id=obj.id),
            "download": url_for("api.download_workflow", id=obj.id),
        }

        if self._internal:
            links["edit"] = url_for("workflows.editor", workflow=obj.id, _external=True)

        return links

    def _generate_actions(self, obj):
        return {
            "edit": url_for("api.edit_workflow", id=obj.id),
            "remove": url_for("api.remove_workflow", id=obj.id),
        }
