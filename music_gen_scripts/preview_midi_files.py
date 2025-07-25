import os
import pretty_midi

# Path to the extracted dataset
root_dir = os.path.join('data', 'lmd_matched')

# Recursively find a few MIDI files
midi_files = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith('.mid') or file.lower().endswith('.midi'):
            midi_files.append(os.path.join(root, file))
        if len(midi_files) >= 5:
            break
    if len(midi_files) >= 5:
        break

print('Sample MIDI files:')
for f in midi_files:
    print(f)

# Load and print info about the first MIDI file
if midi_files:
    print('\nPreviewing first MIDI file:')
    midi = pretty_midi.PrettyMIDI(midi_files[0])
    print(f'Number of instruments: {len(midi.instruments)}')
    for i, inst in enumerate(midi.instruments):
        print(f'  Instrument {i}: Program={inst.program}, Name={pretty_midi.program_to_instrument_name(inst.program)}, Notes={len(inst.notes)}')
else:
    print('No MIDI files found.') 