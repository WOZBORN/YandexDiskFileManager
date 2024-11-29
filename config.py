import os
from dotenv import load_dotenv

load_dotenv()

# Все эти настройки берутся из переменных окружения (.env)
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key') # Ключ для защиты сессий, по умолчанию 'dev-key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # База данных SQLite по умолчанию
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение сигналов изменений SQLAlchemy

    # API настройки
    YANDEX_API_BASE_URL = os.getenv('YANDEX_API_BASE_URL', 'https://cloud-api.yandex.net/v1/disk/resources')
    YANDEX_OAUTH_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')

    # Асинхронные задачи
    MAX_CONCURRENT_REQUESTS = int(
        os.getenv('MAX_CONCURRENT_REQUESTS', 5))  # Ограничение на количество одновременных запросов, по умолчанию 5