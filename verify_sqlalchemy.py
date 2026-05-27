import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()
url = os.getenv("POSTGRES_URL")
if not url:
    raise SystemExit("POSTGRES_URL not set")
if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(url, future=True, echo=False)

async def main():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()
        print(value)
        if value != 1:
            raise SystemExit("SELECT 1 failure")

asyncio.run(main())
