from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class CompanyRead(BaseConfig):
    id: int
    name: str
    website: Optional[str]
    sector: Optional[str]
    location: Optional[str]
    profile: Optional[str]
    created_at: datetime


class UserRead(BaseConfig):
    id: int
    email: str
    name: str
    role: str
    company_id: Optional[int]
    created_at: datetime


class TenderBase(BaseModel):
    source: Optional[str] = Field(default="eprocure")
    source_tender_id: Optional[str]
    title: str
    description: Optional[str] = None
    authority: Optional[str] = None
    deadline: Optional[datetime] = None
    estimated_value: Optional[float] = None
    category: Optional[str] = None
    region: Optional[str] = None
    tender_url: Optional[str] = None
    status: Optional[str] = Field(default="open")
    raw_metadata: Optional[dict[str, Any]] = None


class TenderDocumentRead(BaseConfig):
    id: int
    tender_id: int
    url: str
    filename: Optional[str]
    raw_text: Optional[str]
    parsed_sections: Optional[dict[str, Any]]
    created_at: datetime


class TenderAnalysisRead(BaseConfig):
    id: int
    tender_id: int
    summary: Optional[str]
    eligibility: Optional[List[str]]
    required_documents: Optional[List[str]]
    technical_requirements: Optional[List[str]]
    risk_factors: Optional[List[str]]
    recommendation: Optional[str]
    risk_level: Optional[str]
    risk_reasons: Optional[List[str]]
    category: Optional[str]
    deadline: Optional[str]
    budget: Optional[str]
    confidence_score: Optional[float]
    match_score: Optional[float]
    relevance_score: Optional[float]
    success_probability: Optional[float]
    raw_response: Optional[dict[str, Any]]
    created_at: datetime
    updated_at: datetime


class TenderCreate(TenderBase):
    pass


class TenderRead(TenderBase, BaseConfig):
    id: int
    created_at: datetime
    updated_at: datetime
    analysis: Optional[TenderAnalysisRead] = None
    documents: Optional[List[TenderDocumentRead]] = None


class EligibilityRequirementRead(BaseConfig):
    id: int
    tender_id: int
    requirement_text: str
    matched: bool
    created_at: datetime


class RiskAssessmentRead(BaseConfig):
    id: int
    tender_id: int
    issue: str
    severity: str
    detail: Optional[str]
    created_at: datetime


class NotificationRead(BaseConfig):
    id: int
    user_id: Optional[int]
    tender_id: Optional[int]
    title: str
    message: str
    notification_type: str
    read: bool
    created_at: datetime


class DashboardStats(BaseModel):
    total_tenders: int
    active_tenders: int
    high_match_opportunities: int
    upcoming_deadlines: int
    risk_alerts: int


class RecommendationItem(BaseModel):
    tender_id: int
    title: str
    authority: Optional[str]
    match_score: float
    success_probability: float
    risk_level: Optional[str]
    budget: Optional[str] = None
    deadline: Optional[str] = None


class ScrapeRequest(BaseModel):
    source_url: Optional[str]


class AnalysisRequest(BaseModel):
    tender_id: int


class RecommendationQuery(BaseModel):
    company_id: Optional[int] = None


class ScrapeLogRead(BaseConfig):
    id: int
    source_url: str
    status: str
    message: Optional[str]
    records_scraped: int
    records_created: int
    started_at: datetime
    finished_at: Optional[datetime]


class NotificationCreate(BaseModel):
    title: str
    message: str
    notification_type: str = Field(default="info")
    tender_id: Optional[int] = None
    user_id: Optional[int] = None


class NotificationEmailRequest(BaseModel):
    recipient: str
