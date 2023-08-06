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
import sys

import click
from flask import current_app

from kadi.cli.main import kadi
from kadi.cli.utils import check_env
from kadi.cli.utils import danger
from kadi.cli.utils import echo
from kadi.cli.utils import success
from kadi.cli.utils import warning
from kadi.ext.db import db
from kadi.lib.db import get_class_by_tablename
from kadi.lib.search.core import add_to_index
from kadi.lib.search.core import create_index
from kadi.lib.search.core import SearchableMixin
from kadi.lib.search.elasticsearch import es


@kadi.group()
def search():
    """Utility commands for managing the search index."""


@search.command()
def init():
    """Create all search indices."""
    for tablename in db.metadata.tables.keys():
        model = get_class_by_tablename(tablename)

        if model is not None and issubclass(model, SearchableMixin):
            if not create_index(model):
                danger(f"Error creating index for '{model.__tablename__}'.")
                sys.exit(1)

    success("Search indices created successfully.")


@search.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def clean(i_am_sure):
    """Remove all search indices."""
    if not i_am_sure:
        warning(
            "This will remove all search indices of instance(s)"
            f" '{current_app.config['ELASTICSEARCH_HOSTS']}'. If you are sure you want"
            " to do this, use the flag --i-am-sure."
        )
        return

    es.indices.delete("*")

    success("Search indices removed successfully.")


@search.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def reindex(i_am_sure):
    """Rebuild the search index.

    This will create a new index (possibly with an updated mapping), populate it and
    switch it with the current one afterwards.
    """
    if not i_am_sure:
        warning(
            "This will rebuild all search indices of instance(s)"
            f" '{current_app.config['ELASTICSEARCH_HOSTS']}'. If you are sure you want"
            " to do this, use the flag --i-am-sure."
        )
        return

    for tablename in db.metadata.tables.keys():
        model = get_class_by_tablename(tablename)

        if model is None or not issubclass(model, SearchableMixin):
            continue

        # Make sure the initial index exists, even if it might be empty first.
        create_index(model)

        alias = tablename

        # As there should only be one index we can ignore the potentially
        # nondeterministic insertion order.
        old_index = list(es.indices.get_alias(alias).keys())[0]
        new_index = create_index(model, force=True)

        echo(f"Populating new index '{new_index}'...")

        for obj in model.query:
            if not add_to_index(obj, index=new_index):
                danger(f"Error indexing {obj!r}.")
                es.indices.delete(new_index)
                sys.exit(1)

        # Switch the alias to only point to the new index.
        es.indices.update_aliases(
            {
                "actions": [
                    {"remove": {"index": old_index, "alias": alias}},
                    {"add": {"index": new_index, "alias": alias}},
                ]
            }
        )

        # Now the old index can be safely deleted.
        es.indices.delete(old_index)

        success(
            f"Moved alias '{alias}' from old index '{old_index}' to new index"
            f" '{new_index}'."
        )
