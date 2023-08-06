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

from .models import File
from .schemas import FileSchema
from .schemas import RecordSchema


def get_export_data(record, export_type=None):
    """Export the (meta)data of a record and its files in a given format.

    :param record: The record to export.
    :param export_type: (optional) The export format, currently only ``"json"``. If not
        given, defaults to the "raw" serialized data.
    :return: The exported data.
    """
    schema = RecordSchema(exclude=["_actions", "_links", "creator._links"])
    data = schema.dump(record)

    schema = FileSchema(many=True, exclude=["_actions", "_links", "creator._links"])
    data["files"] = schema.dump(record.active_files.order_by(File.last_modified.desc()))

    if export_type == "json":
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)

    return data
