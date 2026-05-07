import os
from app import create_app, db
from app.models import User, Prediction
from app.prediction_management import save_prediction, get_user_predictions

def test_predictions():
    app = create_app()
    with app.app_context():
        # Clean up database for testing
        db.create_all()
        
        user = User.query.first()
        if not user:
            user = User(username='test_user', pin='1234')
            db.session.add(user)
            db.session.commit()
            
        print(f"Testing with user: {user.username} (ID: {user.id})")
        
        # Test Save
        test_data = {"winner": "Brazil", "runner_up": "France"}
        success, msg = save_prediction(user.id, "cat6", test_data)
        print(f"Save Prediction: success={success}, msg={msg}")
        
        # Test Retrieve
        preds = get_user_predictions(user.id)
        print(f"Retrieved Predictions: {preds}")
        
        if success and "cat6" in preds and preds["cat6"] == test_data:
            print("TEST PASSED: Predictions stored and retrieved correctly.")
        else:
            print("TEST FAILED.")

if __name__ == "__main__":
    test_predictions()
