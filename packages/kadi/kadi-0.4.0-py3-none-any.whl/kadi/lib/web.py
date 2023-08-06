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
from collections import OrderedDict
from functools import wraps
from io import BytesIO
from urllib.parse import urljoin
from urllib.parse import urlparse

from flask import current_app
from flask import has_request_context
from flask import request
from flask import url_for as _url_for
from flask_login import make_next_param
from werkzeug.exceptions import default_exceptions
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.routing import BaseConverter
from werkzeug.wsgi import FileWrapper


class IdentifierConverter(BaseConverter):
    """Custom URL converter for identifiers.

    Automatically uses the same conversions that are applied when creating or updating
    an identifier.
    """

    regex = r"\s*[a-zA-Z0-9-_]+\s*"

    def to_python(self, value):
        return value.strip().lower()


def paginated(page_max=None, per_page_max=100):
    """Decorator to parse paginated query parameters.

    Convenience decorator to get and parse the query parameters ``"page"`` and
    ``"per_page"`` from the current request. The former defaults to 1 while the latter
    defaults to 10 if no valid integer values were found. Both parameters will be
    injected into the decorated function as keyword arguments ``page`` and ``per_page``.

    :param page_max: (optional) The maximum possible value of the ``"page"`` parameter.
    :param per_page_max: (optional) The maximum possible value of the ``"per_page"``
        parameter.
    """

    def decorator(func):
        apidoc_meta = {"page_max": page_max, "per_page_max": per_page_max}
        if hasattr(func, "_apidoc"):
            func._apidoc["pagination"] = apidoc_meta
        else:
            func._apidoc = {"pagination": apidoc_meta}

        @wraps(func)
        def decorated_view(*args, **kwargs):
            page = request.args.get("page", 1, type=int)
            page = max(page, 1)

            if page_max is not None:
                page = min(page, page_max)

            per_page = request.args.get("per_page", 10, type=int)
            per_page = min(max(per_page, 1), per_page_max)

            kwargs["page"] = page
            kwargs["per_page"] = per_page

            return func(*args, **kwargs)

        return decorated_view

    # Decoration without parentheses.
    if callable(page_max) and per_page_max == 100:
        return paginated()(page_max)

    return decorator


def qparam(
    name, default, location=None, multiple=False, type=None, parse=None, description=""
):
    """Decorator to parse a query parameter.

    Convenience decorator to get and parse a specified query parameter from the current
    request. The decorator can be applied multiple times. Each parameter will be
    injected into the decorated function as part a dictionary inside the keyword
    argument ``qparams``. The dictionary maps each given parameter name to its
    respective value.

    :param name: The name of the parameter to inject into the decorated function. Will
        also be used as the name of the query parameter if ``location`` is not given.
    :param default: (optional) The default value to use in case the query parameter is
        missing.
    :param location: (optional) The name of the query parameter to use instead of
        ``name``.
    :param multiple: (optional) Flag indicating whether the query parameter can be
        specified multiple times and should be retrieved as list value.
    :param type: (optional) A type to coerce the value/each value of the query
        parameter into. If the coercion fails, the default value will be taken instead.
    :param parse: (optional) A function to further parse the parameter value after the
        coercion. Must take and return a single parameter value.
    :param description: (optional) A description of the query parameter, which may be
        used for generating the API documentation. Supports reST syntax.
    """

    def decorator(func):
        nonlocal location
        location = location if location is not None else name

        apidoc_meta = {
            "multiple": multiple,
            "default": default,
            "description": description,
        }

        if hasattr(func, "_apidoc"):
            if "qparams" in func._apidoc:
                func._apidoc["qparams"][location] = apidoc_meta
                func._apidoc["qparams"].move_to_end(location, last=False)
            else:
                func._apidoc["qparams"] = OrderedDict([(location, apidoc_meta)])
        else:
            func._apidoc = {"qparams": OrderedDict([(location, apidoc_meta)])}

        @wraps(func)
        def decorated_view(*args, **kwargs):
            if multiple:
                value = request.args.getlist(location, type=type)
                value = value if value else default
            else:
                value = request.args.get(location, default=default, type=type)

            if parse is not None:
                value = parse(value)

            if "qparams" in kwargs:
                kwargs["qparams"][name] = value
            else:
                kwargs["qparams"] = {name: value}

            return func(*args, **kwargs)

        return decorated_view

    return decorator


def url_for(endpoint, _ignore_version=False, **values):
    r"""Generate an URL based on a given endpoint.

    Wraps Flask's ``url_for`` function with additional support for API versioning. If
    the endpoint is an API endpoint (starting with ``"api."``) and the current request
    includes an API version, then this version will also be included in the resulting
    URL again. API URLs will also always be "external", i.e. absolute.

    :param endpoint: The endpoint (name of the function) of the URL.
    :param _ignore_version: (optional) Flag indicating whether the API version should be
        ignored when building the URL.
    :param \**values: The variable arguments of the URL rule.
    :return: The generated URL string.
    """
    from kadi.lib.api.utils import get_api_version, is_api_request

    if is_api_request():
        values["_external"] = True

        if not _ignore_version:
            api_version = get_api_version()

            if api_version is not None:
                endpoint = f"{endpoint}_v{api_version.replace('.', '_')}"

    return _url_for(endpoint, **values)


def static_url(filename):
    """Generate a static URL for a given filename.

    Will make use of the ``MANIFEST_MAPPING`` if it is defined in the application's
    configuration and if an entry exists for the given filename.

    :param filename: The name of the file to include in the URL.
    :return: The generated URL string.
    """
    manifest_mapping = current_app.config["MANIFEST_MAPPING"]

    if manifest_mapping is None:
        return url_for("static", filename=filename)

    return url_for("static", filename=manifest_mapping.get(filename, filename))


def contains_query_param(query_params, key, value=None):
    """Check if a dictionary of query parameters contains a specific key.

    :param query_params: Dictionary of query parameters containing either a single value
        or a list for each key. The values themselves are not restricted to strings.
    :param key: The parameter key.
    :param value: (optional) The parameter value to check additionally.
    """
    param_values = query_params.get(key, [])
    if param_values == []:
        return False

    if value is not None:
        if isinstance(param_values, list):
            return value in param_values

        return value == param_values

    return True


def _copy_param_value(values):
    if isinstance(values, list):
        # Creates a shallow copy of the list.
        return list(values)

    return values


def _include_query_params(query_params, **kwargs):
    for param, value in kwargs.items():
        if param in query_params:
            if not isinstance(query_params[param], list):
                query_params[param] = [query_params[param]]

            if not isinstance(value, list):
                value = [value]

            for val in value:
                query_params[param].append(val)
        else:
            query_params[param] = value

    return query_params


def _exclude_query_params(query_params, **kwargs):
    new_params = {}
    for param, value in query_params.items():
        if param in kwargs:
            excluded_value = kwargs[param]

            # None excludes all values.
            if excluded_value is None:
                continue

            if not isinstance(excluded_value, list):
                excluded_value = [excluded_value]

            if not isinstance(value, list):
                value = [value]

            new_values = []
            for val in value:
                if val not in excluded_value:
                    new_values.append(val)

            if new_values:
                new_params[param] = new_values if len(new_values) > 1 else new_values[0]
        else:
            new_params[param] = _copy_param_value(value)

    return new_params


def _toggle_query_params(query_params, **kwargs):
    for param, value in kwargs.items():
        if isinstance(value, list):
            for val in value:
                if contains_query_param(query_params, param, value=val):
                    query_params = _exclude_query_params(query_params, **{param: val})
                else:
                    query_params = _include_query_params(query_params, **{param: val})
        else:
            if contains_query_param(query_params, param, value=value):
                query_params = _exclude_query_params(query_params, **{param: value})
            else:
                query_params = _include_query_params(query_params, **{param: value})

    return query_params


def _replace_query_params(query_params, **kwargs):
    for param, value in kwargs.items():
        if contains_query_param(query_params, param):
            query_params[param] = value

    return query_params


def modify_query_params(
    query_params, include=None, exclude=None, toggle=None, replace=None
):
    """Return a modified copy of a dictionary of query parameters.

    The order of the operations is "include", "exclude", "toggle" and finally "replace".

    :param query_params: Dictionary of query parameters containing either a single value
        or a list for each key. The values themselves are not restricted to only
        strings.
    :param include: (optional) A dictionary mapping parameter keys to either single
        values or lists. Each key corresponds to a new or existing parameter key, while
        the respective values will be added to the new or to the existing key of the
        original query parameters. Adding any values to single values will create lists.
        Duplicate values will not be filtered out.
    :param exclude: (optional) A dictionary mapping parameter keys to either a single
        value, a list of values or ``None``. All given values will be excluded in the
        original query parameters. ``None`` always excludes all values of the
        corresponding key. If only a single value remains for a key, the list will be
        replaced with that value.
    :param toggle: (optional) A dictionary mapping parameter keys to either single
        values or lists. For each key/value pair either an "include" or an "exclude"
        operation will be done, depending on whether the original query parameters
        already contain the respective key/value pair or not.
    :param replace: (optional)  A dictionary mapping parameter keys to either single
        values or lists. For each key that already exists in the original query
        parameters, the respective value(s) will be replaced with the given one(s).
    :return: A copy of the modified query parameters.
    """
    new_params = {}
    for param, value in query_params.items():
        new_params[param] = _copy_param_value(value)

    if include is not None:
        new_params = _include_query_params(new_params, **include)
    if exclude is not None:
        new_params = _exclude_query_params(new_params, **exclude)
    if toggle is not None:
        new_params = _toggle_query_params(new_params, **toggle)
    if replace is not None:
        new_params = _replace_query_params(new_params, **replace)

    return new_params


def download_string(data, filename, mimetype="text/plain"):
    """Send string data as UTF-8 encoded file to a client.

    :param data: The string data.
    :param filename: The name of the file.
    :param mimetype: (optional) The MIME type of the file.
    :return: The response object.
    """

    # uwsgi does not support file-like objects, so Flask's "send_file" function cannot
    # be used here as it tries to delegate to the file wrapper of the wsgi server. We
    # can bypass that by building the response manually.
    #
    # See also:
    # https://github.com/unbit/uwsgi/issues/1126
    # https://www.pythonanywhere.com/forums/topic/13570/

    file_wrapper = FileWrapper(BytesIO(data.encode()))
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    response = current_app.response_class(
        file_wrapper, mimetype=mimetype, headers=headers, direct_passthrough=True
    )

    return response


def get_locale():
    """Get the current locale.

    The ``locale`` query parameter of the current request will take precedence, followed
    by the ``locale`` cookie and finally the default locale. The chosen locale has to be
    valid, i.e. it has to be configured in the application's configuration in
    ``LOCALES``.

    :return: The current locale. If no valid locale could be found, ``LOCALE_DEFAULT``
        will be returned as configured in the application's configuration.
    """
    default_locale = current_app.config["LOCALE_DEFAULT"]

    if not has_request_context():
        return default_locale

    locales = list(current_app.config["LOCALES"].keys())

    if "locale" in request.args:
        locale = request.args.get("locale")
    elif "locale" in request.cookies:
        locale = request.cookies.get("locale")
    else:
        locale = default_locale

    if locale in locales:
        return locale

    return default_locale


def make_next_url(next_url):
    """Create a target URL to redirect a user to after login.

    :param next_url: An internal URL to redirect to.
    """
    next_param = make_next_param(url_for("accounts.login"), next_url)
    return url_for("accounts.login", next=next_param)


def get_next_url(fallback=None):
    """Get the validated target URL to redirect a user to after login.

    The target URL has to be specified as a ``next`` query parameter in the current
    request.

    :param fallback: (optional) The fallback URL to use in case the target URL was
        invalid or could not be found. Defaults to the index page.
    """
    if has_request_context() and "next" in request.args:
        next_url = request.args.get("next")

        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, next_url))

        if test_url.scheme in ["http", "https"] and ref_url.netloc == test_url.netloc:
            return next_url

    return fallback if fallback is not None else url_for("main.index")


def get_error_message(status_code):
    """Get an error message corresponding to an HTTP status code.

    :param status_code: The HTTP status code.
    :return: The error message.
    """
    return HTTP_STATUS_CODES.get(status_code, "Unknown error")


def get_error_description(status_code):
    """Get an error description corresponding to an HTTP status code.

    :param status_code: The HTTP status code.
    :return: The error description.
    """
    exc = default_exceptions.get(status_code, None)
    if exc is not None:
        return exc.description

    return "An unknown error occured."
