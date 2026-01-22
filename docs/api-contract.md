# Proposal Dashboard API Contract

## 1. Base Information
- Base URL (local): http://localhost:8000
- Base URL (dev): https://api.dev.example.com


## 2. Authentication

- Authentication method: JWT (planned)
- Header:
  - Authorization: Bearer {token}

## 3. Proposal APIs

- GET /proposals
- GET /proposals/{id}
- POST /proposals


## 4. Dashboard APIs

- GET /dashboard/kpis
- GET /dashboard/pipeline
- GET /dashboard/recent-proposals


## 5. Common Response Format

```json
{
  "success": true,
  "data": {},
  "message": null
}


👉 모든 API는 이 틀을 따른다 = 불변 규칙

---



## 6. Error Codes

| Code | Meaning |
|-----|--------|
| AUTH_001 | Unauthorized |
| PROP_404 | Proposal not found |
