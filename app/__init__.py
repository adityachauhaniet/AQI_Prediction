from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv # .env file load karne ke liye

# .env file se variables load karte hain
load_dotenv()

# Database object globally create kiya
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-123')

    # Database URL Logic for PostgreSQL
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Render/Heroku fix: PostgreSQL ka prefix 'postgresql://' hona chahiye
        if database_url.startswith("postgres://"):
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("postgres://", "postgresql://", 1)
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Agar koi URL nahi mila toh fallback to SQLite (Dev purposes)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'aqi.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['AQI_API_KEY'] = os.environ.get('AQI_API_KEY')
        
    os.makedirs(app.instance_path, exist_ok=True)

    # DB ko app se connect karte hain
    db.init_app(app)

    # Blueprints ko function ke andar import karte hain (Circular Import se bachne ke liye)
    from app.routes.auth import auth_bp
    from app.routes.prediction import prediction_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.realtime import realtime_bp
    from app.routes.pages import pages_bp

    # Blueprints Register karna
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(realtime_bp)
    app.register_blueprint(pages_bp)

    return app