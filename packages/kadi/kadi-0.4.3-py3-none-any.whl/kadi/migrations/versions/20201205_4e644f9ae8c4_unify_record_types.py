"""Unify record types

Revision ID: 4e644f9ae8c4
Revises: dc589906a474
Create Date: 2020-12-05 14:22:34.756036

"""
import json

import sqlalchemy as sa
from alembic import op

import kadi.lib.migration_types


# revision identifiers, used by Alembic.
revision = "4e644f9ae8c4"
down_revision = "dc589906a474"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Lowercase all existing record types, no matter the state of the record.
    op.execute(
        """
        UPDATE record
        SET type = LOWER(type)
        """
    )

    # Lowercase all existing record types in template.
    templates = conn.execute(
        """
        SELECT id, data
        FROM template
        WHERE type='record'
        """
    )

    for template in templates:
        record_type = template.data.get("type")

        if record_type is not None:
            data = template.data
            data["type"] = record_type.lower()

            op.execute(
                """
                UPDATE template
                SET data = '{data}'::jsonb
                WHERE id={id}
                """.format(
                    id=template.id, data=json.dumps(data)
                )
            )


def downgrade():
    pass
