import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
dotenv_path = Path(ROOT_DIR) / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

def normalize_database_url(url: str | None) -> str | None:
    if url is None:
        return None
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL"))
if not DATABASE_URL:
    sqlite_path = Path(ROOT_DIR) / "agentic_ai_tender.db"
    DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    pool_pre_ping=True,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
