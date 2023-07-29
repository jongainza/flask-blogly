"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import text
from models import db, connect_db, User, Post


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.app_context().push()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "jongainza"

# toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route("/")
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/", methods=["POST"], endpoint="create_user")
def create():
    """Handle form submission for creating a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image = request.form["image"]

    new_user = User(first_name=first_name, last_name=last_name, image=image)
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.first_name} added.")

    return redirect(f"/{new_user.id}")


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.all()
    return render_template("details.html", user=user, posts=posts)


@app.route("/create_user")
def show_create_user_form():
    "Shows form to create new user"
    return render_template("form.html")


@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    "Deletes user"
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route("/edit/<int:user_id>", methods=["GET"])
def edit_user(user_id):
    "Shows form to edit user"
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/edit/<int:user_id>", methods=["POST"])
def edit(user_id):
    user = User.query.get_or_404(user_id)
    new_first_name = request.form["first_name"]
    if not new_first_name:
        new_first_name = user.first_name
    new_last_name = request.form["last_name"]
    if not new_last_name:
        new_last_name = user.last_name
    new_image = request.form["image"]
    if not new_image:
        new_image = user.image

    user.first_name = new_first_name
    user.last_name = new_last_name
    user.image = new_image

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/add_post/<int:user_id>")
def show_create_post_form(user_id):
    """Shows form to create a new post"""
    user = User.query.get_or_404(user_id)
    return render_template("post_form.html", user=user)


@app.route("/new_post/<int:user_id>", methods=["POST"], endpoint="create_post")
def create_post(user_id):
    """Handles form submission to create a new post"""
    title = request.form["title"]
    content = request.form["content"]

    user = User.query.get_or_404(user_id)
    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/{user_id}")


@app.route("/post/details/<int:post_id>")
def post_details(post_id):
    """show details about post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    "Deletes post"
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


@app.route("/post/edit/<int:post_id>", methods=["GET"])
def edit_post(post_id):
    "Shows form to edit post"
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/post/edit/<int:post_id>", methods=["POST"])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    new_title = request.form["title"]
    if not new_title:
        new_title = post.title
    new_content = request.form["content"]
    if not new_content:
        new_content = post.content

    post.title = new_title
    post.content = new_content
    post.user_id = post.user_id

    db.session.add(post)
    db.session.commit()

    return redirect(f"/post/details/{post.id}")
