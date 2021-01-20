from datetime import datetime

from .database import db


class User(db.Model):
    __repr_attr__ = 'username'

    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    passwd = db.Column(db.String(128), nullable=False)
    about = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author')


class Post(db.Model):
    __repr_attr__ = 'title'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', onupdate='CASCADE', ondelete='SET NULL')
    )
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(170))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False, default= datetime.utcnow(), onupdate=datetime.utcnow())
    is_published = db.Column(db.Boolean, nullable=False, default=False)


posts_tags = db.Table(
    'posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Tag(db.Model):
    __repr_attr__ = 'name'

    name = db.Column(db.String(32), unique=True, nullable=False)
    posts = db.relationship(Post, secondary=posts_tags, backref='tags')
