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
from flask_babel import gettext as _
from flask_login import current_user
from flask_login import login_required

from .blueprint import bp
from .models import Workflow
from kadi.lib.web import qparam
from kadi.lib.web import url_for


@bp.route("")
@login_required
def workflows():
    """Workflow overview page."""
    return render_template(
        "workflows/workflows.html",
        title=_("Workflows"),
        js_resources={"get_workflows_endpoint": url_for("api.get_workflows")},
    )


@bp.route("/editor")
@login_required
@qparam("workflow", None, type=int)
def editor(qparams):
    """Page for the workflow editor application."""
    initial_workflow = None

    if qparams["workflow"]:
        workflow = Workflow.query.get(qparams["workflow"])
        if workflow is not None and workflow.creator == current_user:
            initial_workflow = url_for("api.get_workflow", id=workflow.id)

    return render_template(
        "workflows/editor.html",
        title=_("Workflow editor"),
        js_resources={"initial_workflow_endpoint": initial_workflow},
    )
