from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User, Article
from fetchLecturers import get_lecturers
from fetchStudents import get_students
from fetchArticles import get_articles
from werkzeug.security import generate_password_hash
from . import db
from flask import request
import openpyxl

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
    db_path = 'instance/database.db'  # Update with your database path
    articles = Article.query.all()  # Fetch articles from the database
    return render_template("home.html", user=current_user, articles=articles)


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

# Student list import from .xlsx file
@views.route('/import_students', methods=['POST'])
@login_required
def import_students():
    if 'students_xlsx' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    
    file = request.files['students_xlsx']
    
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        try:
            students_data = read_students_xlsx(file)
            save_students_to_database(students_data)
            flash('Students imported successfully!', category='success')
        except Exception as e:
            flash(f'Error importing students: {str(e)}', category='error')
    else:
        flash('Invalid file format', category='error')
    
    return redirect(url_for('views.home_lecturer'))


def read_students_xlsx(file):
    students_data = []
    try:
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            if len(row) >= 3:  # Ensure the row has at least the required data
                email = row[2] if row[2] else ''
                first_name = row[0] if row[0] else ''
                last_name = row[1] if row[1] else ''
                students_data.append({'email': email, 'first_name': first_name, 'last_name': last_name, 'role': 'student'})
            else:
                raise ValueError('Insufficient values in the row')
        return students_data
    except Exception as e:
        raise e

def save_students_to_database(students_data):
    try:
        for student in students_data:
            # Check if the email already exists in the database
            existing_student = User.query.filter_by(email=student['email']).first()
            if existing_student:
                flash(f'Student with email {student["email"]} already exists.', category='error')
                continue

            # Concatenate first_name and last_name from the xlsx file
            full_name = f"{student['first_name']} {student['last_name']}"
            # Set a standard password for each student
            password1 = "securepassword"
            new_student = User(email=student['email'], 
                               first_name=full_name, 
                               password=password1,
                               role=student['role'])
            db.session.add(new_student)
        db.session.commit()
        flash('Students imported successfully!', category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error importing students: {str(e)}', category='error')
        raise e

#Article import from .xlsx file
@views.route('/upload_articles', methods=['POST'])
def upload_articles():
    if 'articles_xlsx' not in request.files:
        flash('No file part', category='error')
        return redirect(request.url)
    
    file = request.files['articles_xlsx']
    
    if file.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        article_names = read_xlsx_file(file)
        if article_names:
            save_article_names_to_database(article_names)
            flash('Article names uploaded successfully!', category='success')
        else:
            flash('Failed to read article names from file.', category='error')
    else:
        flash('Invalid file format', category='error')
    
    return redirect(url_for('views.home_lecturer'))


def read_xlsx_file(file):
    article_names = []
    try:
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            article_names.append(row[0])
        return article_names
    except Exception as e:
        print(f"Error reading XLSX file: {e}")
        return None

def save_article_names_to_database(article_names):
    try:
        for name in article_names:
            # Check if the article name already exists in the database
            existing_article = Article.query.filter_by(name=name).first()
            if existing_article:
                flash(f'Article with name "{name}" already exists.', category='error')
                continue

            new_article = Article(name=name)
            db.session.add(new_article)
        db.session.commit()
        flash('Article names uploaded successfully!', category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving article names to database: {e}', category='error')
        raise e

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xlsx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
