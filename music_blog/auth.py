from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from .database import db
from .models import User
from .forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_url = request.args.get('next')
            return redirect(next_url or '/')
        else:
            flash("Неверные логин и/или пароль.")
    return render_template('login.html', title='Авторизация', form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        if User.is_exist(form.username.data, form.email.data):
            flash('Пользователь с таким логином или почтой уже существует')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('blog.posts_list'))
