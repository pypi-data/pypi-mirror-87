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
import os
from functools import partial

from flask import abort
from flask import send_file
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.storage.misc import create_misc_uploads_path
from kadi.lib.web import qparam
from kadi.modules.groups.models import Group
from kadi.modules.permissions.core import permission_required


route = partial(bp.route, methods=["GET"])


@route("/groups/<int:id>/image", v=None)
@permission_required("read", "group", "id")
@internal_endpoint
def preview_group_image(id):
    """Download a group's image thumbnail for direct preview in the browser."""
    group = Group.query.get_active_or_404(id)

    if group.image_name:
        filepath = create_misc_uploads_path(str(group.image_name))

        if os.path.isfile(filepath):
            return send_file(filepath, mimetype="image/jpeg")

    abort(404)


@route("/groups/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
@qparam("exclude", [], multiple=True, type=int)
@qparam("action", ["read"], multiple=True)
def select_groups(qparams):
    """Search groups in dynamic selections.

    See :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    return get_selected_resources(
        Group,
        page=qparams["page"],
        term=qparams["term"],
        exclude=qparams["exclude"],
        actions=qparams["action"],
    )
