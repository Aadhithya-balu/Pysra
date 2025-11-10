import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_text_data(csv_path):
    '''
    Load and preprocess text emotion dataset
    Expected columns: 'text', 'emotion'
    Place your text.csv in the datasets folder
    '''
    data = pd.read_csv(csv_path)

    texts = data['text'].values
    emotions = data['label'].values  # Column is named 'label' in the CSV

    return texts, emotions

def create_text_model(vocab_size=10000, max_length=100, num_classes=7):
    '''
    Create LSTM model for text emotion recognition
    '''
    model = Sequential()

    model.add(Embedding(vocab_size, 128, input_length=max_length))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(64)))
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

def train_text_model(csv_path='datasets/text.csv', epochs=30, batch_size=32):
    '''
    Train the text emotion recognition model
    '''
    print("Loading text dataset...")
    texts, emotions = load_text_data(csv_path)

    # Encode emotions
    le = LabelEncoder()
    emotions_encoded = le.fit_transform(emotions)

    # Tokenize texts
    tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')

    X_train, X_val, y_train, y_val = train_test_split(
        padded, emotions_encoded, test_size=0.2, random_state=42
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

    model = create_text_model(num_classes=len(le.classes_))
    print(model.summary())

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )

    # Save model and tokenizer
    model.save('static/models/text_emotion_model.h5')

    import pickle
    with open('static/models/text_tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    with open('static/models/text_label_encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    print("Model saved to static/models/text_emotion_model.h5")

    return history

if __name__ == '__main__':
    # Run this script to train the text emotion model
    # Make sure text.csv is in the datasets folder
    train_text_model()
