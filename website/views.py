from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User
from . import views
from fetchLecturers import get_lecturers
from fetchStudents import get_students
from werkzeug.security import generate_password_hash
from . import db
import csv
import io


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
        db_path = 'instance/database.db'  
        students = get_students(db_path)
        students_list = [{'id': id, 'email': email, 'first_name': first_name, 'role': role} 
                          for id, email, first_name, role in students]
        return render_template("home_lecturer.html", user=current_user, students=students_list)
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
    
# Pasniedzejam skatities studentu sarakstu
@views.route('/lecturer/students')
@login_required
def lecturer_students():
    if current_user.role != 'lecturer':  # Assuming 'role' attribute exists and is 'lecturer' for lecturers
        flash('You do not have access to this page.', category='error')
        return redirect(url_for('views.home'))
    students = User.query.all()
    return render_template('lecturer_students.html', students=students)



# Student list import from .csv file

@views.route('/import_students', methods=['GET', 'POST'])
@login_required
def import_students():
    if request.method == 'POST':
        # Check if there is a file in the request
        if 'students_csv' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['students_csv']
        # If the user does not select a file, browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.DictReader(stream)
            for row in csv_input:
                # Here you would add your logic to process each row; this is just an example
                new_student = User(email=row['email'], password=row['password'], first_name=row['first_name'], role='student')
                db.session.add(new_student)
            db.session.commit()
            flash('Students imported successfully!', category='success')
            return redirect(url_for('views.home_admin'))  # Or wherever you want to redirect
        else:
            flash('Invalid file format', category='error')
    return render_template('import_students.html')

