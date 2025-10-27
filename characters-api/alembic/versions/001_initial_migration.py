"""Initial migration

Revision ID: 001_initial
Revises:
Create Date: 2024-12-05 14:59:58.430262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tables are created automatically via Base.metadata.create_all()
    pass


def downgrade() -> None:
    # Tables are managed via Base.metadata
    pass
