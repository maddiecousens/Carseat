"""Modes and database functions for Rideshare Project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Database Models








##############################################################################
# Helper Functions

def connect_db(app):
    """Connect db to Flask app"""

    # Configure connection to PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rideshare'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to Database"