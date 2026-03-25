from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.models import Prediction


#create a blueprint object
dashboard_bp = Blueprint('dashboard', __name__)
#dashboard-->name of the bp,  __name__ --> name of the module

@dashboard_bp.route('/dashboard')
def dashboard():
    #ager user loggedin nhi ho
    if 'user_id' not in session:
        flash("Please login first", "warning")
        return redirect(url_for('auth.login'))
   
    return render_template('dashboard.html')
