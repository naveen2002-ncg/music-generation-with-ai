import pickle
import numpy as np
from collections import Counter

SEQUENCE_LENGTH = 30  # Number of notes in input sequence
DURATION_RESOLUTION = 0.05  # Quantize durations to nearest 0.05 seconds

# Load preprocessed note sequences
with open('piano_note_sequences.pkl', 'rb') as f:
    note_sequences = pickle.load(f)

# Helper: quantize duration
def quantize(x, resolution):
    return round(x / resolution) * resolution

# Build list of all (pitch, duration, velocity) tuples
tokens = []
processed_sequences = []
for seq in note_sequences:
    processed_seq = []
    for note in seq:
        pitch = note[0]
        duration = quantize(note[2] - note[1], DURATION_RESOLUTION)
        velocity = note[3]
        token = (pitch, duration, velocity)
        tokens.append(token)
        processed_seq.append(token)
    processed_sequences.append(processed_seq)

# Build vocabulary
counter = Counter(tokens)
vocab = sorted(counter.keys())
token_to_int = {token: i for i, token in enumerate(vocab)}
int_to_token = {i: token for i, token in enumerate(vocab)}

print(f'Vocabulary size: {len(vocab)}')

# Prepare input/output pairs
inputs = []
targets = []
for seq in processed_sequences:
    if len(seq) > SEQUENCE_LENGTH:
        for i in range(len(seq) - SEQUENCE_LENGTH):
            input_seq = seq[i:i+SEQUENCE_LENGTH]
            target = seq[i+SEQUENCE_LENGTH]
            inputs.append([token_to_int[token] for token in input_seq])
            targets.append(token_to_int[target])

inputs = np.array(inputs)
targets = np.array(targets)

print(f'Prepared {inputs.shape[0]} input/output pairs.')

# Save for model training
with open('training_data.npz', 'wb') as f:
    np.savez(f, inputs=inputs, targets=targets)
with open('vocab.pkl', 'wb') as f:
    pickle.dump({'vocab': vocab, 'token_to_int': token_to_int, 'int_to_token': int_to_token}, f)

print('Saved training data and vocabulary.') 