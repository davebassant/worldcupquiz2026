import os
from app import create_app, db
from app.models import User

def add_player(username, pin="0000"):
    app = create_app()
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Error: User '{username}' already exists.")
            return

        # Create and add new user
        new_user = User(username=username, pin=pin)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            print(f"Successfully added player: {username}")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add player: {e}")

if __name__ == "__main__":
    add_player("Gaspar")
