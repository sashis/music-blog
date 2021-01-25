from flask import render_template

from . import app
from .models import User, Post, Tag

@app.route('/')
def posts_list():
    posts = Post.query.all()
    return render_template('posts_all.html', posts=posts)


@app.route('/post/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return f'{post}'


@app.route('/post/<int:post_id>/img/')
def post_image(post_id):
    return f'Post {post_id} image'


@app.route('/tag/<int:tag_id>')
def posts_list_by_tag(tag_id):
    return f'All posts with tag {tag_id}'
