from datetime import datetime
import sqlalchemy as sa

from . import db


class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id = sa.Column(sa.Integer, primary_key=True)

    def __repr__(self):
        attr = getattr(self, '__repr_attr__', 'id')
        value = getattr(self, attr, 'unknown')
        return f'<{self.__class__.__name__} {value}>'


class User(db.Model):
    __repr_attr__ = 'username'

    username = db.Column(sa.String(64), index=True, unique=True)
    email = db.Column(sa.String(128), index=True, unique=True)
    passwd = db.Column(sa.String(128), nullable=False)
    about = db.Column(sa.String(128))

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
    'posts_tags', Base.metadata,
    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id')),
    sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id'))
)


class Tag(Base):
    __repr_attr__ = 'name'

    name = sa.Column(sa.String(32), unique=True, nullable=False)
    posts = relationship(Post, secondary=posts_tags, backref='tags')


class Comment(Base):
    __repr_attr__ = 'body'

    post_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    body = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow())

    author = relationship(User, backref='comments')
    post = relationship(Post, backref='comments')
