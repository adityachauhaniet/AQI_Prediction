from app import create_app # db importing the create_app function and db instance from app package(app/__init__.py-->app factory)
#basically hum un tools ko import kr rhe hain jo hume flask app create krne ke liye chahiye
# Database Migration / Creation
from app.models import reportRequest

app = create_app() #creating the flask app instance by calling the create_app function

#creating the database tables before the first request is handled by the app
# with app.app_context(): #app context is required to access the app's resources like database
#     db.create_all() #creating all the database tables defined in the models.py file
#ab humara flask app ready hai to run karne ke liye

if __name__ == '__main__': #agar ye script directly run ho rhi hai
    # Debug mode development ke liye on rakhein
    app.run(debug=True) #run the flask app in debug mode for development purpose

