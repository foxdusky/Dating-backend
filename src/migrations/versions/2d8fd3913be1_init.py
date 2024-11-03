"""init

Revision ID: 2d8fd3913be1
Revises: 
Create Date: 2024-11-03 18:51:39.203193

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2d8fd3913be1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('filename', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('front_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('gender',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('e_mail', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('surname', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('profile_photo', sa.Integer(), nullable=True),
                    sa.Column('reg_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['profile_photo'], ['file.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('e_mail')
                    )
    # ### end Alembic commands ###
    # Default values initialize ##
    op.execute("""
        INSERT INTO "gender" ("name")
        VALUES (
            'male'
        )
    """)
    op.execute("""
        INSERT INTO "gender" ("name")
        VALUES (
            'female'
        )
    """)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('gender')
    op.drop_table('file')
    # ### end Alembic commands ###

    ## Default values deletion  ##

    op.execute("""
        DELETE FROM "gender" 
        WHERE "name" = 'male'
    """)
    op.execute("""
        DELETE FROM "gender" 
        WHERE "name" = 'female'
    """)