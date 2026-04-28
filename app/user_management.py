from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

PARTICIPANTS = [
    "Dave", "Lou", "Paul", "Katie", "Aaron", "Nicki", "Paige", 
    "Isla", "Willow", "Neil", "Rebecca", "Max", "Neve", 
    "Craig", "Elaine", "Mark", "Gwen"
]

def init_users():
    """Seeds the database with the family members if they don't exist."""
    # Note: 'Isla' was listed twice in GEMINI.md, but we treat usernames as unique.
    # If there are two Islas, they would need distinct identifiers (e.g., Isla M and Isla S).
    for name in PARTICIPANTS:
        user = User.query.filter_by(username=name).first()
        if not user:
            # Default PIN is '0000' - users should change this on first login
            # We use hashing for security even in a simple family app
            hashed_pin = generate_password_hash("0000")
            new_user = User(username=name, pin=hashed_pin)
            db.session.add(new_user)
    
    # Set Dave as admin by default
    dave = User.query.filter_by(username="Dave").first()
    if dave:
        dave.is_admin = True
        
    db.session.commit()

def authenticate_user(username, pin):
    """Verifies a user's PIN."""
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.pin, pin):
        return user
    return None

def update_user_pin(user_id, new_pin):
    """Updates a user's PIN."""
    user = User.query.get(user_id)
    if user:
        user.pin = generate_password_hash(new_pin)
        db.session.commit()
        return True
    return False

def get_all_usernames():
    """Returns a list of all usernames for the login dropdown."""
    return [u.username for u in User.query.order_by(User.username).all()]
