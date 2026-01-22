from sqlalchemy import (
    Column, BigInteger, String, Date, Text,
    Numeric, DateTime
)
from sqlalchemy.sql import func

from app.db import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=False)
    business_domain = Column(String(100))

    owner_name = Column(String(100))
    team_name = Column(String(100))

    idea_date = Column(Date)
    planning_start_date = Column(Date)
    submit_due_date = Column(Date)
    submitted_at = Column(Date)
    result_date = Column(Date)

    expected_amount = Column(Numeric(18, 2))
    currency = Column(String(3), default="KRW")

    priority = Column(String(20))      # HIGH / MEDIUM / LOW
    status = Column(String(30), nullable=False)  # IDEA, WRITING, ...
    stage_note = Column(Text)

    keywords = Column(Text)
    rfp_no = Column(String(100))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
