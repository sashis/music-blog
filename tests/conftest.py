from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from music_blog.models import Base
from .helpers import user_faker, post_faker, tag_faker


@fixture(scope='session')
def engine():
    return create_engine('sqlite://')


@fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    users = list(map(user_faker, ('user1', 'user2')))
    posts = list(map(post_faker, ('post1', 'post2', 'post3', 'post4')))
    tags = list(map(tag_faker, ('tag1', 'tag2', 'tag3', 'tag4')))
    users[0].posts = posts[:2]
    users[1].posts = posts[2:]
    posts[0].tags = tags[:]
    posts[1].tags = tags[1:]
    posts[2].tags = tags[2:]
    posts[3].tags = tags[3:]
    session = Session(bind=engine)
    session.add_all(users)
    session.add_all(posts)
    session.add_all(tags)
    session.commit()
    session.close()
    yield
    Base.metadata.drop_all(engine)


@fixture
def db_session(tables, engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
