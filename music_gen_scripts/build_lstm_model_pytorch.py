import numpy as np
import pickle
import torch
import torch.nn as nn

# Load training data
with np.load('../training_data.npz') as data:
    inputs = data['inputs']
    targets = data['targets']

with open('../vocab.pkl', 'rb') as f:
    vocab_data = pickle.load(f)
    vocab = vocab_data['vocab']
    vocab_size = len(vocab)

SEQUENCE_LENGTH = inputs.shape[1]

# Define the LSTM model in PyTorch
class MusicLSTM(nn.Module):
    def __init__(self, vocab_size, embed_size=128, lstm_size=256, num_layers=2):
        super(MusicLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, lstm_size, num_layers, batch_first=True)
        self.fc1 = nn.Linear(lstm_size, 256)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(256, vocab_size)
    def forward(self, x):
        x = self.embedding(x)
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # Take the output of the last time step
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        return out

model = MusicLSTM(vocab_size)
print(model)
print(f"Number of parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}") 