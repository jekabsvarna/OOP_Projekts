from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/home_admin')
@login_required
def home_admin():
    if current_user.email == "admin@rtu.lv":  # Check if user is admin
        return render_template("home_admin.html", user=current_user)
    else:
        flash("You are not authorized to access this page.", category="error")
        return redirect(url_for("views.home"))  # Redirect to regular home
    
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