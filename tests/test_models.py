from pytest import mark
from sqlalchemy import func, desc

from music_blog.models import User, Post, Tag


def test_get_all_users(db_session):
    usernames = db_session.query(User.username)
    assert sorted(name for name, in usernames) == ['user1', 'user2']


@mark.parametrize("username, post_titles", [
    ('user1', ['post1', 'post2']),
    ('user2', ['post3', 'post4'])
])
def test_get_all_user_posts(db_session, username, post_titles):
    user = db_session.query(User).filter(User.username == username).one()
    user_posts = db_session.query(Post.title).filter_by(author=user)
    assert sorted(title for title, in user_posts) == post_titles


def test_get_tags_popularity(db_session):
    tags_rank = (db_session.query(Tag.name,
                                  func.count(Tag.name).label('post_count')
                                  )
                 .join(Tag.posts)
                 .group_by(Tag.name)
                 .order_by(desc('post_count'))
                 .all()
                 )
    assert tags_rank == [
        ('tag4', 4),
        ('tag3', 3),
        ('tag2', 2),
        ('tag1', 1),
    ]
