from pathlib import Path

import click
from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from .auth import auth, login_manager
from .blog import blog
from .config import get_config
from .commands import fake_db
from .database import db


def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(get_config(mode))

    db.init_app(app)
    login_manager.init_app(app)

    migrations_path = Path(__file__).parent / 'migrations'
    Migrate(app, db, migrations_path)
    app.cli.add_command(fake_db)
    app.register_blueprint(auth)
    app.register_blueprint(blog)
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Music Blog application."""
