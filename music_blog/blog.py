from flask import Blueprint, current_app, render_template, send_from_directory, request

from .database import db
from .models import Post, Tag

blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/posts/')
def posts_list(item_id=None):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc())
    context = {
        'header': 'Блог о любимой музыке и темах, с ней связанных',
        'item_id': item_id,
        'pagination': posts.paginate(page, current_app.config['POST_PER_PAGE'], False),
        'tags': Tag.query.all()
    }
    return render_template('paginated_list.html', **context)


@blog.route('/posts/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    post.view_count += 1
    db.session.commit()
    return render_template('post_detail.html', post=post, title=post.title)


@blog.route('/posts/<int:post_id>/img/')
def post_image(post_id):
    post = Post.query.get_or_404(post_id)
    return send_from_directory(current_app.config['UPLOADS'], post.img_filename)


@blog.route('/tags/<int:item_id>/')
def posts_list_by_tag(item_id):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.get_or_404(item_id)
    posts_by_tag = tag.posts.order_by(Post.created_at.desc())
    context = {
        'header': f'Статьи с тегом "{tag.name}"',
        'title': f'{tag.name}',
        'item_id': item_id,
        'pagination': posts_by_tag.paginate(page, current_app.config['POST_PER_PAGE'], False),
        'tags': Tag.query.all()
    }
    return render_template('paginated_list.html', **context)
