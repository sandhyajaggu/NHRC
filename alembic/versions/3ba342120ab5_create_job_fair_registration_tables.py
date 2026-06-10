"""create job fair registration tables

Revision ID: 3ba342120ab5
Revises: 493e1058a333
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "3ba342120ab5"
down_revision: Union[str, Sequence[str], None] = "493e1058a333"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "student_job_fair_registrations",

        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column(
            "job_fair_id",
            sa.Integer(),
            sa.ForeignKey("job_fairs.id"),
            nullable=False
        ),

        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(50), nullable=False),

        sa.Column("location", sa.String(255), nullable=False),

        sa.Column("iam_a", sa.String(100), nullable=False),

        sa.Column("nhrc_id", sa.String(100), nullable=False),

        sa.Column("college_name", sa.String(255), nullable=False),

        sa.Column("year_of_passout", sa.String(50), nullable=False),

        sa.Column("department", sa.String(255), nullable=False),

        sa.Column(
            "preferred_job_role",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "technical_skills",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "receive_updates",
            sa.Boolean(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )

    op.create_table(
        "hr_job_fair_registrations",

        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column(
            "job_fair_id",
            sa.Integer(),
            sa.ForeignKey("job_fairs.id"),
            nullable=False
        ),

        sa.Column(
            "company_name",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "company_url",
            sa.String(500),
            nullable=True
        ),

        sa.Column(
            "full_name",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "nhrc_id",
            sa.String(100),
            nullable=False
        ),

        sa.Column(
            "email",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "phone",
            sa.String(50),
            nullable=False
        ),

        sa.Column(
            "receive_updates",
            sa.Boolean(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        )
    )

    op.create_table(
        "hr_job_fair_roles",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "registration_id",
            sa.Integer(),
            sa.ForeignKey(
                "hr_job_fair_registrations.id"
            ),
            nullable=False
        ),

        sa.Column(
            "hiring_type",
            sa.String(100),
            nullable=False
        ),

        sa.Column(
            "job_role",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "experience",
            sa.String(100),
            nullable=False
        ),

        sa.Column(
            "no_of_openings",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "salary_min",
            sa.String(50),
            nullable=False
        ),

        sa.Column(
            "salary_max",
            sa.String(50),
            nullable=False
        ),

        sa.Column(
            "job_location",
            sa.String(255),
            nullable=False
        ),

        sa.Column(
            "education_required",
            sa.String(255),
            nullable=False
        )
    )


def downgrade() -> None:

    op.drop_table("hr_job_fair_roles")

    op.drop_table("hr_job_fair_registrations")

    op.drop_table("student_job_fair_registrations")