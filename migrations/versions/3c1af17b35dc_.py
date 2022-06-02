"""empty message

Revision ID: 3c1af17b35dc
Revises: 52e9b2209fda
Create Date: 2022-06-02 06:43:07.650647

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3c1af17b35dc'
down_revision = '52e9b2209fda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=256), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###