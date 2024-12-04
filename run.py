"""
This module serves as the entry point for the Flask application.

It initializes the application using the factory method `create_app` and
starts the development server when run as the main module.
"""

from app import create_app

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode for development
    app.run(debug=True)
