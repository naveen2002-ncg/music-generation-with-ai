import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load training data
with np.load('training_data.npz') as data:
    inputs = data['inputs']
    targets = data['targets']

with open('vocab.pkl', 'rb') as f:
    vocab_data = pickle.load(f)
    vocab = vocab_data['vocab']
    vocab_size = len(vocab)

SEQUENCE_LENGTH = inputs.shape[1]

# Define the model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=128, input_length=SEQUENCE_LENGTH),
    LSTM(256, return_sequences=True),
    LSTM(256),
    Dense(256, activation='relu'),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary() 