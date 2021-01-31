import os
from pathlib import Path

storage_path = Path(__file__).parent.joinpath('../app_data').resolve()


class Config:
    DEBUG = False
    TESTING = False
    POST_PER_PAGE = os.getenv('MUSIC_BLOG_POST_PER_PAGE') or 6
    SECRET_KEY = os.getenv('MUSIC_BLOG_SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('MUSIC_BLOG_DSN') or f'sqlite:///{storage_path}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 30
    UPLOADS = os.getenv('MUSIC_BLOG_UPLOADS') or storage_path / 'uploads'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


def get_config(mode):
    app_modes = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return app_modes.get(mode) or DevelopmentConfig
