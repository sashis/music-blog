import os
from pathlib import Path

from . import app

class Config:
    POST_PER_PAGE = os.getenv('BLOG_POST_PER_PAGE') or 6
    SECRET_KEY = os.getenv('BLOG_SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('BLOG_DSN') or f'sqlite:///{app.instance_path}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SEND_FILE_MAX_AGE_DEFAULT = 30
    UPLOADS = os.getenv('BLOG_UPLOADS') or Path(app.instance_path) / 'uploads'
