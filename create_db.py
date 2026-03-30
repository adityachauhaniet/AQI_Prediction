# DATABASE TABLE CREATE KARNA (ONE-TIME)
from app import create_app, db #importing the create_app function and db instance from app package(app/__init__.py-->app
from app.models import User, Prediction, reportRequest, ContactMessage #importing the database models to create tables
#basically hum un tools ko import kr rhe hain jo hume flask app create krne


#Flask app create
app = create_app() #creating the flask app instance by calling the create_app function


#App context me jaake database tables create karenge
with app.app_context(): #app context is required to access the app's resources like database
    db.create_all() #creating all the database tables defined in the models.py file
    print("PostgreSQL Tables created successfully in 'aqi_db'!")


# Report table bnanke ke liye terminal me ye command run karein:
# python create_db.py
