import os
from pathlib import Path
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

load_dotenv(Path('..') / '.env')
config = Config('alembic.ini')
print('Using config URL:', config.get_main_option('sqlalchemy.url'))
try:
    command.upgrade(config, 'head')
    print('Alembic upgrade head completed')
except Exception as exc:
    print('Alembic error:', exc)
    raise
