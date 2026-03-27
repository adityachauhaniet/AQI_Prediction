from flask import flash

from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(225), nullable = False)

    role = db.Column(db.String(20), default="user")
    #values: "user" | "admin"

    prediction = db.relationship('Prediction', backref='user', lazy=True)
    profile_image = db.Column(db.String(200), default='default.png')


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    co= db.Column(db.Integer, nullable = False)
    ozone = db.Column(db.Float, nullable = False)
    no2 = db.Column(db.Float, nullable = False)
    pm25 = db.Column(db.Float, nullable = False)
    
    predicted_aqi = db.Column(db.Float, nullable = False)
    predicted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #Task creation timestamp column

    # Foriegn Key: Ye user ke Id ko point karega
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key = True) #for unique user id
    title = db.Column(db.String(200), nullable = False) #report title(UI pe show hoga)
    description = db.Column(db.Text, nullable = True) #report description(UI pe show hoga)
    year = db.Column(db.Integer, nullable = False) #report ka year
    file_name = db.Column(db.String(100), nullable = False) #report file name(jise download karenge) pdf file ka exact naam jo static/reports me hoga
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #Task creation timestamp column


# reportRequest model ko use karenge report entries ko database me store karne ke liye
class reportRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True) #for unique report id
    name = db.Column(db.String(100), nullable = False) #name of the person requesting the report
    email = db.Column(db.String(100), nullable = False) #email of the person
    organization = db.Column(db.String(150), nullable = True) #organization of the person

    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable = False) #foriegn key to link to the report being requested
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #timestamp
   

# ------------------------For Admin Contact Messages    -----------------------

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # NEW FEILED TO TRACK IF THE MESSAGE HAS BEEN READ BY ADMIN
    is_read = db.Column(db.Boolean, default=False)
