import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL가 .env에 설정되어 있지 않습니다.")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 찍어보고 싶으면 True, 너무 시끄러우면 False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
