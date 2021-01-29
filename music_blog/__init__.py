from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from .auth import auth, login_manager
from .blog import blog
from .config import Config
from .commands import create_demo_data
from .database import db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

migrations_path = Path(__file__).parent / 'migrations'
migrate = Migrate(app, db, migrations_path)

with app.app_context():
    create_demo_data()

app.register_blueprint(auth)
app.register_blueprint(blog)
