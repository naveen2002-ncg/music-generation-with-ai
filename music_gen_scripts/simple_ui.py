import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Path to scripts and MIDI file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
GENERATE_SCRIPT = os.path.join(SCRIPT_DIR, 'generate_music_pytorch.py')
MIDI_FILE = os.path.join(PROJECT_ROOT, 'generated_music.mid')

# Color scheme
BG_COLOR = '#232946'
BTN_COLOR = '#eebbc3'
BTN_TEXT_COLOR = '#232946'
TITLE_COLOR = '#eebbc3'
STATUS_COLOR = '#fffffe'

# Function to generate music
def generate_music():
    status_var.set('Generating music...')
    root.update_idletasks()
    try:
        result = subprocess.run([sys.executable, GENERATE_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            status_var.set('Music generated successfully!')
            messagebox.showinfo('Success', 'Music generated successfully!')
        else:
            status_var.set('Error generating music.')
            messagebox.showerror('Error', f'Error generating music:\n{result.stderr}')
    except Exception as e:
        status_var.set('Error generating music.')
        messagebox.showerror('Error', f'Exception: {e}')

# Function to play MIDI file
def play_midi():
    if not os.path.exists(MIDI_FILE):
        status_var.set('No generated MIDI file found!')
        messagebox.showerror('Error', 'No generated MIDI file found!')
        return
    status_var.set('Playing music...')
    root.update_idletasks()
    try:
        if sys.platform.startswith('win'):
            os.startfile(MIDI_FILE)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', MIDI_FILE])
        else:
            subprocess.run(['xdg-open', MIDI_FILE])
        status_var.set('Playing music!')
    except Exception as e:
        status_var.set('Could not play MIDI file.')
        messagebox.showerror('Error', f'Could not play MIDI file: {e}')

# Build the UI
root = tk.Tk()
root.title('AI Music Generator')
root.geometry('350x220')
root.configure(bg=BG_COLOR)

# Title label
title_label = tk.Label(root, text='AI Music Generator', font=('Arial Rounded MT Bold', 20), fg=TITLE_COLOR, bg=BG_COLOR)
title_label.pack(pady=(18, 8))

# Generate button
btn_generate = tk.Button(root, text='Generate Music', command=generate_music, width=20, height=2,
                        bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=('Arial', 12, 'bold'), bd=0, activebackground='#f6caca')
btn_generate.pack(pady=8)

# Play button
btn_play = tk.Button(root, text='Play Music', command=play_midi, width=20, height=2,
                    bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=('Arial', 12, 'bold'), bd=0, activebackground='#f6caca')
btn_play.pack(pady=8)

# Status label
status_var = tk.StringVar()
status_var.set('Ready.')
status_label = tk.Label(root, textvariable=status_var, font=('Arial', 11), fg=STATUS_COLOR, bg=BG_COLOR)
status_label.pack(pady=(10, 0))

root.mainloop() 