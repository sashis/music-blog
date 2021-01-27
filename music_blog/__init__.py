from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

import music_blog.models
from .config import Config
from .database import db
from .auth import login_manager
from .commands import create_demo_data


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

migrations_path = Path(__file__).parent / 'migrations'
migrate = Migrate(app, db, migrations_path)


with app.app_context():
    create_demo_data()
import music_blog.views  # noqa: E402
