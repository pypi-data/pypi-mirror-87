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
from jinja2 import Markup
from markdown import markdown


def strip(value):
    """Strip all surrounding whitespaces in one or multiple strings.

    :param value: A single string or a list of strings to strip.
    :return: The stripped string(s) or ``None`` if the input was ``None`` as well.
    """
    if value is not None:
        if isinstance(value, list):
            value = [v.strip() for v in value]
        else:
            value = value.strip()

    return value


def normalize(value):
    """Normalize and strip all whitespaces in one or multiple strings.

    :param value: A single string or a list of strings to normalize.
    :return: The normalized string(s) or ``None`` if the input was ``None`` as well.
    """
    if value is not None:
        if isinstance(value, list):
            value = [" ".join(v.split()) for v in value]
        else:
            value = " ".join(value.split())

    return value


def lower(value):
    """Lowercase all characters in one or multiple strings.

    :param value: A single string or a list of strings to lowercase.
    :return: The lowercased string(s) or ``None`` if the input was ``None`` as well.
    """
    if value is not None:
        if isinstance(value, list):
            value = [v.lower() for v in value]
        else:
            value = value.lower()

    return value


def markdown_to_html(value):
    """Render a markdown string as HTML.

    :param value: The string to render.
    :return: The rendered string or ``None`` if the input was ``None`` as well.
    """
    if value is not None:
        value = markdown(value, extensions=["tables"])

    return value


def strip_markdown(value):
    """Strip a string of its markdown directives.

    May not strip all tags, since some allowed (i.e. rendered) tags may not be standard
    markdown and are therefore not included in the library used to render the tags here.

    :param value: The string to strip.
    :return: The stripped string copy or ``None`` if the input was ``None`` as well.
    """
    if value is not None:
        # First, escape the string to preserve manually entered HTML.
        value = Markup.escape(value)
        # Second, render markdown tags.
        value = markdown_to_html(value)
        # Third, strip resulting HTML tags, newlines and normalize whitespace.
        value = Markup.striptags(value)
        # Finally, undo the first step by unescaping.
        value = Markup.unescape(value)

    return value


def to_primitive_type(value):
    """Convert any non-primitive value to a string.

    The primitive types considered here are ``str``, ``int``, ``float``, ``bool``. A
    ``None`` value will also be returned as is.

    :param value: The value to convert.
    :return: The string representation of the value or the unmodified value if it is a
        primitive type or ``None``.
    """
    if value is not None and not isinstance(value, (str, int, float, bool)):
        value = str(value)

    return value


def recode_string(value, from_encoding, to_encoding="utf-8"):
    """Change the encoding of a string.

    :param value: The string value.
    :param from_encoding: The original encoding of the string.
    :param to_encoding: (optional) The target encoding of the string.
    :return: A copy of the newly encoded string or the original value if the given value
        was not a string or the recoding failed.
    """
    try:
        if isinstance(value, str):
            value = value.encode(from_encoding).decode(to_encoding)
    except UnicodeDecodeError:
        pass

    return value
