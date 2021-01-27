from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user

from .models import User
from .forms import LoginForm

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('blog.posts_list'))
        else:
            flash("Неверные логин и/или пароль.")
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.posts_list'))
