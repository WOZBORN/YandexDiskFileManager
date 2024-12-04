"""
This module contains the application factory for the Flask application.

It initializes the core components, such as SQLAlchemy, Flask-Migrate,
and Flask-Login. The function `create_app` sets up the application with
configurations and blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Initialize core components
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Create and configure the Flask application.

    This function initializes the Flask application with configurations,
    extensions, and blueprints.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"

    # Register blueprints
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load a user by their ID.

        Args:
            user_id (int): The user ID to load.

        Returns:
            User: The user instance if found, else None.
        """
        from app.models import User
        return User.query.get(int(user_id))

    return app
