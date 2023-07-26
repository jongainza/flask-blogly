"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import text
from models import db, connect_db, User


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


@app.route("/", methods=["POST"])
def create():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image = request.form["image"]

    new_user = User(first_name=first_name, last_name=last_name, image=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")


@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/create_user")
def create_user():
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
    "Shows form to create new user"
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
