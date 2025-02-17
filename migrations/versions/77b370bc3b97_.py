"""empty message

Revision ID: 77b370bc3b97
Revises: 0ecab60bd1eb
Create Date: 2024-09-13 10:03:27.846506

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '77b370bc3b97'
down_revision = '0ecab60bd1eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('new_price', sa.Float(), nullable=False))
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', mysql.FLOAT(), nullable=False))
        batch_op.drop_column('new_price')

    # ### end Alembic commands ###
