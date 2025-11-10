from datetime import datetime
from models import db

class EmotionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    emotion = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    detection_type = db.Column(db.String(20), nullable=False)  # 'face', 'text', or 'audio'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EmotionLog {self.emotion} at {self.timestamp}>'
