from flask_login import UserMixin
from datetime import datetime
from models import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with emotion logs
    emotion_logs = db.relationship('EmotionLog', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
