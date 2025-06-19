from werkzeug.security import generate_password_hash
from backend.app import app
from backend.models import ClientUser, db
import sys

with app.app_context():
    username = input("Enter the username for the new user: ")
    password = input("Enter the password for the new user: ")
    hashed_password = generate_password_hash(password)
    user = ClientUser(
        username=username,
        password=hashed_password,
        status=True,
        created_at=db.func.now(),
    )
    user.description = "Created"
    db.session.add(user)
    db.session.commit()
    print(f"User {username} created successfully.")
