from flask import Blueprint
from flask_login import LoginManager

from .models import User

login_manager = LoginManager()
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth.route('/register', methods=['GET', 'POST'])
def register():
    pass


@auth.route('/logout')
def logout():
    pass