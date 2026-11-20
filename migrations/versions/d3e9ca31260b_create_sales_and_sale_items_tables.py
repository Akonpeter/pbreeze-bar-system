
"""create sales and sale items tables

Revision ID: d3e9ca31260b
Revises: d72f70fbdb83
Create Date: 2026-11-17 19:04:22.579873

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers.
revision: str = 'd3e9ca31260b'
down_revision: Union[str, Sequence[str], None] = 'd72f70fbdb83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create sales and sale items tables."""

    op.create_table(
        'sales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('total_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_sales_id'),
        'sales',
        ['id'],
        unique=False
    )

    op.create_table(
        'sale_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sale_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('subtotal', sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.ForeignKeyConstraint(['sale_id'], ['sales.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_sale_items_id'),
        'sale_items',
        ['id'],
        unique=False
    )


def downgrade() -> None:
    """Drop sales and sale items tables."""

    op.drop_index(
        op.f('ix_sale_items_id'),
        table_name='sale_items'
    )
    op.drop_table('sale_items')

    op.drop_index(
        op.f('ix_sales_id'),
        table_name='sales'
    )
    op.drop_table('sales')
