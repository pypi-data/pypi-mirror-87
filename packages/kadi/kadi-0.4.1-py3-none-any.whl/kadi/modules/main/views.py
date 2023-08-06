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

from .blueprint import bp
from kadi.ext.db import db
from kadi.modules.collections.models import Collection
from kadi.modules.groups.models import Group
from kadi.modules.groups.utils import get_user_groups
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import Record
from kadi.version import __version__


@bp.route("/")
def index():
    """The index/home page.

    Will change depending on whether the current user is authenticated or not.
    """
    if not current_user.is_authenticated:
        return render_template("main/index.html", version=__version__)

    records_query = get_permitted_objects(current_user, "read", "record")
    collections_query = get_permitted_objects(current_user, "read", "collection")

    resource_queries = []
    for model, query, endpoint in [
        (Record, records_query, "records.view_record"),
        (Collection, collections_query, "collections.view_collection"),
    ]:
        resources_query = query.with_entities(
            model.id,
            model.title,
            model.identifier,
            model.plain_description,
            model.visibility,
            model.last_modified.label("last_modified"),
            db.literal(model.__tablename__).label("type"),
            db.literal(endpoint).label("endpoint"),
        ).filter(model.state == "active")

        resource_queries.append(resources_query)

    resources = (
        resource_queries[0]
        .union(*resource_queries[1:])
        .order_by(db.desc("last_modified"))
        .limit(6)
    )

    # No need to filter permitted groups, as the current user will have at least read
    # permission for their own groups.
    paginated_groups = (
        get_user_groups(current_user)
        .order_by(Group.last_modified.desc())
        .paginate(1, 4, False)
    )

    return render_template(
        "main/home.html",
        title=_("Home"),
        groups=paginated_groups.items,
        has_more_groups=paginated_groups.has_next,
        latest_updates=resources.all(),
    )


@bp.route("/about")
def about():
    """The about page."""
    return render_template("main/about.html", title=_("About"), version=__version__)


@bp.route("/help")
def help():
    """The help page."""
    return render_template("main/help.html", title=_("Help"))
