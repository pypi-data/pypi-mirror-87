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
import click
from flask.cli import FlaskGroup
from flask.cli import routes_command
from flask.cli import shell_command

from kadi.app import create_app


class KadiGroup(FlaskGroup):
    """Click group for use in custom commands.

    Automatically makes commands run inside an application context. Wraps Flask's own
    custom Click group.
    """

    def __init__(self, **kwargs):
        super().__init__(
            add_default_commands=False,
            add_version_option=False,
            create_app=create_app,
            **kwargs,
        )

    def _load_plugin_commands(self):
        pass


@click.group(cls=KadiGroup)
def kadi():
    """The Kadi command line interface."""


kadi.add_command(routes_command)
kadi.add_command(shell_command)


# pylint: disable=unused-import


from .commands.assets import assets
from .commands.celery import celery
from .commands.db import db
from .commands.files import files
from .commands.i18n import i18n
from .commands.search import search
from .commands.users import users
from .commands.utils import utils
