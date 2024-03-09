from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User
from . import views
from fetchLecturers import get_lecturers
from werkzeug.security import generate_password_hash
from . import db


views = Blueprint('views', __name__)

@views.route('/home_admin')
@login_required
def home_admin():
    if current_user.role == 'admin':
        db_path = 'instance/database.db'  
        lecturers = get_lecturers(db_path)
        lecturers_list = [{'id': id, 'email': email, 'first_name': first_name, 'role': role} 
                          for id, email, first_name, role in lecturers]
        return render_template("home_admin.html", user=current_user, lecturers=lecturers_list)
    else:
        flash("You are not authorized to access this page.", category="error")
        return redirect(url_for("views.home"))
    
    
@views.route('/home_lecturer')
@login_required
def home_lecturer():
    if current_user.email.endswith("@rtu.lv") and current_user.email != "admin@rtu.lv":  # Check if user is admin
        return render_template("home_lecturer.html", user=current_user)
    else:
        flash("You are not authorized to access this page.", category="error")
        return redirect(url_for("views.home"))  # Redirect to regular home

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/admin/lecturers')
@login_required
def admin_lecturers():
    if current_user.role != 'admin':
        return "Access denied", 403  # Or handle as appropriate
    lecturers = User.query.filter_by(role='lecturer').all()
    return render_template("admin_lecturers.html", lecturers=lecturers)

@views.route('/add_lecturer', methods=['GET', 'POST'])
@login_required
def add_lecturer():
    if current_user.role == 'admin':
        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Hash the password for security
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Create new User instance for lecturer
            new_lecturer = User(email=email, first_name=first_name + " " + last_name, 
                                password=hashed_password, role='lecturer')
            
            # Add new lecturer to the database
            db.session.add(new_lecturer)
            try:
                db.session.commit()
                flash('Lecturer added successfully!', category='success')
            except:
                db.session.rollback()  # Roll back in case of errors
                flash('Error adding lecturer.', category='error')
            
            return redirect(url_for('views.home_admin'))

        # If GET request or no form submission
        return render_template('add_lecturer.html', user=current_user)  # Include user in context
    else:
        flash("You are not authorized to perform this action.", category='error')
        return redirect(url_for('views.home'))