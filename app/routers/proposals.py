from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.db import SessionLocal
from app import models
from app.schemas import (
    ProposalStatus,
    ProposalCreate,
    ProposalUpdate,
    ProposalRead,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1) 제안 목록 조회 (필터 + 기간)
@router.get("/", response_model=List[ProposalRead])
def list_proposals(
    db: Session = Depends(get_db),
    status: Optional[List[ProposalStatus]] = Query(
        None, description="상태 멀티 선택"
    ),
    client_name: Optional[str] = None,
    owner_name: Optional[str] = None,
    q: Optional[str] = Query(None, description="제목/고객사/키워드 검색"),
    from_date: Optional[date] = Query(
        None, description="기간 시작 (submit_due_date 기준)"
    ),
    to_date: Optional[date] = Query(
        None, description="기간 종료 (submit_due_date 기준)"
    ),
    skip: int = 0,
    limit: int = 50,
):
    stmt = select(models.Proposal)

    # 상태 멀티 필터
    if status:
        status_values = [s.value for s in status]
        stmt = stmt.where(models.Proposal.status.in_(status_values))

    if client_name:
        stmt = stmt.where(models.Proposal.client_name.ilike(f"%{client_name}%"))

    if owner_name:
        stmt = stmt.where(models.Proposal.owner_name.ilike(f"%{owner_name}%"))

    if q:
        like_q = f"%{q}%"
        stmt = stmt.where(
            (models.Proposal.title.ilike(like_q))
            | (models.Proposal.client_name.ilike(like_q))
            | (models.Proposal.keywords.ilike(like_q))
        )

    # 기간 필터 (제출 마감일 기준)
    if from_date:
        stmt = stmt.where(models.Proposal.submit_due_date >= from_date)
    if to_date:
        stmt = stmt.where(models.Proposal.submit_due_date <= to_date)

    # 기본 정렬: 최근 업데이트 순
    stmt = stmt.order_by(models.Proposal.updated_at.desc())

    stmt = stmt.offset(skip).limit(limit)
    proposals = db.execute(stmt).scalars().all()
    return proposals


# 2) 최근 진행 중 제안 (대시보드 하단 테이블용)
@router.get("/recent-in-progress", response_model=List[ProposalRead])
def recent_in_progress(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    in_progress_status = [
        ProposalStatus.WRITING.value,
        ProposalStatus.INTERNAL_REVIEW.value,
        ProposalStatus.SUBMITTED.value,
        ProposalStatus.RESULT_PENDING.value,
        ProposalStatus.PLANNING.value,
        ProposalStatus.IDEA.value,
    ]

    stmt = (
        select(models.Proposal)
        .where(models.Proposal.status.in_(in_progress_status))
        .order_by(models.Proposal.updated_at.desc())
        .limit(limit)
    )

    proposals = db.execute(stmt).scalars().all()
    return proposals


# 3) 필터 옵션 (고객사/담당자 드롭다운용)
@router.get("/filters/options")
def get_filter_options(
    db: Session = Depends(get_db),
):
    clients_stmt = (
        select(func.distinct(models.Proposal.client_name))
        .order_by(models.Proposal.client_name)
    )
    owners_stmt = (
        select(func.distinct(models.Proposal.owner_name))
        .order_by(models.Proposal.owner_name)
    )

    clients = [c for c in db.execute(clients_stmt).scalars().all() if c]
    owners = [o for o in db.execute(owners_stmt).scalars().all() if o]

    return {
        "clients": clients,
        "owners": owners,
    }


# 4) 제안 생성
@router.post("/", response_model=ProposalRead, status_code=status.HTTP_201_CREATED)
def create_proposal(
    payload: ProposalCreate,
    db: Session = Depends(get_db),
):
    proposal = models.Proposal(**payload.model_dump())
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


# 5) 제안 상세 조회  ← ※ 동적 경로는 아래쪽으로
@router.get("/{id}", response_model=ProposalRead)
def get_proposal(
    id: int,
    db: Session = Depends(get_db),
):
    proposal = db.get(models.Proposal,id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


# 6) 제안 수정
@router.patch("/{id}", response_model=ProposalRead)
def update_proposal(
    id: int,
    payload: ProposalUpdate,
    db: Session = Depends(get_db),
):
    proposal = db.get(models.Proposal, id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(proposal, field, value)

    db.commit()
    db.refresh(proposal)
    return proposal
