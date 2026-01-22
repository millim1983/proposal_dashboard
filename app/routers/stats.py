# app/routers/stats.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select, and_

from app.db import SessionLocal
from app import models
from app.schemas import ProposalStatus

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
):
    """대시보드 상단 KPI 요약용 API"""

    today = date.today()
    first_day_month = today.replace(day=1)
    first_day_year = today.replace(month=1, day=1)

    # 이번 달 신규 제안 (created_at 기준)
    stmt_new_month = (
        select(func.count(models.Proposal.id))
        .where(models.Proposal.created_at >= first_day_month)
    )
    new_proposals_this_month = db.execute(stmt_new_month).scalar() or 0

    # 진행 중 제안 수 (WRITING ~ RESULT_PENDING)
    in_progress_status = [
        ProposalStatus.WRITING.value,
        ProposalStatus.INTERNAL_REVIEW.value,
        ProposalStatus.SUBMITTED.value,
        ProposalStatus.RESULT_PENDING.value,
    ]
    stmt_in_progress = (
        select(func.count(models.Proposal.id))
        .where(models.Proposal.status.in_(in_progress_status))
    )
    in_progress_count = db.execute(stmt_in_progress).scalar() or 0

    # 올해 WON 건수
    stmt_won_count = (
        select(func.count(models.Proposal.id))
        .where(
            and_(
                models.Proposal.status == ProposalStatus.WON.value,
                models.Proposal.result_date >= first_day_year,
            )
        )
    )
    won_count = db.execute(stmt_won_count).scalar() or 0

    # 올해 WON 금액 합계
    stmt_won_amount = (
        select(func.coalesce(func.sum(models.Proposal.expected_amount), 0))
        .where(
            and_(
                models.Proposal.status == ProposalStatus.WON.value,
                models.Proposal.result_date >= first_day_year,
            )
        )
    )
    won_amount = float(db.execute(stmt_won_amount).scalar() or 0)

    return {
        "new_proposals_this_month": new_proposals_this_month,
        "in_progress_count": in_progress_count,
        "won_count_this_year": won_count,
        "won_amount_this_year": won_amount,
        "currency": "KRW",
    }


@router.get("/pipeline")
def get_pipeline_stats(
    db: Session = Depends(get_db),
):
    """단계별 파이프라인(건수/금액)용 API"""

    stmt = (
        select(
            models.Proposal.status,
            func.count(models.Proposal.id),
            func.coalesce(func.sum(models.Proposal.expected_amount), 0),
        )
        .group_by(models.Proposal.status)
    )

    rows = db.execute(stmt).all()
    row_map = {status: (count, amount) for status, count, amount in rows}

    ordered_statuses = [
        ProposalStatus.IDEA,
        ProposalStatus.PLANNING,
        ProposalStatus.WRITING,
        ProposalStatus.INTERNAL_REVIEW,
        ProposalStatus.SUBMITTED,
        ProposalStatus.RESULT_PENDING,
        ProposalStatus.WON,
        ProposalStatus.LOST,
    ]

    pipeline = []
    for s in ordered_statuses:
        count, amount = row_map.get(s.value, (0, 0))
        pipeline.append(
            {
                "status": s.value,
                "count": int(count or 0),
                "total_expected_amount": float(amount or 0),
            }
        )

    return {"pipeline": pipeline}
