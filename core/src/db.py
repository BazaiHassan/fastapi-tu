# core/src/db.py
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from typing import Generator

# ✅ ONLY declare Base here — NOTHING ELSE
Base = declarative_base()

# ✅ Delay engine and session creation until called
def get_engine():
    from core.src.config import settings  # ← Import ONLY when needed
    return create_engine(settings.SQLALCHEMY_DATABASE_URL)

def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

def get_db() -> Generator:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()