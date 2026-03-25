from flask import Blueprint, render_template, redirect, session, flash, request, url_for
from app import db
from app.models import Prediction, User
from app.forms import PredictionForm # form pass kr rhe hain
import numpy as np
import os
import pickle

# ---------------- AQI Category Helper ----------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good(0–50): 🌱It’s a healthy environment with clean and fresh air — safe for everyone."
    elif aqi <= 100:
        return "Moderate(51–100): 😊 Air quality is acceptable; however, sensitive individuals may experience mild discomfort."
    elif aqi <= 200:
        return "Unhealthy for Sensitive Groups(101–200): ⚠️ Air may cause minor health effects for people with respiratory issues or heart conditions."
    elif aqi <= 300:
        return "Poor(201–300): 😷 Prolonged outdoor exposure may cause breathing discomfort and irritation."
    elif aqi <= 400:
        return "Very Poor(301–400): 🚫 Air quality is unhealthy; everyone may experience health effects, especially children and elders."
    else:
        return "Severe(>400): ☠️ Serious health risks — avoid outdoor activities and stay indoors as much as possible."


#ek blueprint object create karte hain Prediction ke liye
prediction_bp = Blueprint('prediction', __name__)
#prediction-->name of the bp,  __name__ --> name of the module

#ab ML Model ko load kr lete hain
# ------------------------------------------------ Load ML Model -----------------------------------
# MODEL_PATH = os.path.join("app", "ml", "aqi_model(1).pkl") #Relative path deploy pe fail ho jaata hai.


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "aqi_model.pkl")


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)



# ------------------------------------------------ Helper: check login -----------------------------
def get_current_user_id():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please Login first', 'warning')
        return None
    return user_id


#----------------------------------------route to display prediction of logged-in user ---------------------------
@prediction_bp.route('/')
def view_prediction():
    user_id = get_current_user_id()
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    #only for current user
    #fetch all predictions
    predictions = Prediction.query.filter_by(user_id = user_id).order_by(Prediction.predicted_at.desc()).all()

    latest_prediction = predictions[0] if predictions else None

    aqi_category = None #initialize variable
    if latest_prediction: #Ager koi prediction hai
        aqi_category = get_aqi_category(latest_prediction.predicted_aqi) #get category  
        latest_prediction.aqi_category = aqi_category #dynamically attribute add kr rhe hain
    
    #Create Form instance
    form = PredictionForm()


    return render_template('prediction.html',latest_prediction=latest_prediction, predictions = predictions, aqi_category=aqi_category, form = form)


#--------------------------------------------------route to create a new prediction ---------------------------------------
#Ye root POST request ke liye h (form submit)
@prediction_bp.route('/new_prediction', methods=["POST"])
def new_prediction():
    user_id = get_current_user_id()
    if 'user_id' not in session:
        flash('Please logon to create a new prediction', 'warning')
        return redirect( url_for('auth.login'))
    
    form = PredictionForm()
        
    #get AQI value of Gases
    # 1️⃣ Form data
    if form.validate_on_submit():
        co = float(request.form.get("co"))
        ozone = float(request.form.get("ozone"))
        no2 = float(request.form.get("no2"))
        pm25 = float(request.form.get("pm25"))

        #-----------------------------------------------------Ab Ml Model ke liye input prepare karenge--------------------------------------
        #Model 2d array expect karta h esliye 2d array bnayenge
        input_data = np.array([[co, ozone, no2, pm25]])

        #------------------------------------------------------Prediction-------------------------------------------------------------------
        #[0] esiliye b/c output array hota h
        predicted_aqi = model.predict(input_data)[0]

    #-----------------------------------------------------Ab prediction ko DB me save kr lete hain---------------------------------------
        new_prediction = Prediction(
            co=co,
            ozone=ozone,
            no2=no2,
            pm25=pm25,
            predicted_aqi=predicted_aqi,
            user_id=user_id
        )

        db.session.add(new_prediction)
        db.session.commit()

        #ab ye save ho chuka h
        flash("AQI Prediction Successful", "success")
        #ab esko phir se Prediction Page pe redirect kra dete hain
        return redirect(url_for("prediction.view_prediction"))
    

    flash("Error in form data, Please try again", "danger")
    return redirect(url_for("prediction.view_prediction"))


#-----------------------------------------------------------route to delete a prediction--------------------------------------------
#User apni ek prediction delete kar sake
@prediction_bp.route('/delete/<int:id>', methods=["POST"])
def delete_prediction(id):
    prediction = Prediction.query.get_or_404(id) #Prediction le rhe hain id ke through

    db.session.delete(prediction)
    db.session.commit()

    flash("Prediction deleted successfuly", "info")
    return redirect(url_for("prediction.view_prediction"))


#--------------------------------------------------route to clear all predictions of logged-in user---------------------------------------
#Logged-in user ki saari prediction ko clear ko clear karega
@prediction_bp.route("/clear")
def clear_prediction():
    #yha per hum user id se saari prediction deleet kr denge, to hume user_id chahiye
    user_id = get_current_user_id()
    if 'user_id' not in session:
        flash("Please login first to clear the predictions", "warning")
        return redirect(url_for("auth.login"))
    
    Prediction.query.filter_by(user_id = user_id).delete() #Us user ki sabhi prediction ko leke delete kar denge
    db.session.commit()

    flash("All prediction cleared", "danger")
    return redirect(url_for("prediction.view_prediction"))

