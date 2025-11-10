# Pysra - Emotion Recognition System

A Flask-based web application for multi-modal emotion recognition using face, text, and audio inputs.

## Features

- **Face Emotion Detection**: Upload images for facial emotion analysis
- **Text Emotion Analysis**: Analyze emotional content in text
- **Audio Emotion Recognition**: Process audio files for emotion detection
- **User Authentication**: Secure login/registration system
- **Dashboard**: View emotion history and statistics
- **Motivational Messages**: Get personalized motivation based on detected emotions
- **Games**: Games that boost user's emotion by playing

## Project Structure

```
Pysra/
├── datasets/
│   ├── emotion.csv          # Audio emotion dataset
│   ├── fer2013.csv         # Facial emotion dataset
│   └── text.csv            # Text emotion dataset
├── ml/
│   ├── __init__.py
│   ├── predict.py          # Emotion prediction logic
│   ├── train_audio.py      # Audio model training
│   ├── train_face.py       # Face model training
│   └── train_text.py       # Text model training
├── models/
│   ├── __init__.py
│   ├── emotion_log.py      # Database model for emotion logs
│   └── user.py             # Database model for users
├── static/
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── games.css
│   │   └── style.css
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── games.js
│   │   ├── heatmap.js
│   │   └── main.js
│   ├── models/
│   │   └── face_emotion_model.h5  # Pre-trained face emotion model
│   └── uploads/            # User uploaded files
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── detect.html
│   ├── games.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   └── register.html
├── utils/
│   ├── __init__.py
│   └── motivation.py       # Motivational message generator
├── app.py                  # Main Flask application
├── config.py               # Application configuration
└── requirements.txt        # Python dependencies
```

## Datasets

### 1. FER2013 Dataset (`fer2013.csv`)
- **Purpose**: Facial emotion recognition training
- **Format**: CSV with pixel values and emotion labels
- **Emotions**: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
- Download: https://www.kaggle.com/datasets/genadieva/fer-2013-csv-dataset

### 2. Emotion Dataset (`emotion.csv`)
- **Purpose**: Audio emotion recognition training
- **Format**: CSV with audio features and emotion labels
- **Features**: MFCC, spectral features, prosodic features
- Download: https://www.kaggle.com/datasets/mostafaabdlhamed/speech-signal-features
  
### 3. Text Dataset (`text.csv`)
- **Purpose**: Text emotion analysis training
- **Format**: CSV with text samples and emotion labels
- **Content**: Social media posts, reviews, comments
- Download: https://www.kaggle.com/datasets/adhamelkomy/twitter-emotion-dataset

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Pysra
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Install the Datasets**
- Download the datasets from Kaggle
- Place `fer2013.csv` in the `datasets/` directory
- Place `emotion.csv` in the `datasets/` directory
- Place `text.csv` in the `datasets/` directory

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Emotion Detection**: 
   - Upload an image for face emotion detection
   - Enter text for sentiment analysis
   - Upload audio file for voice emotion recognition
3. **View Results**: See detected emotions with confidence scores
4. **Dashboard**: Track your emotion history and patterns
5. **Games**: Access emotion-based interactive games

## Dependencies

- Flask - Web framework
- TensorFlow/Keras - Deep learning models
- OpenCV - Image processing
- librosa - Audio processing
- scikit-learn - Machine learning utilities
- pandas - Data manipulation
- numpy - Numerical computing

## API Endpoints

- `GET /` - Home page
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /detect` - Emotion detection interface
- `POST /detect` - Process emotion detection
- `GET /dashboard` - User dashboard
- `GET /history` - Emotion history
- `GET /api/emotion-data` - Emotion data API

## Model Information

- **Face Model**: CNN trained on FER2013 dataset
- **Text Model**: NLP model for sentiment classification
- **Audio Model**: Feature-based classifier using MFCC and spectral features

## License

This project is licensed under the MIT License.
