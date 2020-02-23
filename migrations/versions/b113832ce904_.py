"""empty message

Revision ID: 28caae1b112c
Revises: 
Create Date: 2020-02-23 07:07:01.541769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28caae1b112c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vendors', sa.Column('open_hours', sa.DateTime()))
    op.add_column('vendors', sa.Column('close_hours', sa.DateTime()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vendors', 'close_hours')
    op.drop_column('vendors', 'open_hours')
    # ### end Alembic commands ###
