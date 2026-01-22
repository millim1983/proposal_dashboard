from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ★ 추가
from app.routers import proposals, stats
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proposal Dashboard API",
    version="0.1.0",
)

# ★ CORS 설정
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proposals.router, prefix="/proposals", tags=["proposals"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/")
def read_root():
    return {"message": "Proposal Dashboard API running"}
