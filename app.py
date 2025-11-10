from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize db instance from models package to avoid circular imports
from models import db
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization (within app context when needed)
from models.user import User
from models.emotion_log import EmotionLog
from utils.motivation import get_motivation_message
from ml.predict import predict_emotion

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('detect'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('detect'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('detect'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('detect'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'POST':
        detection_type = request.form.get('detection_type')

        if detection_type == 'face':
            if 'face_file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['face_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                emotion, confidence = predict_emotion(filepath, 'face')

                # Log emotion
                log = EmotionLog(
                    user_id=current_user.id,
                    emotion=emotion,
                    confidence=confidence,
                    detection_type='face'
                )
                db.session.add(log)
                db.session.commit()

                motivation = get_motivation_message(emotion)

                return jsonify({
                    'emotion': emotion,
                    'confidence': confidence,
                    'motivation': motivation
                })

        elif detection_type == 'text':
            text_input = request.form.get('text_input')
            if text_input:
                emotion, confidence = predict_emotion(text_input, 'text')

                log = EmotionLog(
                    user_id=current_user.id,
                    emotion=emotion,
                    confidence=confidence,
                    detection_type='text'
                )
                db.session.add(log)
                db.session.commit()

                motivation = get_motivation_message(emotion)

                return jsonify({
                    'emotion': emotion,
                    'confidence': confidence,
                    'motivation': motivation
                })

        elif detection_type == 'audio':
            if 'audio_file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['audio_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                emotion, confidence = predict_emotion(filepath, 'audio')

                log = EmotionLog(
                    user_id=current_user.id,
                    emotion=emotion,
                    confidence=confidence,
                    detection_type='audio'
                )
                db.session.add(log)
                db.session.commit()

                motivation = get_motivation_message(emotion)

                return jsonify({
                    'emotion': emotion,
                    'confidence': confidence,
                    'motivation': motivation
                })

    return render_template('detect.html')

@app.route('/dashboard')
@login_required
def dashboard():
    logs = EmotionLog.query.filter_by(user_id=current_user.id).order_by(EmotionLog.timestamp.desc()).all()
    return render_template('dashboard.html', logs=logs)

@app.route('/history')
@login_required
def history():
    logs = EmotionLog.query.filter_by(user_id=current_user.id).order_by(EmotionLog.timestamp.desc()).limit(100).all()
    return render_template('history.html', logs=logs)

@app.route('/games')
@login_required
def games():
    return render_template('games.html')

@app.route('/api/emotion-data')
@login_required
def get_emotion_data():
    logs = EmotionLog.query.filter_by(user_id=current_user.id).order_by(EmotionLog.timestamp).all()

    data = {
        'dates': [log.timestamp.strftime('%Y-%m-%d') for log in logs],
        'emotions': [log.emotion for log in logs],
        'confidences': [log.confidence for log in logs]
    }

    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
