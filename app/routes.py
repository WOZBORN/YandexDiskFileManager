"""
This module handles user routes for the Flask application.

It defines routes for user authentication, file browsing, and the main page.
Routes include login, registration, logout, and integration
with Yandex.Disk API.
"""

from aiohttp import ClientError
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm
from app.api import YandexDiskAPI


# Define blueprint for user routes
routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
async def index():
    """Render the main page of the application.

    Returns:
        str: Rendered HTML template for the main page.
    """
    return render_template('index.html', title="Главная страница")


@routes_bp.route('/login', methods=['GET', 'POST'])
async def login():
    """Handle user login.

    GET: Render the login page.
    POST: Authenticate the user and redirect to the main page.

    Returns:
        str: Rendered HTML template or a redirect response.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('routes.index'))
        flash('Неверные email или пароль!', 'danger')
    return render_template('auth/login.html', form=form)


@routes_bp.route('/register', methods=['GET', 'POST'])
async def register():
    """Handle user registration.

    GET: Render the registration page.
    POST: Register a new user and redirect to the login page.

    Returns:
        str: Rendered HTML template or a redirect response.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Войдите в систему.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('auth/register.html', form=form)


@routes_bp.route('/logout')
@login_required
async def logout():
    """Handle user logout.

    Logs the user out and redirects to the main page.

    Returns:
        str: Redirect response to the main page.
    """
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('routes.index'))


@routes_bp.route('/files', methods=['GET'])
@login_required
async def files():
    """Browse files from Yandex.Disk.

    Retrieves file data from Yandex.Disk API based on the provided public key
    and optional path. If successful, renders a file browser page.

    GET: Retrieve file data from Yandex.Disk API.

    Query Parameters:
        public_key (str): Public key for accessing Yandex.Disk.
        path (str): Path to a specific folder on Yandex.Disk (optional).

    Returns:
        str: Rendered HTML template for the file browser or a redirect response.
    """
    public_key = request.args.get('public_key')  # Current public key
    path = request.args.get('path')
    if not public_key:
        flash("Публичный ключ не предоставлен.", "warning")
        return redirect(url_for('routes.index'))

    try:
        # Fetch data from Yandex.Disk API
        files_data = await YandexDiskAPI.get_files(public_key, path or '/')
        files_list = files_data.get('_embedded', {}).get('items', [])

        # Save the last response for debugging
        with open('last_response.json', 'w', encoding='utf-8') as f:
            f.write(str(files_data))

        return render_template(
            'files.html',
            title="Список файлов",
            files=files_list,
            public_key=public_key,
            path=path
        )
    except ClientError as e:
        flash(f"Ошибка при получении файлов: {str(e)}", "danger")
        return redirect(url_for('routes.index'))
