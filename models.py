"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import text

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tanblename__ = "users"

    def __repr__(self):
        u = self
        return f"User id={u.id} first_name={u.first_name} last_name={u.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=True)
    image = db.Column(
        db.String,
        nullable=False,
        default=" https://media.istockphoto.com/id/1143500885/vector/man-portrait-with-beard-vector-illustration-of-male-character.jpg?s=612x612&w=0&k=20&c=v9pv64ASjUYTRscfrYXEeof-oI2IfTPwJPuxRWNeG74=",
    )

    def greet(self):
        return f" Hi, I'm {self.first_name} {self.last_name} and this is my picture"
