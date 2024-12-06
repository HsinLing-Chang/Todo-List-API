"""Rename user column to user_email

Revision ID: 7a11f3fc1a3c
Revises: 538066f96107
Create Date: 2024-11-26 14:54:26.639468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a11f3fc1a3c'
down_revision: Union[str, None] = '538066f96107'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'Task',
        'user',
        new_column_name='user_email'
    )


def downgrade() -> None:
    pass
