from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm
from app.api import YandexDiskAPI


routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
async def index():
    """
    Главная страница приложения.
    """
    return render_template('index.html', title="Главная страница")


@routes_bp.route('/login', methods=['GET', 'POST'])
async def login():
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
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('routes.index'))


@routes_bp.route('/files', methods=['GET'])
@login_required
async def files():
    """
    Маршрут для отображения списка файлов по публичному ключу Яндекс.Диска.

    Query Parameters:
        public_key (str): Публичный ключ ресурса.

    Returns:
        HTML: Страница со списком файлов.
    """
    public_key = request.args.get('public_key')  # Получаем параметр из строки запроса
    if not public_key:
        flash("Публичный ключ не предоставлен.", "warning")
        return redirect(url_for('routes.index'))

    try:
        files_data = await YandexDiskAPI.get_files(public_key)
        files_list = files_data.get('_embedded', {}).get('items', [])
        return render_template('files.html', title="Список файлов", files=files_list)
    except Exception as e:
        flash(f"Ошибка при получении файлов: {str(e)}", "danger")
        return redirect(url_for('routes.index'))