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
from flask_login import current_user
from sqlalchemy import null
from sqlalchemy.dialects.postgresql import JSONB

from .models import Revision
from .utils import get_revision_columns
from kadi.ext.db import db
from kadi.lib.conversion import to_primitive_type
from kadi.lib.db import get_class_by_tablename
from kadi.lib.db import get_column_type
from kadi.lib.db import is_many_relationship
from kadi.lib.utils import rgetattr
from kadi.lib.utils import SimpleReprMixin


def _has_changes(obj, parent, columns, relationships):
    if parent is None:
        return True

    for column in columns:
        if getattr(obj, column) != getattr(parent, column):
            return True

    for relationship, attrs in relationships:
        relationship_obj = getattr(obj, relationship)

        # Get a list of dictionaries of all revisioned relationship columns.
        if is_many_relationship(obj.__class__, relationship):
            # Always order by ID to get predictable results.
            relationship_objs = relationship_obj.order_by("id")

            values = []
            for relationship_obj in relationship_objs:
                values_dict = {}
                for attr in attrs:
                    values_dict[attr] = to_primitive_type(
                        getattr(relationship_obj, attr)
                    )

                values.append(values_dict)

        # Get a dictionary of all revisioned relationship columns or None in case the
        # object is None as well.
        else:
            if relationship_obj is None:
                values = None
            else:
                values = {}
                for attr in attrs:
                    values[attr] = to_primitive_type(getattr(relationship_obj, attr))

        if values != getattr(parent, relationship):
            return True

    return False


def create_revision(obj, user=None):
    """Create a new revision of an object that supports revisioning.

    If none of the revisioned values changed, no new revision will be created.

    See also :func:`kadi.lib.revisions.core.setup_revisions`.

    :param obj: The object to create a new revision for.
    :param user: (optional) The user that triggered the revision. Defaults to the
        current user.
    """
    columns, relationships = get_revision_columns(obj.__class__)
    parent = (
        obj._revision_class.query.join(Revision)
        .join(obj.__class__)
        .filter(obj.__class__.id == obj.id)
        .order_by(Revision.id.desc())
        .first()
    )

    # Check if any of the revisioned values changed.
    if not _has_changes(obj, parent, columns, relationships):
        return

    user = user if user is not None else current_user

    revision = Revision.create(user=user)
    object_revision = obj._revision_class()

    object_revision.revision = revision
    object_revision.parent = parent
    setattr(object_revision, obj.__tablename__, obj)

    for column in columns:
        setattr(object_revision, column, getattr(obj, column))

    for relationship, attrs in relationships:
        relationship_obj = getattr(obj, relationship)

        # Save a list of dictionaries of all revisioned relationship columns.
        if is_many_relationship(obj.__class__, relationship):
            # Always order by ID to get predictable results.
            relationship_objs = relationship_obj.order_by("id")

            values = []
            for relationship_obj in relationship_objs:
                values_dict = {}
                for attr in attrs:
                    values_dict[attr] = to_primitive_type(
                        getattr(relationship_obj, attr)
                    )

                values.append(values_dict)

        # Save a dictionary of all revisioned relationship columns or None in case the
        # object is None as well.
        else:
            if relationship_obj is None:
                # We have to use this special null value, since the normal None value
                # will be represented as a JSON null value otherwise.
                values = null()
            else:
                values = {}
                for attr in attrs:
                    values[attr] = to_primitive_type(getattr(relationship_obj, attr))

        setattr(object_revision, relationship, values)

    db.session.add(object_revision)


def _make_revision_model(model, classname, tablename):
    columns, relationships = get_revision_columns(model)
    model_tablename = model.__tablename__

    class_dict = {
        "__tablename__": tablename,
        "Meta": type(
            "Meta",
            (),
            {"representation": (["id", "revision_id", model_tablename + "_id"])},
        ),
        "_model_class": model,
        "id": db.Column(db.Integer, primary_key=True),
        "revision_id": db.Column(
            db.Integer, db.ForeignKey("revision.id"), nullable=False
        ),
        model_tablename
        + "_id": db.Column(
            get_column_type(model, "id"),
            db.ForeignKey(model_tablename + ".id"),
            nullable=False,
        ),
        tablename
        + "_id": db.Column(db.Integer, db.ForeignKey(tablename + ".id"), nullable=True),
        model_tablename: db.relationship(model.__name__),
        "revision": db.relationship("Revision"),
        "parent": db.relationship(classname, remote_side=classname + ".id"),
    }

    for column in columns:
        if column not in class_dict:
            class_dict[column] = db.Column(
                get_column_type(model, column), nullable=True
            )

    for relationship, _ in relationships:
        if relationship not in class_dict:
            # We simply use JSON to store the relationship values.
            class_dict[relationship] = db.Column(JSONB, nullable=True)

    return type(classname, (SimpleReprMixin, db.Model), class_dict)


def setup_revisions():
    """Setup revisioning for all models that support it.

    The columns to store revisions of have to be specified in a ``Meta.revision``
    attribute in each model. It should be a list of strings specifying the attribute
    names.

    **Example:**

    .. code-block:: python3

        class Foo:
            class Meta:
                revision = ["bar", "baz[foo, bar]"]

    The columns can either be simple columns, like the first value in the list, or
    relationships like the second value. For the latter, all columns of the relationship
    that should be included in the revision need to be specified in square brackets,
    separated by commas.

    For each model, a new model class for the revisions will be created automatically,
    linked to the original model class and to :class:`.Revision`. The revision model
    class will also be stored on the original model as ``_revision_class``.
    """
    tablenames = list(db.metadata.tables.keys())

    for tablename in tablenames:
        model = get_class_by_tablename(tablename)

        if rgetattr(model, "Meta.revision", None) is not None:
            classname = model.__name__ + "Revision"
            tablename = model.__tablename__ + "_revision"

            # Stops SQLAlchemy from complaining on server reload.
            if db.metadata.tables.get(tablename) is not None:
                return

            revision_model = _make_revision_model(model, classname, tablename)

            model._revision_class = revision_model
            model.revisions = db.relationship(revision_model, lazy="dynamic")
