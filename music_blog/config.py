import os
from pathlib import Path

storage_path = Path('../app_data').resolve()


class Config:
    POST_PER_PAGE = os.getenv('BLOG_POST_PER_PAGE') or 6
    SECRET_KEY = os.getenv('BLOG_SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('BLOG_DSN') or f'sqlite:///{storage_path}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 30
    UPLOADS = os.getenv('BLOG_UPLOADS') or storage_path / 'uploads'
