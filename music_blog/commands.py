import random
from pathlib import Path
from zipfile import ZipFile
import click
from flask.cli import with_appcontext
from faker import Faker
from flask import current_app

from .database import db
from .models import User, Post, Tag


def _fake_user(faker):
    return User(
        username=faker.user_name(),
        email=faker.email(),
        password='123'
    )


def get_random_sample_image():
    img_path = Path(current_app.config['UPLOADS'])
    img_file = random.choice(list(img_path.glob('*')))
    return img_file.name


def _fake_post(faker, users, tags):
    post = Post(
        title=faker.sentence(),
        img_filename=get_random_sample_image(),
        description=' '.join(faker.sentences(2)),
        body=faker.text(max_nb_chars=1000).replace('\n', '<br>'),
        created_at=faker.date_time_this_year()
    )
    post.author = random.choice(users)
    post.tags.extend(random.choices(tags, k=random.randint(1, 5)))
    return post


def _init_storage():
    db.drop_all()
    db.create_all()
    images_archive = Path(__file__).parent.joinpath('sample_data/sample_images.zip')
    with ZipFile(images_archive) as archive:
        archive.extractall(path=current_app.config['UPLOADS'])


@click.command(name='demo')
@with_appcontext
def fake_db(user_count=3, post_count=60, tag_count=10):
    """Fill the application db with a fake data."""
    _init_storage()
    faker = Faker('ru-RU')
    users = [_fake_user(faker) for _ in range(user_count)]
    tags = [Tag(name=name) for name in faker.words(nb=tag_count, unique=True)]
    posts = [_fake_post(faker, users, tags) for _ in range(post_count)]
    db.session.add_all(users)
    db.session.add_all(tags)
    db.session.add_all(posts)
    db.session.commit()
