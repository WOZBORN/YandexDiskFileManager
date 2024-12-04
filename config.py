"""
This module contains the application settings.

The settings are loaded from environment variables using `dotenv` for
development purposes. Default values are provided for most settings to ensure
the application runs out of the box.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Config:
    """Configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): Key for session protection, defaults to 'dev-key'.
        SQLALCHEMY_DATABASE_URI (str): Database connection string, defaults to
            SQLite.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable SQLAlchemy change
            signals.
        YANDEX_API_BASE_URL (str): Base URL for Yandex Disk API.
        YANDEX_OAUTH_TOKEN (str): OAuth token for authenticating with Yandex
            Disk API.
        MAX_CONCURRENT_REQUESTS (int): Max number of concurrent requests,
            defaults to 5.
    """

    # General application settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Yandex API settings
    YANDEX_API_BASE_URL = os.getenv(
        "YANDEX_API_BASE_URL",
        "https://cloud-api.yandex.net/v1/disk/resources"
    )
    YANDEX_OAUTH_TOKEN = os.getenv("YANDEX_OAUTH_TOKEN")

    # Asynchronous task settings
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 5))
