import numpy as np
import cv2
from tensorflow import keras
import pickle
import librosa
import os

# Emotion labels
EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def predict_emotion(input_data, model_type):
    '''
    Unified prediction function for all modalities

    Args:
        input_data: File path for face/audio, text string for text
        model_type: 'face', 'text', or 'audio'

    Returns:
        emotion (str), confidence (float)
    '''

    if model_type == 'face':
        return predict_face_emotion(input_data)
    elif model_type == 'text':
        return predict_text_emotion(input_data)
    elif model_type == 'audio':
        return predict_audio_emotion(input_data)
    else:
        return 'Unknown', 0.0

def predict_face_emotion(image_path):
    '''
    Predict emotion from face image
    '''
    try:
        # Load model
        model = keras.models.load_model('static/models/face_emotion_model.h5')

        # Load and preprocess image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Detect face
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)

        if len(faces) == 0:
            # If no face detected, use whole image
            face = img
        else:
            x, y, w, h = faces[0]
            face = img[y:y+h, x:x+w]

        # Resize and normalize
        face = cv2.resize(face, (48, 48))
        face = face / 255.0
        face = face.reshape(1, 48, 48, 1)

        # Predict
        predictions = model.predict(face, verbose=0)
        emotion_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][emotion_idx])

        emotion = EMOTION_LABELS[emotion_idx]

        return emotion, confidence

    except Exception as e:
        print(f"Error in face prediction: {e}")
        return 'Neutral', 0.5

def predict_text_emotion(text):
    '''
    Predict emotion from text
    '''
    try:
        # Load model and preprocessors
        model = keras.models.load_model('static/models/text_emotion_model.h5')

        with open('static/models/text_tokenizer.pkl', 'rb') as f:
            tokenizer = pickle.load(f)
        with open('static/models/text_label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)

        # Preprocess text
        from keras.preprocessing.sequence import pad_sequences
        sequence = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequence, maxlen=100, padding='post', truncating='post')

        # Predict
        predictions = model.predict(padded, verbose=0)
        emotion_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][emotion_idx])

        emotion = le.inverse_transform([emotion_idx])[0]

        # Map to standard emotion labels if needed
        emotion_mapping = {
            'happy': 'Happy',
            'sad': 'Sad',
            'anger': 'Angry',
            'fear': 'Fear',
            'surprise': 'Surprise',
            'neutral': 'Neutral'
        }
        emotion = emotion_mapping.get(emotion.lower(), emotion.capitalize())

        return emotion, confidence

    except Exception as e:
        print(f"Error in text prediction: {e}")
        return 'Neutral', 0.5

def predict_audio_emotion(audio_path):
    '''
    Predict emotion from audio file
    '''
    try:
        # Load model and label encoder
        model = keras.models.load_model('static/models/audio_emotion_model.h5')

        with open('static/models/audio_label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)

        # Extract features
        audio, sr = librosa.load(audio_path, duration=3, sr=22050)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        mfcc_processed = mfcc_processed.reshape(1, -1)

        # Predict
        predictions = model.predict(mfcc_processed, verbose=0)
        emotion_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][emotion_idx])

        emotion = le.inverse_transform([emotion_idx])[0]

        # Map to standard emotion labels if needed
        emotion_mapping = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'fear': 'Fear',
            'surprise': 'Surprise',
            'neutral': 'Neutral'
        }
        emotion = emotion_mapping.get(emotion.lower(), emotion.capitalize())

        return emotion, confidence

    except Exception as e:
        print(f"Error in audio prediction: {e}")
        return 'Neutral', 0.5
