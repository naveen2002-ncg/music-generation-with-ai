import numpy as np
import pickle
import torch
from build_lstm_model_pytorch import MusicLSTM
import pretty_midi

# Load vocab and model parameters
with open('../vocab.pkl', 'rb') as f:
    vocab_data = pickle.load(f)
    vocab = vocab_data['vocab']
    token_to_int = vocab_data['token_to_int']
    int_to_token = vocab_data['int_to_token']
    vocab_size = len(vocab)

SEQUENCE_LENGTH = 30

# Load the trained model
model = MusicLSTM(vocab_size)
model.load_state_dict(torch.load('../music_lstm_pytorch.pth', map_location=torch.device('cpu')))
model.eval()

print('Model and vocabulary loaded. Ready for music generation.')

# Load a seed sequence from training data
with np.load('../training_data.npz') as data:
    inputs = data['inputs']

# Randomly select a seed
seed_idx = np.random.randint(0, len(inputs))
seed_seq = inputs[seed_idx]

print('Seed sequence selected. Ready to generate music.')

# Parameters for generation
GENERATE_LENGTH = 100  # Number of notes to generate

generated = list(seed_seq)

for _ in range(GENERATE_LENGTH):
    input_seq = torch.tensor([generated[-SEQUENCE_LENGTH:]], dtype=torch.long)
    with torch.no_grad():
        output = model(input_seq)
        probabilities = torch.softmax(output[0], dim=0).cpu().numpy()
        next_token_idx = np.random.choice(len(probabilities), p=probabilities)
    generated.append(next_token_idx)

print(f'Generated {GENERATE_LENGTH} new notes.')

try:
    # Convert generated indices to (pitch, duration, velocity) tuples
    note_tuples = [int_to_token[idx] for idx in generated]
    print(f'Converted {len(note_tuples)} tokens to note tuples.')

    # Create a PrettyMIDI object and an instrument
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano

    # Start time for the first note
    current_time = 0.0
    for i, (pitch, duration, velocity) in enumerate(note_tuples):
        try:
            note = pretty_midi.Note(
                velocity=int(velocity),
                pitch=int(pitch),
                start=current_time,
                end=current_time + float(duration)
            )
            instrument.notes.append(note)
            current_time += float(duration)
        except Exception as e:
            print(f'Error creating note at index {i}: {e}')

    midi.instruments.append(instrument)
    output_file = 'generated_music.mid'
    midi.write(output_file)
    print(f'Generated music saved to {output_file}')
except Exception as e:
    print(f'Error during MIDI generation/export: {e}') 