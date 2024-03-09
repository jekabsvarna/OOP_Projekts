from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
import hashlib
from. import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

auth = Blueprint('auth', __name__)

# Example function to add a user (simplified for illustration)
def register_user(email, password, first_name, role='lecturer'):  # Add role parameter
    new_user = User(email=email, password=password, first_name=first_name, role=role)
    db.session.add(new_user)
    db.session.commit()



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:  # In a real application, ensure password is securely hashed and checked
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                
                # Check for user role instead of email
                if user.role == "admin":  # Adjust the role string as necessary
                    return redirect(url_for('views.home_admin'))
                elif user.role == "lecturer":  # Adjust the role string as necessary
                    return redirect(url_for('views.home_lecturer'))  # Redirect to lecturer page
                else:  # Default redirection for other roles or if no role is set
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created.', category='success')
            return redirect(url_for('auth.login'))  # Redirect to login page

    return render_template("sign_up.html", user=current_user)