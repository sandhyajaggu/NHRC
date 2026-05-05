"""make membership_id not null

Revision ID: f1de37ff39df
Revises: 12ed411624c7
Create Date: 2026-05-05 12:11:16.953744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1de37ff39df'
down_revision: Union[str, Sequence[str], None] = '12ed411624c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


'''def upgrade() -> None:
    """Upgrade schema."""
    pass'''
def upgrade():
    op.alter_column(
        'contact_messages',
        'membership_id',
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
