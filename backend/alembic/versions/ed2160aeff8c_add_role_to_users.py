"""add role to users

Revision ID: ed2160aeff8c
Revises:
Create Date: 2026-09-02 16:09:21.175078

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision: str = 'ed2160aeff8c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add the role column with a database-level default.
    #
    # Existing users already stored in the database need a value
    # for this new NOT NULL column. "user" safely assigns the
    # least-privileged role to those existing accounts.
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=20),
            nullable=False,
            server_default='user'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Remove the role column if this migration is rolled back.
    op.drop_column('users', 'role')