from flask import render_template, send_from_directory, request

from . import app
from .models import User, Post, Tag

@app.route('/')
def posts_list(page=1):
    # page = request.args.get('page', 1, type=int)
    app.logger.debug(f'Page number: {page}')
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page, app.config['POST_PER_PAGE'], False)
    tags = Tag.query.all()
    return render_template('posts_all.html', posts=posts.items, tags=tags)


@app.route('/posts/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return f'{post}'


@app.route('/post/<int:post_id>/img/')
def post_image(post_id):
    post = Post.query.get_or_404(post_id)
    app.logger.debug(post.img_filename)
    return send_from_directory(app.config['UPLOADS'], post.img_filename)


@app.route('/tag/<int:tag_id>')
def posts_list_by_tag(tag_id):
    return f'All posts with tag {tag_id}'
