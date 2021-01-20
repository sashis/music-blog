import os


class Config:
    POST_PER_PAGE = os.getenv('BLOG_POST_PER_PAGE') or 5
    SECRET_KEY = os.getenv('BLOG_SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('BLOG_DSN') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS = os.getenv('BLOG_UPLOADS') or 'uploads'
