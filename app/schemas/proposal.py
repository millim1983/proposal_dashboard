from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProposalStatus(str, Enum):
    IDEA = "IDEA"
    PLANNING = "PLANNING"
    WRITING = "WRITING"
    INTERNAL_REVIEW = "INTERNAL_REVIEW"
    SUBMITTED = "SUBMITTED"
    RESULT_PENDING = "RESULT_PENDING"
    WON = "WON"
    LOST = "LOST"


class ProposalPriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ProposalBase(BaseModel):
    title: str = Field(..., max_length=255)
    client_name: str
    business_domain: Optional[str] = None

    owner_name: Optional[str] = None
    team_name: Optional[str] = None

    idea_date: Optional[date] = None
    planning_start_date: Optional[date] = None
    submit_due_date: Optional[date] = None
    submitted_at: Optional[date] = None
    result_date: Optional[date] = None

    expected_amount: Optional[float] = None
    currency: Optional[str] = "KRW"

    priority: Optional[ProposalPriority] = None
    status: ProposalStatus
    stage_note: Optional[str] = None

    keywords: Optional[str] = None
    rfp_no: Optional[str] = None


class ProposalCreate(ProposalBase):
    pass


class ProposalUpdate(BaseModel):
    title: Optional[str] = None
    client_name: Optional[str] = None
    business_domain: Optional[str] = None

    owner_name: Optional[str] = None
    team_name: Optional[str] = None

    idea_date: Optional[date] = None
    planning_start_date: Optional[date] = None
    submit_due_date: Optional[date] = None
    submitted_at: Optional[date] = None
    result_date: Optional[date] = None

    expected_amount: Optional[float] = None
    currency: Optional[str] = None

    priority: Optional[ProposalPriority] = None
    status: Optional[ProposalStatus] = None
    stage_note: Optional[str] = None

    keywords: Optional[str] = None
    rfp_no: Optional[str] = None


class ProposalRead(ProposalBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
