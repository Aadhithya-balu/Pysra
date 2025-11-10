import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Conv1D, MaxPooling1D, Flatten
from sklearn.model_selection import train_test_split
import librosa

def extract_audio_features(file_path):
    '''
    Extract MFCC features from audio file
    '''
    try:
        audio, sr = librosa.load(file_path, duration=3, sr=22050)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        return mfcc_processed
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def load_audio_data(csv_path):
    '''
    Load audio emotion dataset
    CSV should have columns: 'file_path', 'emotion'
    Audio files should be referenced in the CSV
    '''
    data = pd.read_csv(csv_path)

    features = []
    emotions = []

    for idx, row in data.iterrows():
        feature = extract_audio_features(row['file_path'])
        if feature is not None:
            features.append(feature)
            emotions.append(row['emotion'])

        if idx % 100 == 0:
            print(f"Processed {idx} files...")

    return np.array(features), np.array(emotions)

def create_audio_model(input_shape=(40,), num_classes=7):
    '''
    Create neural network for audio emotion recognition
    '''
    model = Sequential()

    model.add(Dense(256, activation='relu', input_shape=input_shape))
    model.add(Dropout(0.3))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def train_audio_model(csv_path='datasets/emotion.csv', epochs=50, batch_size=32):
    '''
    Train the audio emotion recognition model
    '''
    print("Loading audio dataset...")
    X, y = load_audio_data(csv_path)

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    model = create_audio_model(input_shape=(X.shape[1],), num_classes=len(le.classes_))
    print(model.summary())

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )

    # Save model and label encoder
    model.save('static/models/audio_emotion_model.h5')

    import pickle
    with open('static/models/audio_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    print("Model saved to static/models/audio_emotion_model.h5")

    return history

if __name__ == '__main__':
    # Run this script to train the audio emotion model
    # Make sure emotion.csv is in the datasets folder with file paths
    train_audio_model()
