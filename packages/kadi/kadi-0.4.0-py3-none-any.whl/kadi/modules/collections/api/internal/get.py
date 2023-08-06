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
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.resources.api import get_selected_resources
from kadi.lib.web import download_string
from kadi.lib.web import qparam
from kadi.modules.collections.models import Collection
from kadi.modules.collections.utils import get_export_data
from kadi.modules.permissions.core import permission_required


route = partial(bp.route, methods=["GET"])


@route("/collections/<int:id>/export/<export_type>", v=None)
@permission_required("read", "collection", "id")
@internal_endpoint
def download_collection_export(id, export_type):
    """Export and download a collection in a specific format.

    Currently only ``json`` is supported as export type.
    """
    collection = Collection.query.get_active_or_404(id)

    if export_type == "json":
        filename = collection.identifier + ".json"
        mimetype = "application/json"
    else:
        abort(404)

    data = get_export_data(collection, export_type)
    return download_string(data, filename, mimetype)


@route("/collections/select", v=None)
@login_required
@internal_endpoint
@qparam("page", 1, type=int)
@qparam("term", "")
@qparam("exclude", [], multiple=True, type=int)
@qparam("action", ["read"], multiple=True)
def select_collections(qparams):
    """Search collections in dynamic selections.

    See :func:`kadi.lib.resources.api.get_selected_resources`.
    """
    return get_selected_resources(
        Collection,
        page=qparams["page"],
        term=qparams["term"],
        exclude=qparams["exclude"],
        actions=qparams["action"],
    )
