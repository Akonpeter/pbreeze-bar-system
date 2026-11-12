"""add quantity to stock movements

Revision ID: d72f70fbdb83
Revises: 
Create Date: 2026-11-12 21:17:38.314010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd72f70fbdb83'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'stock_movements',
        sa.Column(
            'quantity',
            sa.Numeric(precision=12, scale=2),
            nullable=False
        )
    )

def downgrade() -> None:
    op.drop_column('stock_movements', 'quantity')