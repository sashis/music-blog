from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db


class User(db.Model):
    __repr_attr__ = 'username'

    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    _password = db.Column('password_hash', db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_passwd):
        self._password = generate_password_hash(plain_passwd)

    def check_password(self,plain_passwd):
        return check_password_hash(self.password, plain_passwd)


posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Tag(db.Model):
    __repr_attr__ = 'name'

    name = db.Column(db.String(32), unique=True, nullable=False)


class Post(db.Model):
    __repr_attr__ = 'title'

    title = db.Column(db.String(80), nullable=False)
    img_filename = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(170))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    view_count = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    tags = db.relationship(Tag, secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'), lazy='dynamic')
