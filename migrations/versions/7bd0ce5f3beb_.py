"""empty message

Revision ID: 7bd0ce5f3beb
Revises: 
Create Date: 2020-02-24 01:52:18.942007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bd0ce5f3beb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vendors', 'close_hours', new_column_name='closing_hours',
                    existing_type=sa.DateTime, type_=sa.Time)
    op.alter_column('vendors', 'open_hours', new_column_name='opening_hours',
                    existing_type=sa.DateTime, type_=sa.Time)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('customers')
    op.drop_table('vendors')
    # ### end Alembic commands ###