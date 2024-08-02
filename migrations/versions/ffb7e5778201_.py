"""empty message

Revision ID: ffb7e5778201
Revises: 6cf6d886f14e
Create Date: 2024-08-01 10:52:48.728400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffb7e5778201'
down_revision = '6cf6d886f14e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('published_date', sa.Date(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('borrow_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('borrow_date', sa.DateTime(), nullable=False),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.Column('fee', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrow_record')
    op.drop_table('book')
    # ### end Alembic commands ###
