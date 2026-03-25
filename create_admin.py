from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

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
        print("Admin created!")
    else:
        print("Admin already exists")

    # Debug
    print(User.query.all())


    