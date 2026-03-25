from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

#create database object Globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'aqi.db')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['AQI_API_KEY'] = 'your-aqi-api-key'  # Configuration for AQI API Key 

    #AB DATABSE DB ko app se connect karenge
    db.init_app(app)
    #Ab Blueprint ko import karkle register karenge
    from app.routes.auth import auth_bp
    from app.routes.prediction import prediction_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.realtime import realtime_bp
    from app.routes.pages import pages_bp




    #Ab register_blueprint ko call karke teeno ko pass kar denge 
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(realtime_bp)
    app.register_blueprint(pages_bp)



    

    #Ab app ko finally return kr denge
    return app