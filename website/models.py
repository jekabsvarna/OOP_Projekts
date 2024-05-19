from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_migrate import Migrate
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(10), default='student')  


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)



class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lecturer = db.relationship('User', backref='workshops')

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))
    student = db.relationship('User', backref='enrollments')
    workshop = db.relationship('Workshop', backref='students')