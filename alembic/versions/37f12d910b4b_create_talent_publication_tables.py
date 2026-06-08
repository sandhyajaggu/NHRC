"""create talent publication tables

Revision ID: 37f12d910b4b
Revises: 1135815d24bc
Create Date: 2026-06-08 13:19:42.833595
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '37f12d910b4b'
down_revision: Union[str, Sequence[str], None] = '1135815d24bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Talent Publication main table
    op.create_table(
        'talent_publications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('cover_image', sa.String(length=500), nullable=False),
        sa.Column('pdf_file', sa.String(length=500), nullable=False),
        sa.Column('display_order', sa.Integer(), server_default='1'),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Config table (YouTube only)
    op.create_table(
        'talent_publication_config',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('youtube_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('talent_publication_config')
    op.drop_table('talent_publications')