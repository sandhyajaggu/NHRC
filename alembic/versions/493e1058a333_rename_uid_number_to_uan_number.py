"""rename uid_number to uan_number

Revision ID: 493e1058a333
Revises: 34ec925364a4
Create Date: 2026-06-09 11:33:53.407123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '493e1058a333'
down_revision: Union[str, Sequence[str], None] = '34ec925364a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column(
        "black_profiles",
        "uid_number",
        new_column_name="uan_number",
        existing_type=sa.String(length=100)
    )

def downgrade() -> None:

    op.alter_column(
        "black_profiles",
        "uan_number",
        new_column_name="uid_number",
        existing_type=sa.String(length=100)
    )