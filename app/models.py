"""
This module defines database models for the application.

It includes the User model for managing user data and authentication,
and the FileCache model for caching file metadata from Yandex Disk.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model, UserMixin):
    """Model representing a user in the application.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password for authentication.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.

        Args:
            password (str): The plaintext password to hash and store.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if a plaintext password matches the stored hash.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)


class FileCache(db.Model):
    """Model for caching file metadata from Yandex Disk.

    Attributes:
        id (int): Unique identifier for the cached file.
        public_key (str): Public key associated with the file.
        file_name (str): Name of the cached file.
        file_path (str): Path of the cached file.
        cached_at (datetime): Timestamp when the file was cached.
    """

    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(256), nullable=False)
    file_name = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    cached_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )
