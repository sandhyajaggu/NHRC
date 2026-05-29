"""update employee password hash

Revision ID: 1c19132440d6
Revises: ed36fd43ec5d
Create Date: 2026-05-26 11:18:11.052486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c19132440d6'
down_revision: Union[str, Sequence[str], None] = 'ed36fd43ec5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



"""update employee password hash

Revision ID: 1c19132440d6
Revises: ed36fd43ec5d
Create Date: 2026-05-26 11:18:11.052486
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '1c19132440d6'
down_revision: Union[str, Sequence[str], None] = 'ed36fd43ec5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        'employees',
        sa.Column('password_hash', sa.String(), nullable=True)
    )

    op.drop_column(
        'employees',
        'password'
    )

    op.alter_column(
        'student_autonomous_details',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        'student_university_details',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )


def downgrade() -> None:

    op.alter_column(
        'student_university_details',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        'student_autonomous_details',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.add_column(
        'employees',
        sa.Column(
            'password',
            sa.VARCHAR(),
            nullable=True
        )
    )

    op.drop_column(
        'employees',
        'password_hash'
    )

