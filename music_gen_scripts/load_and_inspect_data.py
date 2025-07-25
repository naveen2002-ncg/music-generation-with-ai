import pickle

with open('piano_note_sequences.pkl', 'rb') as f:
    note_sequences = pickle.load(f)

print(f'Total sequences loaded: {len(note_sequences)}')

# Show a sample sequence
if note_sequences:
    print('\nSample sequence (first 10 notes):')
    for note in note_sequences[0][:10]:
        print(f'Pitch: {note[0]}, Start: {note[1]:.2f}, End: {note[2]:.2f}, Velocity: {note[3]}')
else:
    print('No sequences found.') 