"""add status to job fair registrations

Revision ID: 3f868395bcec
Revises: 8db7ef76fa6d
Create Date: 2026-06-11 14:56:41.922615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3f868395bcec'
down_revision: Union[str, Sequence[str], None] = '8db7ef76fa6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "student_job_fair_registrations",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="PENDING"
        )
    )

    op.add_column(
        "hr_job_fair_registrations",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="PENDING"
        )
    )
def downgrade():

    op.drop_column(
        "student_job_fair_registrations",
        "status"
    )

    op.drop_column(
        "hr_job_fair_registrations",
        "status"
    )