from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    website = Column(String(256), nullable=True)
    sector = Column(String(128), nullable=True)
    location = Column(String(128), nullable=True)
    profile = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    users = relationship("User", back_populates="company", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), nullable=False, unique=True)
    name = Column(String(256), nullable=False)
    role = Column(String(64), nullable=False, default="user")
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    company = relationship("Company", back_populates="users")


class Tender(Base):
    __tablename__ = "tenders"
    __table_args__ = (
        UniqueConstraint("source", "source_tender_id", name="uix_tenders_source_source_tender_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(128), nullable=False, default="cppt")
    source_tender_id = Column(String(128), nullable=True, index=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    authority = Column(String(256), nullable=True)
    deadline = Column(DateTime, nullable=True)
    estimated_value = Column(Float, nullable=True)
    category = Column(String(128), nullable=True)
    region = Column(String(128), nullable=True)
    tender_url = Column(String(512), nullable=True)
    status = Column(String(64), nullable=False, default="open")
    raw_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = relationship("TenderDocument", back_populates="tender", cascade="all, delete-orphan")
    analysis = relationship("TenderAnalysis", back_populates="tender", uselist=False, cascade="all, delete-orphan")
    eligibility_requirements = relationship("EligibilityRequirement", back_populates="tender", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="tender", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="tender", cascade="all, delete-orphan")


class TenderDocument(Base):
    __tablename__ = "tender_documents"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    url = Column(String(512), nullable=False)
    filename = Column(String(256), nullable=True)
    raw_text = Column(Text, nullable=True)
    parsed_sections = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="documents")


class TenderAnalysis(Base):
    __tablename__ = "tender_analysis"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False, unique=True)
    summary = Column(Text, nullable=True)
    eligibility = Column(JSON, nullable=True)
    required_documents = Column(JSON, nullable=True)
    technical_requirements = Column(JSON, nullable=True)
    risk_factors = Column(JSON, nullable=True)
    recommendation = Column(Text, nullable=True)
    risk_level = Column(String(32), nullable=True)
    risk_reasons = Column(JSON, nullable=True)
    category = Column(String(128), nullable=True)
    deadline = Column(String(64), nullable=True)
    budget = Column(String(64), nullable=True)
    confidence_score = Column(Float, nullable=True)
    match_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    success_probability = Column(Float, nullable=True)
    raw_response = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    tender = relationship("Tender", back_populates="analysis")


class EligibilityRequirement(Base):
    __tablename__ = "eligibility_requirements"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    requirement_text = Column(Text, nullable=False)
    matched = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="eligibility_requirements")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    issue = Column(String(256), nullable=False)
    severity = Column(String(32), nullable=False)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="risk_assessments")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=True)
    title = Column(String(256), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(32), nullable=False, default="info")
    read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    tender = relationship("Tender", back_populates="notifications")


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(128), nullable=False)
    event_type = Column(String(128), nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(128), nullable=False)
    entity_id = Column(Integer, nullable=True)
    action = Column(String(128), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class ScraperLog(Base):
    __tablename__ = "scraper_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_url = Column(String(512), nullable=False)
    status = Column(String(32), nullable=False, default="running")
    message = Column(Text, nullable=True)
    records_scraped = Column(Integer, nullable=False, default=0)
    records_created = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
