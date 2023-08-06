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
from kadi.modules.workflows.models import Workflow
from kadi.modules.workflows.schemas import WorkflowSchema


route = partial(bp.route, methods=["POST"])


@route("/workflows", v=None)
@login_required
@internal_endpoint
def new_workflow():
    """Create a new workflow."""
    schema = WorkflowSchema()

    workflow = Workflow.create(creator=current_user, **schema.load_or_400())
    db.session.commit()

    return json_response(201, schema.dump(workflow))
