from app import create_app, db #importing the create_app function and db instance from app package(app/__init__.py-->app factory)
from app.models import Report #importing the database models to create tables
#basically hum un tools ko import kr rhe hain jo hume flask app create krne ke liye chahiye


#Flask app create/Instance
app = create_app() #creating the flask app instance by calling the create_app function

with app.app_context(): #app context is required to access the app's resources like database
# New report obkect create kr rahe hain
    report = Report(
        title = "World Air Quality Report ",
        description = "Comprehensive analysis of global air quality trends and statistics for the year 2024.",
        year = 2024,
        file_name = "world_air_quality_report_2024.pdf"
    )

    #DB session me jaake new report add karenge aur commit karenge
    db.session.add(report) #adding the new report object to the database session
    db.session.commit() #committing the session to save the report in the database

    print("Report entry added successfully to the database.")


    # Report entry add karne ke liye terminal me ye command run karein:
    # python insert_report.py

    # Ab report database me save ho chuki hai
    # ✔️ Tum is file ko delete bhi kar sakte ho (one-time use)