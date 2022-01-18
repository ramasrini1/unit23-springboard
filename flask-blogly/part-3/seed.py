"""Seed file to make sample data for pets db."""

from models import User, Post, db, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user1 = User(first_name='Rama', last_name="Srinivas")
user2 = User(first_name='Kelly', last_name="John")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)

# Commit--otherwise, this never gets saved!
db.session.commit()


Post.query.delete()
# Add Post
post1 = Post(title='Go Green', content="Save Planet Go green", created_at=None, user_id=1)
# Add new objects to session, so they'll persist
db.session.add(post1)

# Commit--otherwise, this never gets saved!
db.session.commit()