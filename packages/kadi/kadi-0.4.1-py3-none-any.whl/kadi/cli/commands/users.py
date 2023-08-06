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
import string
import sys
from random import SystemRandom

import click
from flask import current_app

from kadi.cli.main import kadi
from kadi.cli.utils import danger
from kadi.cli.utils import echo
from kadi.cli.utils import success
from kadi.ext.db import db
from kadi.modules.accounts.forms import RegistrationForm
from kadi.modules.accounts.models import User
from kadi.modules.accounts.providers import LocalProvider


@kadi.group()
def users():
    """Utility commands for managing users."""


@users.command()
def create():
    """Create a new local user."""
    if not LocalProvider.is_registered():
        danger("Local provider not registered in the application.")
        sys.exit(1)

    username = click.prompt("Username")
    email = click.prompt("Email")
    displayname = click.prompt("Display name", default=username)

    system_roles = sorted(list(current_app.config["SYSTEM_ROLES"].keys()))
    system_role = click.prompt(
        "System role",
        type=click.Choice(system_roles, case_sensitive=False),
        default=LocalProvider.Meta.defaults["default_system_role"],
    )

    form = RegistrationForm(
        meta={"csrf": False},
        data={"username": username, "email": email, "displayname": displayname},
    )

    del form.password
    del form.password2

    if not form.validate():
        for error in form.errors.get("username", []):
            danger("[Username] " + error)

        for error in form.errors.get("email", []):
            danger("[Email] " + error)

        sys.exit(1)

    alphanum = string.ascii_letters + string.digits
    password = "".join(SystemRandom().choice(alphanum) for _ in range(16))

    identity = LocalProvider.register(
        username=form.username.data,
        email=form.email.data,
        displayname=form.displayname.data,
        password=password,
        system_role=system_role,
    )

    if identity:
        echo(f"\n{'Displayname':12s}{displayname}")
        echo(f"{'Username':12s}{username}")
        echo(f"{'Email':12s}{email}")
        echo(f"{'System role':12s}{system_role}")

        if click.confirm("Do you want to create this user?"):
            db.session.commit()

            success("User created successfully.\n")
            echo("Initial password: " + password)
    else:
        danger("Error creating user.")


@users.command()
@click.argument("user_id", type=click.INT)
def activate(user_id):
    """Activate an inactive user."""
    user = User.query.get(user_id)

    if user is None:
        danger(f"No valid user found with ID {user_id}.")
        sys.exit(1)

    if user.state == "active":
        echo("User is already active.")
        sys.exit(0)

    echo(f"Found user with ID {user_id} with the following identities:")
    for identity in user.identities:
        echo(f"  * {identity!r}")

    if click.confirm("\nDo you want to activate this user?"):
        user.state = "active"
        db.session.commit()

        success("User activated successfully.")


@users.command()
@click.argument("user_id", type=click.INT)
def deactivate(user_id):
    """Deactivate an active user."""
    user = User.query.get(user_id)

    if user is None:
        danger(f"No valid user found with ID {user_id}.")
        sys.exit(1)

    if user.state == "inactive":
        echo("User is already inactive.")
        sys.exit(0)

    echo(f"Found user with ID {user_id} with the following identities:")
    for identity in user.identities:
        echo(f"  * {identity!r}")

    if click.confirm("\nDo you want to deactivate this user?"):
        user.state = "inactive"
        db.session.commit()

        success("User deactivated successfully.")
