import numpy as np
import pickle
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, random_split
from build_lstm_model_pytorch import MusicLSTM

print('Starting training script...')

# Hyperparameters
BATCH_SIZE = 32  # Reduced batch size for better feedback
EPOCHS = 10
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.1

# Load data
with np.load('../training_data.npz') as data:
    inputs = data['inputs']
    targets = data['targets']

# Use a smaller dataset for quick test
max_samples = 10000
inputs = inputs[:max_samples]
targets = targets[:max_samples]

inputs = torch.tensor(inputs, dtype=torch.long)
targets = torch.tensor(targets, dtype=torch.long)

dataset = TensorDataset(inputs, targets)
val_size = int(len(dataset) * VALIDATION_SPLIT)
train_size = len(dataset) - val_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# Load vocab size
with open('../vocab.pkl', 'rb') as f:
    vocab_data = pickle.load(f)
    vocab_size = len(vocab_data['vocab'])

# Model, loss, optimizer
model = MusicLSTM(vocab_size)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training loop
for epoch in range(1, EPOCHS + 1):
    model.train()
    train_loss = 0
    for batch_idx, (x_batch, y_batch) in enumerate(train_loader):
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(x_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * x_batch.size(0)
        if (batch_idx + 1) % 10 == 0 or (batch_idx + 1) == len(train_loader):
            print(f"Epoch {epoch} Batch {batch_idx+1}/{len(train_loader)} - Loss: {loss.item():.4f}")
    train_loss /= len(train_loader.dataset)

    # Validation
    model.eval()
    val_loss = 0
    correct = 0
    total = 0
    with torch.no_grad():
        for x_batch, y_batch in val_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            val_loss += loss.item() * x_batch.size(0)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == y_batch).sum().item()
            total += y_batch.size(0)
    val_loss /= len(val_loader.dataset)
    val_acc = correct / total

    print(f"Epoch {epoch}/{EPOCHS} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f} - Val Acc: {val_acc:.4f}")

# Save the trained model
torch.save(model.state_dict(), 'music_lstm_pytorch.pth')
print('Training complete. Model saved to music_lstm_pytorch.pth') 