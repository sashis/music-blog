from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email(message="Некорректный адрес электронной почты")])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        EqualTo('confirm', message='Пароли не совпадают')
    ])
    confirm = PasswordField('Снова пароль', validators=[DataRequired()])