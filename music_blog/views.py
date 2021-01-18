from . import app


@app.route('/')
def posts_list():
    return 'All posts'


@app.route('/post/<int:post_id>/')
def post_detail(post_id):
    return f'Single post {post_id} page'


@app.route('/post/<int:post_id>/img/')
def post_image(post_id):
    return f'Post {post_id} image'


@app.route('/tag/<int:tag_id>')
def posts_list_by_tag(tag_id):
    return f'All posts with tag {tag_id}'
