from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
#To run this file: On venv run >python -m unittest test_flask.py
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()
url = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class UsersViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        user = User(first_name="TestRama", last_name="TestSrinivas", image_url=url)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestRama', html)

    def test_(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add New User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            u = {"first_name": "TestKelly", "last_name": "Test John", "image_url": url}
            resp = client.post("/users/new", data=u, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            #self.assertIn("<h1>TestPet2</h1>", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            #self.assertIn('<h1>TestPet</h1>', html)