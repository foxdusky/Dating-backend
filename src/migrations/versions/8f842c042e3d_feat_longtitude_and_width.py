"""feat longtitude and width

Revision ID: 8f842c042e3d
Revises: dbffe7531210
Create Date: 2024-11-04 00:15:21.365537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f842c042e3d'
down_revision: Union[str, None] = 'dbffe7531210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('user', sa.Column('width', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'width')
    op.drop_column('user', 'longitude')
    # ### end Alembic commands ###