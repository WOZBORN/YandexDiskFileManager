"""
This module defines forms for user authentication and registration.

The forms use Flask-WTF and WTForms for handling user input validation and
rendering.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    """Form for user login.

    Attributes:
        email (StringField): Field for the user's email address.
        password (PasswordField): Field for the user's password.
        submit (SubmitField): Submit button to log in.
    """
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message="Введите корректный email.")
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message="Пароль обязателен.")
        ]
    )
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Form for user registration.

    Attributes:
        username (StringField): Field for the user's username.
        email (StringField): Field for the user's email address.
        password (PasswordField): Field for the user's password.
        confirm_password (PasswordField): Field for confirming the password.
        submit (SubmitField): Submit button to register.
    """
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(message="Имя пользователя обязательно."),
            Length(
                min=3,
                max=20,
                message="Имя пользователя должно быть от 3 до 20 символов.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email обязателен."),
            Email(message="Введите корректный email.")
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message="Пароль обязателен."),
            Length(
                min=6,
                message="Пароль должен содержать не менее 6 символов."
            )
        ]
    )
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[
            DataRequired(message="Подтверждение пароля обязательно."),
            EqualTo('password', message="Пароли должны совпадать.")
        ]
    )
    submit = SubmitField('Зарегистрироваться')
