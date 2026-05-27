from alembic.config import Config
from alembic.script import ScriptDirectory

config = Config('alembic.ini')
print('config url:', config.get_main_option('sqlalchemy.url'))
script = ScriptDirectory.from_config(config)
print('script dir:', script.dir)
print('revisions:')
for rev in script.walk_revisions('base', 'heads'):
    print('  ', rev.revision, rev.doc)
