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
from flask import current_app
from flask import render_template
from flask import send_file
from flask_login import login_required

from kadi.ext.db import db
from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.storage.misc import create_misc_uploads_path
from kadi.lib.web import qparam
from kadi.modules.accounts.models import User


route = partial(bp.route, methods=["GET"])


@route("/users/<int:id>/image", v=None)
@login_required
@internal_endpoint
def preview_user_image(id):
    """Download a users's image thumbnail for direct preview in the browser."""
    user = User.query.get_or_404(id)
    if user.is_merged:
        abort(404)

    if user.image_name:
        filepath = create_misc_uploads_path(str(user.image_name))

        if os.path.isfile(filepath):
            return send_file(filepath, mimetype="image/jpeg")

    abort(404)


@route("/users/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
@qparam("exclude", [], multiple=True, type=int)
def select_users(qparams):
    """Search users in dynamic selections.

    Similar to :func:`kadi.lib.resources.api.get_selected_resources`. Note that
    technically identities are returned, not users. Therefore, users with multiple
    identities may be included multiple times.
    """
    identity_queries = []
    for provider_config in current_app.config["AUTH_PROVIDERS"].values():
        model = provider_config["identity_class"]
        identities_query = (
            model.query.join(User, User.id == model.user_id)
            .filter(
                db.or_(
                    model.displayname.ilike(f"%{qparams['term']}%"),
                    model.username.ilike(f"%{qparams['term']}%"),
                ),
                model.user_id.notin_(qparams["exclude"]),
                User.state == "active",
            )
            .with_entities(
                model.displayname.label("displayname"),
                model.username,
                model.user_id,
                db.literal(model.Meta.identity_type["name"]).label("type"),
            )
        )

        identity_queries.append(identities_query)

    identities = (
        identity_queries[0]
        .union(*identity_queries[1:])
        .order_by("displayname")
        .paginate(qparams["page"], 10, False)
    )

    data = {"results": [], "pagination": {"more": identities.has_next}}
    for identity in identities.items:
        data["results"].append(
            {
                "id": identity.user_id,
                "text": "@" + identity.username,
                "body": render_template(
                    "accounts/snippets/select_user.html",
                    displayname=identity.displayname,
                    username=identity.username,
                    type=identity.type,
                ),
            }
        )

    return json_response(200, data)
