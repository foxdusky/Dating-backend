"""gender_id fix

Revision ID: c4b5d249cd78
Revises: 2d8fd3913be1
Create Date: 2024-11-03 21:11:50.131802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c4b5d249cd78'
down_revision: Union[str, None] = '2d8fd3913be1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gender_id', sa.Integer(), nullable=False))
    op.alter_column('user', 'reg_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.create_foreign_key(None, 'user', 'gender', ['gender_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'reg_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('user', 'gender_id')
    # ### end Alembic commands ###