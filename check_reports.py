# bus report check karne ke liye temporary file hai ye
from app import create_app, db #importing the create_app function and db instance from app package(app/__init__.py-->app factory)
from app.models import reportRequest #importing the database models to create tables

#Flask app create/Instance
app = create_app() #creating the flask app instance by calling the create_app function

# Check all reports in the database
with app.app_context(): #app context is required to access the app's resources like database    
    requests = reportRequest.query.all() #fetching all report entries from the database
    for req in requests:
        print(
            f"Request ID: {req.id}, "
            f"Name: {req.name}, "
            f"Email: {req.email}, "
            f"Organization: {req.organization}, "
            f"Report ID: {req.report_id}, "
            f"Requested At: {req.requested_at}"
        )


        # Report check karne ke liye terminal me ye command run karein:
        # python check_reports.py   