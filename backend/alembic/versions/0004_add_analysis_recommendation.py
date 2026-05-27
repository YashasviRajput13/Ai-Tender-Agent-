"""Add recommendation field to tender analysis

Revision ID: 0004_add_analysis_recommendation
Revises: 0003_add_analysis_fields
Create Date: 2026-05-27 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004_add_analysis_recommendation"
down_revision = "0003_add_analysis_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tender_analysis", sa.Column("recommendation", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("tender_analysis", "recommendation")
