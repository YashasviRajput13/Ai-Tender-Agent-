import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect
import asyncio

load_dotenv()
url = os.getenv('POSTGRES_URL')
if not url:
    raise SystemExit('POSTGRES_URL not set')
if url.startswith('postgresql://') and not url.startswith('postgresql+asyncpg://'):
    url = url.replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_async_engine(url, future=True, echo=False)

async def main():
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        print('tables:', tables)

asyncio.run(main())
