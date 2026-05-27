"""add scraper logs and tender source uniqueness

Revision ID: 0002_add_scraper_logs
Revises: 0001_create_full_schema
Create Date: 2026-05-27 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_scraper_logs"
down_revision = "0001_create_full_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scraper_logs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("source_url", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="running"),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("records_scraped", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("records_created", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index(
        "ix_tenders_source_source_tender_id",
        "tenders",
        ["source", "source_tender_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_tenders_source_source_tender_id", table_name="tenders")
    op.drop_table("scraper_logs")
