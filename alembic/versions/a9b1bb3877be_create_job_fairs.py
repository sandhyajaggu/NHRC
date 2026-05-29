"""create job fairs

Revision ID: a9b1bb3877be
Revises: 06e3c3c15639
Create Date: 2026-05-29 11:37:23.155536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9b1bb3877be'
down_revision: Union[str, Sequence[str], None] = '06e3c3c15639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():

    op.create_table(
        "job_fairs",

        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service_id", sa.Integer(), nullable=False),

        sa.Column("title", sa.String()),
        sa.Column("description", sa.String()),

        sa.Column("organizer_name", sa.String()),
        sa.Column("event_mode", sa.String()),

        sa.Column("start_date", sa.Date()),
        sa.Column("end_date", sa.Date()),

        sa.Column("location", sa.String())
    )

    op.create_table(
        "event_job_roles",

        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column(
            "event_id",
            sa.Integer(),
            sa.ForeignKey(
                "service_events.id",
                ondelete="CASCADE"
            )
        ),

        sa.Column("hiring_type", sa.String()),
        sa.Column("job_role", sa.String()),
        sa.Column("experience", sa.String()),
        sa.Column("openings", sa.Integer()),
        sa.Column("job_location", sa.String()),
        sa.Column("salary_min", sa.String()),
        sa.Column("salary_max", sa.String()),
        sa.Column("education_required", sa.String())
    )


def downgrade():

    op.drop_table("event_job_roles")
    op.drop_table("job_fairs")

