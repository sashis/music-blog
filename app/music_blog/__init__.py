from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from .database import db
from .auth import auth, login_manager
from .blog import blog
from .commands import create_demo_data


app = Flask(__name__)

from .config import Config
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

migrations_path = Path(__file__).parent / 'migrations'
migrate = Migrate(app, db, migrations_path)

with app.app_context():
    app.logger.debug(f'{app.instance_path=}')
    create_demo_data()

app.register_blueprint(auth)
app.register_blueprint(blog)
