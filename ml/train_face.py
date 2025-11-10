import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import cv2

def load_fer2013(csv_path):
    '''
    Load and preprocess FER2013 dataset
    Place your fer2013.csv in the datasets folder
    '''
    data = pd.read_csv(csv_path)

    pixels = data['pixels'].tolist()
    width, height = 48, 48
    faces = []

    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.asarray(face).reshape(width, height)
        face = face / 255.0  # Normalize
        faces.append(face.reshape(width, height, 1))

    faces = np.asarray(faces)
    emotions = pd.get_dummies(data['emotion']).values

    return faces, emotions

def create_face_model():
    '''
    Create CNN model for facial emotion recognition
    7 emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
    '''
    model = Sequential()

    # First conv block
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

    # Second conv block
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

    # Third conv block
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Dropout(0.25))

    # Fully connected layers
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))

    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def train_face_model(csv_path='datasets/fer2013.csv', epochs=50, batch_size=64):
    '''
    Train the facial emotion recognition model
    '''
    print("Loading FER2013 dataset...")
    X, y = load_fer2013(csv_path)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    # Data augmentation
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1
    )

    model = create_face_model()
    print(model.summary())

    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=batch_size),
        validation_data=(X_val, y_val),
        epochs=epochs,
        steps_per_epoch=len(X_train) // batch_size,
        verbose=1
    )

    # Save model
    model.save('static/models/face_emotion_model.h5')
    print("Model saved to static/models/face_emotion_model.h5")

    return history

if __name__ == '__main__':
    # Run this script to train the face emotion model
    # Make sure fer2013.csv is in the datasets folder
    train_face_model()
