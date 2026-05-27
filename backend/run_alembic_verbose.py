import logging
from pathlib import Path
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

load_dotenv(Path('..') / '.env')
logging.basicConfig(level=logging.INFO)
config = Config('alembic.ini')
print('Using config URL:', config.get_main_option('sqlalchemy.url'))
command.upgrade(config, 'head')
print('Alembic upgrade head completed')
