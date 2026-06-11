"""fix talent publication

Revision ID: 8db7ef76fa6d
Revises: 3ba342120ab5
Create Date: 2026-06-11 12:48:19.734851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8db7ef76fa6d'
down_revision: Union[str, Sequence[str], None] = '3ba342120ab5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "talent_publications",
        sa.Column("banner_image_1", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("banner_image_2", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("banner_image_3", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("banner_image_4", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("document_1", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("document_2", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("document_3", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("document_4", sa.String(500), nullable=True)
    )

    op.add_column(
        "talent_publications",
        sa.Column("youtube_url", sa.String(500), nullable=True)
    )

    op.drop_column(
        "talent_publications",
        "cover_image"
    )

    op.drop_column(
        "talent_publications",
        "pdf_file"
    )

def downgrade():

    op.add_column(
        "talent_publications",
        sa.Column("cover_image", sa.String(500))
    )

    op.add_column(
        "talent_publications",
        sa.Column("pdf_file", sa.String(500))
    )

    op.drop_column("talent_publications", "youtube_url")

    op.drop_column("talent_publications", "document_4")
    op.drop_column("talent_publications", "document_3")
    op.drop_column("talent_publications", "document_2")
    op.drop_column("talent_publications", "document_1")

    op.drop_column("talent_publications", "banner_image_4")
    op.drop_column("talent_publications", "banner_image_3")
    op.drop_column("talent_publications", "banner_image_2")
    op.drop_column("talent_publications", "banner_image_1")