from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Pehle check karo admin pehle se hai ya nahi
    admin_email = "adityachauhanietlko22@gmail.com"
    existing = User.query.filter_by(email=admin_email).first()

    if not existing:
        admin = User(
            username="admin",
            email=admin_email,
            password=generate_password_hash("Admin123@"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin already exists in database.")