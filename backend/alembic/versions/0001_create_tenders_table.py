"""create full tender intelligence schema

Revision ID: 0001_create_full_schema
Revises: 
Create Date: 2026-05-26 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_full_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False, unique=True),
        sa.Column("website", sa.String(length=256), nullable=True),
        sa.Column("sector", sa.String(length=128), nullable=True),
        sa.Column("location", sa.String(length=128), nullable=True),
        sa.Column("profile", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False, unique=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False, server_default="user"),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "tenders",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False, server_default="cppt"),
        sa.Column("source_tender_id", sa.String(length=128), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("authority", sa.String(length=256), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("estimated_value", sa.Float(), nullable=True),
        sa.Column("category", sa.String(length=128), nullable=True),
        sa.Column("region", sa.String(length=128), nullable=True),
        sa.Column("tender_url", sa.String(length=512), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False, server_default="open"),
        sa.Column("raw_metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_tenders_source_tender_id", "tenders", ["source_tender_id"])
    op.create_index("ix_tenders_status", "tenders", ["status"])
    op.create_index("ix_tenders_deadline", "tenders", ["deadline"])

    op.create_table(
        "tender_documents",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Integer(), sa.ForeignKey("tenders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.String(length=512), nullable=False),
        sa.Column("filename", sa.String(length=256), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("parsed_sections", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "tender_analysis",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Integer(), sa.ForeignKey("tenders.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("eligibility", sa.JSON(), nullable=True),
        sa.Column("required_documents", sa.JSON(), nullable=True),
        sa.Column("risk_level", sa.String(length=32), nullable=True),
        sa.Column("risk_reasons", sa.JSON(), nullable=True),
        sa.Column("category", sa.String(length=128), nullable=True),
        sa.Column("deadline", sa.String(length=64), nullable=True),
        sa.Column("budget", sa.String(length=64), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("match_score", sa.Float(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
        sa.Column("success_probability", sa.Float(), nullable=True),
        sa.Column("raw_response", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "eligibility_requirements",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Integer(), sa.ForeignKey("tenders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("requirement_text", sa.Text(), nullable=False),
        sa.Column("matched", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "risk_assessments",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Integer(), sa.ForeignKey("tenders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("issue", sa.String(length=256), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("tender_id", sa.Integer(), sa.ForeignKey("tenders.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("notification_type", sa.String(length=32), nullable=False, server_default="info"),
        sa.Column("read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "agent_logs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("agent_name", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("entity_type", sa.String(length=128), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("agent_logs")
    op.drop_table("notifications")
    op.drop_table("risk_assessments")
    op.drop_table("eligibility_requirements")
    op.drop_table("tender_analysis")
    op.drop_table("tender_documents")
    op.drop_table("tenders")
    op.drop_table("users")
    op.drop_table("companies")
