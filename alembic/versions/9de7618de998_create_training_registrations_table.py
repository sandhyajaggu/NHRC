from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9de7618de998"
down_revision: Union[str, Sequence[str], None] = "a13e374fb048"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "training_registrations",

        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.Column("training_id", sa.Integer(), nullable=False),

        sa.Column("member_type", sa.String(), nullable=False),

        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),

        sa.Column("location", sa.String(), nullable=False),
        sa.Column("iam_a", sa.String(), nullable=False),
        sa.Column("nhrc_id", sa.String(), nullable=False),

        sa.Column("receive_updates", sa.Boolean(), default=False),

        sa.Column("college_name", sa.String(), nullable=True),
        sa.Column("year_of_passout", sa.String(), nullable=True),

        sa.Column("company_name", sa.String(), nullable=True),
        sa.Column("company_location", sa.String(), nullable=True),

        sa.Column("status", sa.String(), server_default="REGISTERED"),

        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table("training_registrations")