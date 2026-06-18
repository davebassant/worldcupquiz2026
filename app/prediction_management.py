from datetime import datetime
from .models import db, Prediction, User
from .constants import DEADLINE

def is_deadline_passed():
    """Checks if the tournament has started."""
    return datetime.utcnow() > DEADLINE

def get_user_predictions(user_id):
    """Retrieves all predictions for a specific user."""
    preds = Prediction.query.filter_by(user_id=user_id).all()
    # Convert to a dictionary keyed by category for easier template access
    return {p.category: p.prediction_data for p in preds}

def get_all_user_predictions():
    """Retrieves all predictions for all users."""
    all_users = User.query.all()
    all_predictions = []

    for user in all_users:
        user_preds = get_user_predictions(user.id)
        # Ensure all categories exist in the dict to prevent template errors
        # This mirrors the logic in the predictions route
        for cat in ['cat1', 'cat2', 'cat4', 'cat6']:
            if cat not in user_preds:
                user_preds[cat] = {}
        for cat in ['cat3', 'cat5']:
            if cat not in user_preds:
                user_preds[cat] = []
        
        all_predictions.append({
            'username': user.username,
            'predictions': user_preds
        })
    return all_predictions

def save_prediction(user_id, category, data):
    """Saves or updates a prediction for a specific category."""
    if is_deadline_passed():
        return False, "Deadline has passed. Predictions can no longer be edited."
    
    prediction = Prediction.query.filter_by(user_id=user_id, category=category).first()
    
    if prediction:
        prediction.prediction_data = data
    else:
        prediction = Prediction(user_id=user_id, category=category, prediction_data=data)
        db.session.add(prediction)
    
    db.session.commit()
    return True, "Prediction saved successfully."

def get_all_teams():
    """Returns a flattened list of all teams in the tournament for general picks."""
    from .constants import GROUPS
    teams = []
    for group_teams in GROUPS.values():
        teams.extend(group_teams)
    return sorted(list(set(teams)))
