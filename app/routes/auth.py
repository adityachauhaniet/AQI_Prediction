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
    #ager user already login h to usko direct prediction page pe bhej denge
    if 'user_id' in session:
        return redirect(url_for('prediction.view_prediction'))
    
    form = RegistrationForm()

    if form.validate_on_submit(): #Esme method==POST + validation okk both are include
        username = form.username.data
        email = form.email.data
        password = form.password.data

        #Check kar lete hain if username ya email already exist
        existing_user_by_username = User.query.filter_by(username=username).first()
        existing_user_by_email = User.query.filter_by(email=email).first()

        
        if existing_user_by_username:
            flash("Username already taken, choose another one!", 'danger')
            return render_template('register.html', form=form)
        
        if existing_user_by_email:
            flash("Email alredy registered, Please login!", "danger")
            return render_template('register.html', form=form)
        
        #Ab Password Hash kar lete hain, jisase duplicate password creation avoid kr sken
        hashed_password = generate_password_hash(password) #ye unique pass dega

        #naya User Object create karte hain
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registeration successful 🎉, Please login now!", 'success')
        return redirect(url_for('auth.login'))
    

    #GET Request ya validation error ker liye
    return render_template('register.html', form=form)



#----------------------LOGIN ROUTE-----------------------------
@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    #ager user already logged ihn h tb
    if 'user_id' in session:
        return redirect(url_for('prediction.view_prediction'))
    
    form = LoginForm() #login form ko inherate kr lete hain
    
    if form.validate_on_submit(): #method==POST + validation ook then
        identifier = form.email_or_username.data #username or email dono se login ho jayega
        password = form.password.data #form me se data read kr rhe hain

        print("Identifier:", identifier)

        #pahle email se search kr lete hain 
        user = User.query.filter_by(email=identifier).first()
        #Ager email se nhi mila to username se search kro
        if not user:
            user = User.query.filter_by(username=identifier).first()
        print("User found:", user)

        if user:
            print("Stored hash:", user.password)
            print("Entered password:", password)
            print("Match:", check_password_hash(user.password, password))
            

        if user and check_password_hash(user.password, password): #Uaser ka password aur hashed password match hone chahiye
            #yahan DB user ka (id+username) session me daal dete hain
            session['user_id'] = user.id
            session['username'] = user.username #optionl bus display ke liye
            session['role'] = user.role
            flash("Login successfull 🎉", "success")
            return redirect(url_for('dashboard.dashboard'))
            
        else:
            flash("Invalid email/username or password", "danger")

    return render_template('login.html', form=form) #ager, match nhi hua to phir se login page pe bhej do



@auth_bp.route('/create-admin')
def create_admin():
    from app import db
    from app.models import User
    from werkzeug.security import generate_password_hash

    try:
        db.create_all()
        existing = User.query.filter_by(email="adityachauhanietlko22@gmail.com").first()

        if not existing:
            admin = User(
                username="admin",
                email="adityachauhanietlko22@gmail.com",
                password=generate_password_hash("Admin123@"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            return "Admin created!"

        return "Admin already exists"

    except Exception as e:
        return str(e)   # 🔥 IMPORTANT (error दिखेगा)



#-----------------------------------------------LOGOUT ROUTE--------------------------
@auth_bp.route('/logout')
def logout():
    #remove the user form the session for log them out
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user', None)
    
    flash("You have been logged out!", 'info')
    #Ab esko phir se login page pe bhej dete hain
    return redirect(url_for('auth.login')) #WHY auth.login--> b/c login route is in auth blueprint








# Check users
@auth_bp.route('/check-users')
def check_users():
    from app.models import User
    users = User.query.all()
    return str(users)