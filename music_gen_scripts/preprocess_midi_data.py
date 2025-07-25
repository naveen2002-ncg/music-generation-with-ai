import os
import pretty_midi
import pickle

# Path to the extracted dataset
root_dir = os.path.join('data', 'lmd_matched')
output_file = 'piano_note_sequences.pkl'

# Helper: is this a piano instrument?
def is_piano(inst):
    # General MIDI program numbers for piano: 0-7
    return 0 <= inst.program <= 7

note_sequences = []

# Scan MIDI files (limit for demo, e.g., 1000 files)
count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith('.mid') or file.lower().endswith('.midi'):
            midi_path = os.path.join(root, file)
            try:
                midi = pretty_midi.PrettyMIDI(midi_path)
                # Find the first piano instrument
                piano_tracks = [inst for inst in midi.instruments if is_piano(inst) and not inst.is_drum]
                if piano_tracks:
                    notes = piano_tracks[0].notes
                    # Represent each note as (pitch, start, end, velocity)
                    seq = [(n.pitch, n.start, n.end, n.velocity) for n in notes]
                    if len(seq) > 0:
                        note_sequences.append(seq)
                        count += 1
            except Exception as e:
                print(f'Error processing {midi_path}: {e}')
            if count >= 1000:
                break
    if count >= 1000:
        break

# Save the note sequences
with open(output_file, 'wb') as f:
    pickle.dump(note_sequences, f)

print(f'Saved {len(note_sequences)} piano note sequences to {output_file}') 