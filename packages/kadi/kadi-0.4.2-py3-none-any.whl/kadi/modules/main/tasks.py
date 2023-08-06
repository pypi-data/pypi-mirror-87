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
from datetime import timedelta

from flask import current_app

from kadi.ext.celery import celery
from kadi.ext.db import db
from kadi.lib.utils import utcnow
from kadi.modules.collections.core import purge_collection
from kadi.modules.collections.models import Collection
from kadi.modules.groups.core import purge_group
from kadi.modules.groups.models import Group
from kadi.modules.records.core import purge_record
from kadi.modules.records.models import Record


def clean_resources(inside_task=False):
    """Clean all deleted and expired resources.

    Note that this function may issue one or more database commits.

    A resource's expiration date is defined as ``RESOURCES_MAX_AGE`` in the
    application's configuration. The resources that will be cleaned currently consist of
    soft-deleted instances of :class:`.Record`, :class:`.Collection` and
    :class:`.Group`.

    :param inside_task: (optional) A flag indicating whether the function is executed in
        a task. In that case, additional information will be logged.
    """
    expiration_date = utcnow() - timedelta(
        seconds=current_app.config["RESOURCES_MAX_AGE"]
    )

    # Delete expired records.
    records = Record.query.filter(
        Record.state == "deleted", Record.last_modified < expiration_date
    )

    if inside_task:
        current_app.logger.info(f"Deleting {records.count()} expired record(s).")

    for record in records:
        purge_record(record)

    # Delete expired collections.
    collections = Collection.query.filter(
        Collection.state == "deleted", Collection.last_modified < expiration_date
    )

    if inside_task:
        current_app.logger.info(
            f"Deleting {collections.count()} expired collection(s)."
        )

    for collection in collections:
        purge_collection(collection)

    # Delete expired groups.
    groups = Group.query.filter(
        Group.state == "deleted", Group.last_modified < expiration_date
    )

    if inside_task:
        current_app.logger.info(f"Deleting {groups.count()} expired group(s).")

    for group in groups:
        purge_group(group)

    db.session.commit()


@celery.task(name="kadi.main.clean_resources")
def _clean_resources_task(**kwargs):
    clean_resources(inside_task=True)
