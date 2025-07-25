# AI Music Generation with Deep Learning

This project is an AI-powered music generation system that composes original pieces of music using deep learning techniques (LSTM/RNN). It leverages PyTorch and MIDI processing libraries to generate melodies and export them as MIDI files. A simple, colorful UI is included for easy music generation and playback.

## Features
- Generate original melodies using an LSTM neural network
- Train on the Lakh MIDI dataset or your own MIDI files
- Export generated music to MIDI format
- Simple, colorful Tkinter UI for music generation and playback
- Easily extensible for harmonies, different instruments, or styles

## Technologies Used
- Python 3
- PyTorch
- pretty_midi
- Tkinter (for UI)
- Lakh MIDI Dataset (LMD-matched subset)

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd music-generation-with-ai
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   pip install torch pretty_midi
   ```
4. **(Optional) Download and preprocess MIDI data:**
   - Download the Lakh MIDI dataset or use your own MIDI files.
   - Use the provided scripts to preprocess and prepare training data.

## Usage
1. **Train the model:**
   ```sh
   cd music_gen_scripts
   python train_lstm_model_pytorch.py
   ```
2. **Generate music:**
   ```sh
   python generate_music_pytorch.py
   ```
3. **Use the UI:**
   ```sh
   python simple_ui.py
   ```
   - Click "Generate Music" to create a new MIDI file.
   - Click "Play Music" to listen to the generated music.

## File Structure
- `music_gen_scripts/` — All main scripts and the UI
- `data/` — (Optional) MIDI dataset (excluded from repo)
- `venv/` — Python virtual environment (excluded from repo)
- `generated_music.mid` — Output MIDI file
- `.gitignore` — Excludes large and unnecessary files from GitHub

## Credits
- Lakh MIDI Dataset: https://colinraffel.com/projects/lmd/
- PyTorch: https://pytorch.org/
- pretty_midi: https://github.com/craffel/pretty-midi

## License
This project is for educational and research purposes. See `LICENSE` for details.
