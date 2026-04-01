# Proposal Dashboard API Contract

이 문서는 Proposal Dashboard 백엔드에 **현재 구현되어 있는 API**의
엔드포인트, 역할, 입력/출력 규칙을 정의한다.

미래 계획이나 미구현 기능은 포함하지 않는다.

---

## 1. Base Information

- Base URL (local): http://localhost:8000
- Base URL (dev): TBD

---

## 2. Authentication

- 현재 버전에서는 인증을 적용하지 않는다.
- JWT 인증은 향후 도입 예정이며, 도입 시 이 문서를 갱신한다.

---

## 3. Common Response Rule (중요)

- 모든 API는 성공 시 HTTP 2xx 상태코드를 반환한다.
- 실패 시 HTTP 4xx/5xx 상태코드를 사용한다.
- 현재는 **공통 response wrapper를 강제하지 않는다.**
  (향후 도입 가능성 있음)

---

## 4. Root API

### GET /

- 설명: API 헬스체크 및 루트 확인
- 응답 예시: 
json
{
  "message": "Proposal Dashboard API running"
}


## 5. Proposal APIs (/proposals)
Proposal은 우리 회사 내부에서 관리하는 제안 단위를 의미한다.

### 5.1 GET /proposals/
설명: 제안 목록 조회 (필터 + 기간 조회)

Query Parameters:

status (multiple)

client_name

owner_name

q (검색어)

from_date

to_date

skip

limit

Response:

List[ProposalRead]

### 5.2 GET /proposals/recent-in-progress
설명: 최근 진행 중 상태의 제안 목록 조회

Query Parameters:

limit

Response:

List[ProposalRead]

### 5.3 GET /proposals/filters/options
설명: 제안 필터 UI를 위한 옵션 정보 제공

Response 예시:

{
  "clients": [...],
  "owners": [...]
}

### 5.4 POST /proposals/
설명: 제안 생성

Request Body:

ProposalCreate

Response:

ProposalRead

Status Code:

201 Created

### 5.5 GET /proposals/{id}
설명: 특정 제안 상세 조회

Path Parameter:

id

Response:

ProposalRead

### 5.6 PATCH /proposals/{id}
설명: 제안 정보 수정

Path Parameter:

id

Request Body:

ProposalUpdate

Response:

ProposalRead

## 6. Stats APIs (/stats)
Stats API는 대시보드 화면을 위한 집계용 API이다.

### 6.1 GET /stats/summary
설명: 대시보드 상단 KPI 요약 정보

Response 내용:

신규 제안 수

진행 중 제안 수

올해 Won 제안 건수

올해 Won 제안 금액

### 6.2 GET /stats/pipeline
설명: 제안 단계별 파이프라인 통계

Response 내용:

상태별 제안 건수

상태별 예상 금액 합계 (total_expected_amount)

## 7. Error Handling
존재하지 않는 리소스 요청 시 404를 반환한다.
잘못된 요청 파라미터는 422를 반환한다.
내부 오류는 500을 반환한다.
