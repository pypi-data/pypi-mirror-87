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
from functools import partial

from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.templates.models import Template


route = partial(bp.route, methods=["GET"])


@route("/templates/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
@qparam("type", None)
def select_templates(qparams):
    """Search templates in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    templates_query = get_permitted_objects(current_user, "read", "template").filter(
        db.or_(
            Template.title.ilike(f"%{qparams['term']}%"),
            Template.identifier.ilike(f"%{qparams['term']}%"),
        )
    )

    if qparams["type"] is not None:
        templates_query = templates_query.filter(Template.type == qparams["type"])

    templates = templates_query.order_by(Template.title).paginate(
        qparams["page"], 10, False
    )

    data = {"results": [], "pagination": {"more": templates.has_next}}
    for template in templates.items:
        data["results"].append(
            {
                "id": template.id,
                "text": template.title,
                "endpoint": url_for("api.get_template", id=template.id),
            }
        )

    return json_response(200, data)
