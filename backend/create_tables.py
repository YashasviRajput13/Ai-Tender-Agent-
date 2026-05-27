import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

load_dotenv(Path('..') / '.env')
sys.path.insert(0, '.')
from services.tender_service import db, models

async def main():
    async with db.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

asyncio.run(main())
print('Created tables from metadata')
