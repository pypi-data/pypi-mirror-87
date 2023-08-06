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
from kadi.modules.collections.core import purge_collection as _purge_collection
from kadi.modules.collections.core import restore_collection as _restore_collection
from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema


route = partial(bp.route, methods=["POST"])


@route("/collections/<int:id>/restore", v=None)
@login_required
@internal_endpoint
def restore_collection(id):
    """Restore a deleted collection."""
    collection = Collection.query.get_or_404(id)

    if collection.state != "deleted" or current_user != collection.creator:
        abort(404)

    _restore_collection(collection)
    db.session.commit()

    schema = CollectionSchema()
    collection = schema.dump(collection)

    return json_response(200, collection)


@route("/collections/<int:id>/purge", v=None)
@login_required
@internal_endpoint
def purge_collection(id):
    """Purge a deleted collection."""
    collection = Collection.query.get_or_404(id)

    if collection.state != "deleted" or current_user != collection.creator:
        abort(404)

    _purge_collection(collection)
    db.session.commit()

    return json_response(204)
