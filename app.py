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

toolbar = DebugToolbarExtension(app)

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
    redirect("/")


@app.route("/edit/<int:user_id>")
def edit_user():
    "Shows form to create new user"
    return render_template("edit.html")


@app.route("/edit/<int:user_id>", methods=["POST"])
def edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect("/")
