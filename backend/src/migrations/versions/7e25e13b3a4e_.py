"""empty message

Revision ID: 7e25e13b3a4e
Revises: ce0a38669688
Create Date: 2024-09-02 23:34:06.854406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7e25e13b3a4e'
down_revision: Union[str, None] = 'ce0a38669688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('question_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'answers', 'questions', ['question_id'], ['id'])
    op.add_column('questions', sa.Column('title', sa.String(length=100), nullable=True))
    op.drop_column('questions', 'subject')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('subject', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('questions', 'title')
    op.drop_constraint(None, 'answers', type_='foreignkey')
    op.drop_column('answers', 'question_id')
    # ### end Alembic commands ###