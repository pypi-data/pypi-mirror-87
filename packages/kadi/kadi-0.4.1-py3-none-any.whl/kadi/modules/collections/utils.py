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

from flask_login import current_user

from .schemas import CollectionSchema
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import Record
from kadi.modules.records.utils import get_export_data as get_record_export_data


def get_export_data(collection, export_type=None):
    """Export the (meta)data of a collection and its records in a given format.

    :param collection: The collection to export.
    :param export_type: (optional) The export format, currently only ``"json"``. If not
        given, defaults to the "raw" serialized data.
    :return: The exported data.
    """
    schema = CollectionSchema(exclude=["_actions", "_links", "creator._links"])
    data = schema.dump(collection)

    record_ids = (
        get_permitted_objects(current_user, "read", "record")
        .active()
        .with_entities(Record.id)
    )

    data["records"] = []
    for record in collection.records.filter(Record.id.in_(record_ids)):
        record_data = get_record_export_data(record)
        data["records"].append(record_data)

    if export_type == "json":
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)

    return data
