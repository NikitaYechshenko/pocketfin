"""refactor_asset_model: add price, remove user_id, add constraints and indexes

Revision ID: a1b2c3d4e5f6
Revises: 99418b5a4952
Create Date: 2026-03-22 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import CheckConstraint


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '99418b5a4952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: refactor Asset model."""

    # 1. Add price column (required field, so we set a default temporarily)
    op.add_column('assets', sa.Column('price', sa.Numeric(precision=18, scale=8), nullable=True))

    # For existing data, set price = 0 temporarily (you should update this manually in production)
    op.execute("UPDATE assets SET price = 0 WHERE price IS NULL")

    # Make price NOT NULL
    op.alter_column('assets', 'price', nullable=False)

    # 2. Change amount precision from (18, 15) to (18, 8)
    op.alter_column('assets', 'amount',
        type_=sa.Numeric(precision=18, scale=8),
        existing_type=sa.Numeric(precision=18, scale=15),
        existing_nullable=False
    )

    # 3. Add index to portfolio_id (foreign key index for better performance)
    op.create_index('ix_assets_portfolio_id', 'assets', ['portfolio_id'])

    # 4. Add index to portfolios.user_id
    op.create_index('ix_portfolios_user_id', 'portfolios', ['user_id'])

    # 5. Add CHECK constraints
    op.create_check_constraint(
        'check_operation_type',
        'assets',
        "operation_type IN ('buy', 'sell')"
    )
    op.create_check_constraint(
        'check_amount_positive',
        'assets',
        'amount > 0'
    )
    op.create_check_constraint(
        'check_price_positive',
        'assets',
        'price > 0'
    )

    # 6. Drop user_id column from assets (redundant, can get via portfolio.user_id)
    # First drop the foreign key constraint
    op.drop_constraint('assets_user_id_fkey', 'assets', type_='foreignkey')
    op.drop_column('assets', 'user_id')


def downgrade() -> None:
    """Downgrade schema: revert Asset model changes."""

    # 1. Re-add user_id column
    op.add_column('assets', sa.Column('user_id', sa.Integer(), nullable=True))

    # Populate user_id from portfolio.user_id
    op.execute("""
        UPDATE assets
        SET user_id = portfolios.user_id
        FROM portfolios
        WHERE assets.portfolio_id = portfolios.id
    """)

    # Make user_id NOT NULL and add foreign key
    op.alter_column('assets', 'user_id', nullable=False)
    op.create_foreign_key('assets_user_id_fkey', 'assets', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # 2. Drop CHECK constraints
    op.drop_constraint('check_price_positive', 'assets', type_='check')
    op.drop_constraint('check_amount_positive', 'assets', type_='check')
    op.drop_constraint('check_operation_type', 'assets', type_='check')

    # 3. Drop indexes
    op.drop_index('ix_portfolios_user_id', table_name='portfolios')
    op.drop_index('ix_assets_portfolio_id', table_name='assets')

    # 4. Revert amount precision from (18, 8) to (18, 15)
    op.alter_column('assets', 'amount',
        type_=sa.Numeric(precision=18, scale=15),
        existing_type=sa.Numeric(precision=18, scale=8),
        existing_nullable=False
    )

    # 5. Drop price column
    op.drop_column('assets', 'price')
