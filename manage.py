import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

env = os.getenv("FLASK_ENV") or "test"
print(f"Active environment: * {env} *")
app = create_app(env)

manager = Manager(app)
app.app_context().push()
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
