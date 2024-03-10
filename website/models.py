from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_migrate import Migrate


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(10), default='student')  # Possible values: admin, lecturer, student


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

