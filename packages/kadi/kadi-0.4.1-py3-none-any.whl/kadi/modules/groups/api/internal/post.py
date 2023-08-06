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

from flask import abort
from flask_login import current_user
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.modules.groups.core import purge_group as _purge_group
from kadi.modules.groups.core import restore_group as _restore_group
from kadi.modules.groups.models import Group
from kadi.modules.groups.schemas import GroupSchema


route = partial(bp.route, methods=["POST"])


@route("/groups/<int:id>/restore", v=None)
@login_required
@internal_endpoint
def restore_group(id):
    """Restore a deleted group."""
    group = Group.query.get_or_404(id)

    if group.state != "deleted" or current_user != group.creator:
        abort(404)

    _restore_group(group)
    db.session.commit()

    schema = GroupSchema()
    group = schema.dump(group)

    return json_response(200, group)


@route("/groups/<int:id>/purge", v=None)
@login_required
@internal_endpoint
def purge_group(id):
    """Purge a deleted group."""
    group = Group.query.get_or_404(id)

    if group.state != "deleted" or current_user != group.creator:
        abort(404)

    _purge_group(group)
    db.session.commit()

    return json_response(204)
