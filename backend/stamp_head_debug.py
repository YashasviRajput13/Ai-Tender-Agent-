import logging
from pathlib import Path
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

load_dotenv(Path('..') / '.env')
logging.basicConfig(level=logging.INFO)
config = Config('alembic.ini')
print('config URL', config.get_main_option('sqlalchemy.url'))
print('script_location', config.get_main_option('script_location'))
try:
    command.stamp(config, 'head')
    print('stamp head succeeded')
except Exception as e:
    print('stamp head failed:', e)
    raise
