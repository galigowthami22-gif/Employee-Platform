"""attendance module (DEPRECATED - Use 0005_phase13_attendance.py instead)

Revision ID: d61e7952a4e6
Revises: bd0a877916ad
Create Date: 2026-06-22 22:04:04.485369

This migration is deprecated and empty. The proper Phase 13 Attendance migration
is located at 0005_phase13_attendance.py.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd61e7952a4e6'
down_revision: Union[str, Sequence[str], None] = 'bd0a877916ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - No changes (deprecated migration)."""
    pass


def downgrade() -> None:
    """Downgrade schema - No changes (deprecated migration)."""
    pass
