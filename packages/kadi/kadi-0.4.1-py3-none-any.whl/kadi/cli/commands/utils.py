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
import os
import sys

import click
from flask import current_app
from jinja2 import Template

from kadi.cli.main import kadi
from kadi.cli.utils import danger
from kadi.cli.utils import echo
from kadi.cli.utils import run_command
from kadi.cli.utils import success
from kadi.ext.db import db
from kadi.lib.licenses.models import License
from kadi.lib.licenses.utils import update_licenses as _update_licenses


DEFAULT_USER = "kadi"
DEFAULT_GROUP = "www-data"
DEFAULT_CONFIG_FILE = "/opt/kadi/config/kadi.py"
DEFAULT_CERT_FILE = "/etc/ssl/certs/kadi.crt"
DEFAULT_KEY_FILE = "/etc/ssl/private/kadi.key"


@kadi.group()
def utils():
    """Miscellaneous utility commands."""


@utils.command()
def secret_key():
    """Generate a random secret key."""
    echo(os.urandom(24).hex())


@utils.command()
def config():
    """Print the current app configuration."""
    config = [f"{k}: {v}" for k, v in current_app.config.items()]
    for item in sorted(config):
        echo(item)


@utils.command()
def update_licenses():
    """Update the licenses stored in the database.

    The licenses will be updated using the configured LICENSE_URL.
    """
    prev_license_count = License.query.count()

    try:
        _update_licenses()
        db.session.commit()
    except Exception as e:
        danger(f"Error updating licenses: {e}")
        sys.exit(1)

    new_license_count = License.query.count()

    echo(f"Added {new_license_count - prev_license_count} license(s).")
    success("Licenses updated successfully.")


def _generate_config(template_name, outfile=None, **kwargs):
    template_path = os.path.join(
        current_app.root_path, "cli", "templates", template_name
    )

    with open(template_path) as file:
        template = Template(file.read())

    rendered_template = template.render(**kwargs)

    if outfile is not None:
        if os.path.exists(outfile.name):
            danger(f"'{outfile.name}' already exists.")
            sys.exit(1)

        outfile.write(rendered_template)
        outfile.write("\n")

        success(f"File '{outfile.name}' generated successfully.")
    else:
        echo("\n" + rendered_template, bold=True)


@utils.command()
@click.option("--default", is_flag=True, help="Use the default values for all prompts.")
@click.option("--out", type=click.File(mode="w"), help="Output file (e.g. kadi.conf).")
def apache(default, out):
    """Generate a basic Apache web server configuration."""
    DEFAULT_CHAIN_FILE = ""

    if default:
        cert_file = DEFAULT_CERT_FILE
        key_file = DEFAULT_KEY_FILE
        chain_file = DEFAULT_CHAIN_FILE
    else:
        cert_file = click.prompt("SSL/TLS certificate file", default=DEFAULT_CERT_FILE)
        key_file = click.prompt("SSL/TLS key file", default=DEFAULT_KEY_FILE)
        chain_file = click.prompt(
            "SSL/TLS intermediate certificates chain file (optional)",
            default=DEFAULT_CHAIN_FILE,
        )

    anonip_bin = None
    if click.confirm(
        "Anonymize IP addresses in access logs? Note that this will install the"
        " 'anonip' package in the current virtual environment if it is not installed"
        " already."
    ):
        run_command(["pip", "install", "anonip"])
        anonip_bin = os.path.join(sys.base_prefix, "bin", "anonip")

    _generate_config(
        "kadi.conf",
        outfile=out,
        server_name=current_app.config["SERVER_NAME"],
        storage_path=current_app.config["STORAGE_PATH"],
        misc_uploads_path=current_app.config["MISC_UPLOADS_PATH"],
        kadi_root=current_app.root_path,
        cert_file=cert_file,
        key_file=key_file,
        chain_file=chain_file,
        anonip_bin=anonip_bin,
    )


@utils.command()
@click.option("--default", is_flag=True, help="Use the default values for all prompts.")
@click.option("--out", type=click.File(mode="w"), help="Output file (e.g. kadi.ini).")
def uwsgi(default, out):
    """Generate a basic uWSGI application server configuration."""
    if default:
        uid = DEFAULT_USER
        gid = DEFAULT_GROUP
        kadi_config = DEFAULT_CONFIG_FILE
    else:
        uid = click.prompt("User the server will run under", default=DEFAULT_USER)
        gid = click.prompt("Group the server will run under", default=DEFAULT_GROUP)
        kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi.ini",
        outfile=out,
        kadi_root=current_app.root_path,
        venv_path=sys.base_prefix,
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )


@utils.command()
@click.option("--default", is_flag=True, help="Use the default values for all prompts.")
@click.option(
    "--out", type=click.File(mode="w"), help="Output file (e.g. kadi-celery.service)."
)
def celery(default, out):
    """Generate a basic systemd unit file for Celery."""
    if default:
        uid = DEFAULT_USER
        gid = DEFAULT_GROUP
        kadi_config = DEFAULT_CONFIG_FILE
    else:
        uid = click.prompt("User the service will run under", default=DEFAULT_USER)
        gid = click.prompt("Group the service will run under", default=DEFAULT_GROUP)
        kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi-celery.service",
        outfile=out,
        kadi_bin=os.path.join(sys.base_prefix, "bin", "kadi"),
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )


@utils.command()
@click.option("--default", is_flag=True, help="Use the default values for all prompts.")
@click.option(
    "--out",
    type=click.File(mode="w"),
    help="Output file (e.g. kadi-celerybeat.service).",
)
def celerybeat(default, out):
    """Generate a basic systemd unit file for Celery beat."""
    if default:
        uid = DEFAULT_USER
        gid = DEFAULT_GROUP
        kadi_config = DEFAULT_CONFIG_FILE
    else:
        uid = click.prompt("User the service will run under", default=DEFAULT_USER)
        gid = click.prompt("Group the service will run under", default=DEFAULT_GROUP)
        kadi_config = click.prompt("Kadi config file", default=DEFAULT_CONFIG_FILE)

    _generate_config(
        "kadi-celerybeat.service",
        outfile=out,
        kadi_bin=os.path.join(sys.base_prefix, "bin", "kadi"),
        uid=uid,
        gid=gid,
        kadi_config=kadi_config,
    )
