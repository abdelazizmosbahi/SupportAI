"""Seed RBAC roles

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-04 18:20

"""
import json

import sqlalchemy as sa

from alembic import op
from app.core.permissions import ROLE_PERMISSIONS_MAP

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for role_name, permissions in ROLE_PERMISSIONS_MAP.items():
        permissions_json = json.dumps(permissions)
        op.execute(
            sa.text(
                "INSERT INTO roles (name, permissions) "
                "VALUES (:name, CAST(:permissions AS json))"
            ).bindparams(
                sa.bindparam("name", role_name),
                sa.bindparam("permissions", permissions_json),
            )
        )


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('OWNER', 'ADMIN', 'AGENT', 'VIEWER')")
