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
from pluggy import HookspecMarker


hookspec = HookspecMarker("kadi")


@hookspec
def kadi_register_blueprints(app):
    """Hook for registering blueprints.

    :param app: The application object.
    """


@hookspec(firstresult=True)
def kadi_template_home_before():
    """Template hook for prepending an HTML snippet to the home page.

    Note that the hook chain will stop after the first returned result that is not
    ``None``.

    Used in :file:`modules/main/templates/main/home.html`.
    """


@hookspec
def kadi_get_translations_paths():
    """Hook for collecting translation paths.

    The translations path returned by a plugin must be absolute. Note that currently
    translations of the main application and plugins are simply merged together, where
    translations of the main application will always take precedence.
    """


@hookspec
def kadi_register_oauth2_providers(registry):
    """Hook for registering OAuth2 providers.

    Currently, only the authorization code grant is supported. Each provider needs to
    register itself to the given registry provided by the Authlib library using a unique
    name.

    Needs to be used together with :func:`kadi_get_oauth2_providers`.

    :param registry: The OAuth2 provider registry.
    """


@hookspec
def kadi_get_oauth2_providers():
    """Hook for collecting OAuth2 providers.

    Each OAuth2 provider has to be returned as a dictionary containing all necessary
    information about the provider. A provider must at least provide the unique name
    that was also used to register it.

    For example:

    .. code-block:: python3

        {
            "name": "my_provider",
            "title": "My provider",
            "website": "https://example.com",
            "description": "The (HTML) description of the OAuth2 provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers`.
    """


@hookspec
def kadi_get_publication_providers():
    """Hook for collecting publication providers.

    Each publication provider has to be returned as a dictionary containing all
    necessary information about the provider. A provider must at least provide the
    unique name that was also used to register the OAuth2 provider that this provider
    should use.

    For example:

    .. code-block:: python3

        {
            "name": "my_provider",
            "description": "The (HTML) description of the publication provider.",
        }

    Needs to be used together with :func:`kadi_register_oauth2_providers` and
    :func:`kadi_get_oauth2_providers`.
    """


@hookspec(firstresult=True)
def kadi_publish_record(record, provider, client, token, task):
    """Hook for publishing a record using a given provider.

    Each plugin has to check the given provider and decide if it should start the
    publishing process or not, otherwise it has to return ``None``.

    Needs to be used together with :func:`kadi_get_publication_providers`. Note that the
    hook chain will stop after the first returned result that is not ``None``.

    :param record: The record to publish.
    :param provider: The provider to use for publishing.
    :param client: The OAuth2 client to use for publishing.
    :param token: The OAuth2 token to use for publishing.
    :param task: A :class:`.Task` object that may be provided if this hook is executed
        in a task.
    """
