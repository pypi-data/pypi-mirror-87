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
from elasticsearch_dsl import Boolean
from elasticsearch_dsl import Date
from elasticsearch_dsl import Document
from elasticsearch_dsl import Double
from elasticsearch_dsl import InnerDoc
from elasticsearch_dsl import Keyword
from elasticsearch_dsl import Long
from elasticsearch_dsl import MetaField
from elasticsearch_dsl import Nested
from elasticsearch_dsl import Text

from kadi.lib.search.core import MappingMixin


class ExtraMapping(InnerDoc):
    """Base search mapping for extra record metadata.

    See :attr:`.Record.extras`.
    """

    key = Text(
        required=True,
        analyzer=MappingMixin.trigram_analyzer,
        fields={"keyword": Keyword()},
    )


class ExtraMappingBoolean(ExtraMapping):
    """Search mapping for extra record metadata as boolean.

    See :attr:`.Record.extras`.
    """

    value = Boolean()


class ExtraMappingDate(ExtraMapping):
    """Search mapping for extra record metadata as date.

    See :attr:`.Record.extras`.
    """

    value = Date(default_timezone="UTC")


class ExtraMappingFloat(ExtraMapping):
    """Search mapping for extra record metadata as float.

    Uses double values for the internal representation. See :attr:`.Record.extras`.
    """

    value = Double()

    unit = Text()


class ExtraMappingInteger(ExtraMapping):
    """Search mapping for extra record metadata as integer.

    Uses long values for the internal representation. See :attr:`.Record.extras`.
    """

    value = Long()

    unit = Text()


class ExtraMappingString(ExtraMapping):
    """Search mapping for extra record metadata as string.

    See :attr:`.Record.extras`.
    """

    value = Text(analyzer=MappingMixin.trigram_analyzer, fields={"keyword": Keyword()})


class RecordMapping(Document, MappingMixin):
    """Search mapping for records.

    See :class:`.Record`.
    """

    class Meta:
        """Container to store meta class attributes."""

        dynamic = MetaField(False)

    identifier = Text(
        required=True,
        analyzer=MappingMixin.trigram_analyzer,
        fields={"keyword": Keyword()},
    )

    title = Text(
        required=True,
        analyzer=MappingMixin.trigram_analyzer,
        fields={"keyword": Keyword()},
    )

    plain_description = Text(required=True)

    created_at = Date(required=True, default_timezone="UTC")

    last_modified = Date(required=True, default_timezone="UTC")

    extras_bool = Nested(ExtraMappingBoolean)

    extras_date = Nested(ExtraMappingDate)

    extras_float = Nested(ExtraMappingFloat)

    extras_int = Nested(ExtraMappingInteger)

    extras_str = Nested(ExtraMappingString)

    @classmethod
    def create_document(cls, obj):
        """Create a new document to be indexed in ElasticSearch

        :param obj: The object to be indexed.
        :param document: The mapping class instance.
        :return: The created document.
        """
        document = cls()
        document.meta.id = obj.id

        for attr in cls.get_attributes():
            if hasattr(obj, attr):
                setattr(document, attr, getattr(obj, attr))

        type_container = {
            "extras_bool": [],
            "extras_date": [],
            "extras_float": [],
            "extras_int": [],
            "extras_str": [],
        }

        flat_extras = _flatten_extras(obj.extras)
        for item in flat_extras:
            type_container["extras_" + item["type"]].append(item)

        for type_name, type_list in type_container.items():
            setattr(document, type_name, type_list)

        return document


def _flatten_extras(extras, key=""):
    """Flatten nested extras metadata.

    :param extras: The nested extras metadata to be recursively flattened.
    :param key: The recursively flattened extras metadata key.
    :return: A flattened copy of nested extras metadata.
    """
    flat_extras = []

    for index, item in enumerate(extras):
        if item["type"] in ["list", "dict"]:
            flat_extras += _flatten_extras(
                item["value"], key=f"{key}{item.get('key', index + 1)}."
            )
        else:
            new_item = dict(item)
            if "key" in item:
                new_item["key"] = key + item["key"]
            else:
                new_item["key"] = key + str(index + 1)

            flat_extras.append(new_item)

    return flat_extras
