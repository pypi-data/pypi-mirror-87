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


def strip(string):
    """Strip all surrounding whitespaces in a string.

    Wrapper for Python's ``strip`` function which allows passing ``None``.

    :param string: The string to strip.
    :return: The stripped string copy or ``None`` if the input was ``None`` as well.
    """
    if string is not None:
        string = string.strip()

    return string


def normalize(string):
    """Normalize all whitespaces in a string.

    Will strip surrounding whitespaces of the copy and normalize all other whitespaces
    to exactly one single whitespace each.

    :param string: The string to normalize.
    :return: The normalized string copy or ``None`` if the input was ``None`` as well.
    """
    if string is not None:
        string = " ".join(string.split())

    return string


def lower(string):
    """Lowercase all characters in a string.

    Wrapper for Python's ``lower`` function which allows passing ``None``.

    :param string: The string to lowercase.
    :return: The lowercased string copy or ``None`` if the input was ``None`` as well.
    """
    if string is not None:
        string = string.lower()

    return string


def markdown_to_html(string):
    """Render a markdown string as HTML.

    :param string: The string to render.
    :return: The rendered string or ``None`` if the input was ``None`` as well.
    """
    if string is not None:
        string = markdown(string, extensions=["tables"])

    return string


def strip_markdown(string):
    """Strip a string of its markdown directives.

    May not strip all tags, since some allowed (i.e. rendered) tags may not be standard
    markdown and are therefore not included in the library used to render the tags here.

    :param string: The string to strip.
    :return: The stripped string copy or ``None`` if the input was ``None`` as well.
    """
    if string is not None:
        # First, escape the string to preserve manually entered HTML.
        string = Markup.escape(string)
        # Second, render markdown tags.
        string = markdown_to_html(string)
        # Third, strip resulting HTML tags, newlines and normalize whitespace.
        string = Markup.striptags(string)
        # Finally, undo the first step by unescaping.
        string = Markup.unescape(string)

    return string


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
