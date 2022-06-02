"""Initial migration.

Revision ID: 3e9e6f7687c8
Revises: 
Create Date: 2022-05-31 11:54:28.012083

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3e9e6f7687c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('keyword',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('email', sa.String(length=256), nullable=True),
                    sa.Column('password', sa.String(length=256), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('product',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=256), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('product_image',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('path', sa.String(length=256), nullable=True),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('product_keywords',
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('keyword_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
                    sa.UniqueConstraint('product_id', 'keyword_id', name='product_keyword_unique')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_keywords')
    op.drop_table('product_image')
    op.drop_table('product')
    op.drop_table('user')
    op.drop_table('keyword')
    # ### end Alembic commands ###