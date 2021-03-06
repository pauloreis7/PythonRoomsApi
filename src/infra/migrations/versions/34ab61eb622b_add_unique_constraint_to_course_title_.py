"""add unique constraint to course title field

Revision ID: 34ab61eb622b
Revises: 4934688d3764
Create Date: 2022-07-16 19:12:42.527070

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "34ab61eb622b"
down_revision = "4934688d3764"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_courses_title"), "courses", ["title"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_courses_title"), table_name="courses")
    # ### end Alembic commands ###
