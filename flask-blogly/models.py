"""Models for Blogly."""
"""Demo file showing off a model for SQLAlchemy."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
    

# Add users
#user1 = User(first_name='Rama', last_name="Srinivas")


# Add new objects to session, so they'll persist
#db.session.add(user1)

# Commit--otherwise, this never gets saved!
#db.session.commit()