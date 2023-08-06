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
from datetime import timezone

from flask_babel import gettext as _

from kadi.lib.utils import utcnow


def durationformat(seconds):
    """Create a human-readable, translated duration string from an amount of seconds.

    Translations are only supported when having an active request context.

    :param seconds: The amount of seconds.
    :return: The formatted string.
    """
    if seconds <= 0:
        return f"0 {_('seconds')}"

    units = [
        (_("second"), _("seconds"), 60),
        (_("minute"), _("minutes"), 60),
        (_("hour"), _("hours"), 24),
        (_("day"), _("days"), 7),
        (_("week"), _("weeks"), None),
    ]

    result = ""
    current_value = new_value = seconds

    for singular, plural, factor in units:
        if factor is not None:
            new_value = current_value // factor
            current_value = current_value % factor

        if current_value > 0:
            unit = singular
            if current_value > 1:
                unit = plural

            result = f"{current_value} {unit}{', ' + result if result else ''}"

        current_value = new_value

    return result


def pretty_type_name(cls_or_string):
    """Return a pretty type name based on a class or a string.

    :param cls_or_string: A class reference (e.g. ``str``) or a corresponding string
        (e.g. ``"str"``).
    :return: The pretty type name.
    """
    type_name = cls_or_string

    if not isinstance(type_name, str):
        type_name = type_name.__name__

    if type_name == "str":
        return "string"
    if type_name == "int":
        return "integer"
    if type_name == "bool":
        return "boolean"
    if type_name == "dict":
        return "dictionary"

    return type_name


def timestamp(date_time=None, include_micro=False):
    """Build a UTC timestamp from a specific date and time.

    The timestamp will be in the form of ``"%Y%m%d%H%M%S"``.

    :param date_time: (optional) A datetime object as specified in Python's ``datetime``
        module. Defaults to the current time.
    :param include_micro: (optional) Flag indicating whether to include microseconds in
        the timestamp or not.
    :return: The timestamp as string.
    """
    fmt = "%Y%m%d%H%M%S"
    if include_micro:
        fmt += "%f"

    if date_time is None:
        date_time = utcnow()

    date_time = date_time.astimezone(timezone.utc)
    return date_time.strftime(fmt)
