"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def root():
    """Landing Page get's redirected to /users."""
    return redirect("/users")

@app.route("/users")
def list_users():
    """Show a page with info on all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    #iterate through list
    return render_template('users.html', users=users)

@app.route("/users/new")
def show_user_form():
    """Show the form to add user"""
    return render_template('add_user_form.html')

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to list."""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("show.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

##############################################################################
# Posts route
@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show post form on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("/posts/new.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_post(user_id):
    """."""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    #flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")
