from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    prediction_data = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Prediction {self.user_id} - {self.category}>'
