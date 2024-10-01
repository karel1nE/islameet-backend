"""a

Revision ID: 0da4fb543421
Revises: 
Create Date: 2024-10-02 02:51:26.060857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0da4fb543421'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=256), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=True),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('birthday', sa.Date(), nullable=True),
        sa.Column('city', sa.String(length=256), nullable=True)
    )

    # Create complaints table
    op.create_table(
        'complaints',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('from_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('to_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=False),
        sa.Column('status', sa.String(length=64), nullable=False),
        sa.Column('time_send', sa.DateTime(), default=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    # Drop complaints table
    op.drop_table('complaints')

    # Drop users table
    op.drop_table('users')