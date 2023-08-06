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
import json
from functools import partial

from flask import abort
from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.conversion import strip
from kadi.lib.web import download_string
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.lib.web import url_for
from kadi.modules.workflows.models import Workflow
from kadi.modules.workflows.schemas import WorkflowSchema


route = partial(bp.route, methods=["GET"])


@route("/workflows", v=None)
@login_required
@internal_endpoint
@paginated
@qparam("filter", "", parse=strip)
def get_workflows(page, per_page, qparams):
    """Get all workflows of the current user."""
    paginated_workflows = (
        current_user.workflows.filter(Workflow.name.ilike(f"%{qparams['filter']}%"))
        .order_by(Workflow.last_modified.desc())
        .paginate(page, per_page, False)
    )

    data = {
        "items": WorkflowSchema(many=True).dump(paginated_workflows.items),
        **create_pagination_data(
            paginated_workflows.total, page, per_page, "api.get_workflows"
        ),
    }

    return json_response(200, data)


@route("/workflows/<int:id>", v=None)
@login_required
@internal_endpoint
def get_workflow(id):
    """Get a workflow."""
    workflow = Workflow.query.get_or_404(id)
    if workflow.creator != current_user:
        abort(404)

    return json_response(200, WorkflowSchema().dump(workflow))


@route("/workflows/<int:id>/download", v=None)
@login_required
@internal_endpoint
def download_workflow(id):
    """Download a workflow."""
    workflow = Workflow.query.get_or_404(id)
    if workflow.creator != current_user:
        abort(404)

    return download_string(json.dumps(workflow.data), f"{workflow.name}.flow")


@route("/workflows/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
def select_workflows(qparams):
    """Search workflows in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    workflows = (
        current_user.workflows.filter(Workflow.name.ilike(f"%{qparams['term']}%"))
        .order_by(Workflow.name)
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": workflows.has_next}}
    for workflow in workflows.items:
        data["results"].append(
            {
                "id": workflow.id,
                "text": workflow.name,
                "endpoint": url_for("api.get_workflow", id=workflow.id),
            }
        )

    return json_response(200, data)
