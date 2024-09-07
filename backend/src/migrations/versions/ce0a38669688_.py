"""empty message

Revision ID: ce0a38669688
Revises: 3ed50ce6d74f
Create Date: 2024-08-24 17:42:26.912105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ce0a38669688'
down_revision: Union[str, None] = '3ed50ce6d74f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('title', sa.String(length=100), nullable=True))
    op.add_column('questions', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('questions', sa.Column('writer', sa.String(length=100), nullable=True))
    op.drop_column('questions', 'question')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('question', mysql.TEXT(), nullable=True))
    op.drop_column('questions', 'writer')
    op.drop_column('questions', 'content')
    op.drop_column('questions', 'title')
    # ### end Alembic commands ###