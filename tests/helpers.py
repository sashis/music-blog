from music_blog.models import User, Post, Tag


def user_faker(username, **kwargs):
    kwargs.setdefault('username', username)
    kwargs.setdefault('email', f'{username}@mail')
    kwargs.setdefault('passwd', 'pass')
    kwargs.setdefault('about', f'About {username}.')
    return User(**kwargs)


def post_faker(title, **kwargs):
    kwargs.setdefault('title', title)
    kwargs.setdefault('description', f'{title} description.')
    kwargs.setdefault('body', f'{title} body.')
    return Post(**kwargs)


def tag_faker(name):
    return Tag(name=name)
