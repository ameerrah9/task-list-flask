"""Update text to title in goal model

Revision ID: 86a754f565a2
Revises: a3ba9777412a
Create Date: 2022-11-09 13:07:04.244767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86a754f565a2'
down_revision = 'a3ba9777412a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('title', sa.String(), nullable=True))
    op.drop_column('goal', 'text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('goal', 'title')
    # ### end Alembic commands ###
