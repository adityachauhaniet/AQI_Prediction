import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash #importing password hashing function
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm




#Ek blueprint object create ker lete hain
auth_bp = Blueprint('auth', __name__)

#-------------------------------------------REGISTER ROUTE----------------------------
@auth_bp.route('/register', methods=["POST", "GET"])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit(): #Esme method==POST + validation okk both are include
        # Check if user/email exists
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken!", 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered!", "danger")
            return render_template('register.html', form=form)
        
        # Password Hash kar lete hain, jisase duplicate password creation avoid kr sken
        hashed_pw = generate_password_hash(form.password.data)
        #naya User Object create karte hain
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit() # PostgreSQL mein commit karna zaroori hai table save karne ke liye

        flash("Registration successful 🎉, Please login!", 'success')
        return redirect(url_for('auth.login'))
    #GET Request ya validation error ker liye
    return render_template('register.html', form=form)



#----------------------LOGIN ROUTE-----------------------------
@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    
    form = LoginForm() #login form ko inherate kr lete hain
    if form.validate_on_submit():
        identifier = form.email_or_username.data #username or email dono se login ho jayega
        
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first() #email ya username dono se login ho jayega

        if user and check_password_hash(user.password, form.password.data): #Uaser ka password aur hashed password match hone chahiye
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful 🎉", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html', form=form) #ager, match nhi hua to phir se login page pe bhej do
 


#-----------------------------------------------LOGOUT ROUTE--------------------------
@auth_bp.route('/logout')
def logout():
    session.clear() # Poora session clear karna zyada safe hai
    flash("You have been logged out!", 'info')
     #Ab esko phir se login page pe bhej dete hain
    return redirect(url_for('auth.login')) #WHY auth.login--> b/c login route is in auth blueprint






# Check users
# @auth_bp.route('/check-users')
# def check_users():
#     from app.models import User
#     users = User.query.all()
#     return str(users)


# @auth_bp.route('/init-db')
# def init_db():
#     from app import db
#     db.create_all()
#     return "DB Created!"