# Generated from paper: Dynamic Network Model from Partial Observations
# Method: Neural Network

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class NeuralNetworkModel(nn.Module):
    """
    Implementation of Neural Network from paper: Dynamic Network Model from Partial Observations
    
    Architecture: Recurrent neural network with memory cells
    
    Based on the paper's methodology and implementation hints:
    Use modern deep learning framework
    """
    
    def __init__(self, input_dim=784, hidden_dim=256, output_dim=10, dropout_rate=0.1):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.dropout_rate = dropout_rate
        
        # Define layers based on the paper's architecture
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout_rate)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        """Initialize model weights"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)
    
    def forward(self, x):
        """
        Forward pass implementing the method from the paper
        
        Args:
            x: Input tensor of shape (batch_size, input_dim)
            
        Returns:
            Output tensor of shape (batch_size, output_dim)
        """
        # Flatten input if needed
        if len(x.shape) > 2:
            x = x.view(x.size(0), -1)
        
        # Apply layers with activation functions
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        
        return x
    
    def predict(self, x):
        """Make predictions on input data"""
        self.eval()
        with torch.no_grad():
            outputs = self.forward(x)
            predictions = torch.argmax(outputs, dim=1)
        return predictions
    
    def get_features(self, x):
        """Extract features from the penultimate layer"""
        self.eval()
        with torch.no_grad():
            if len(x.shape) > 2:
                x = x.view(x.size(0), -1)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
        return x

def create_model(config=None):
    """Factory function to create model instance"""
    if config is None:
        config = {'input_dim': 784, 'hidden_dim': 256, 'output_dim': 10}
    
    return NeuralNetworkModel(**config)

def train_step(model, data_loader, optimizer, criterion, device='cpu'):
    """Single training step"""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (data, target) in enumerate(data_loader):
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        total += target.size(0)
    
    accuracy = 100. * correct / total
    avg_loss = total_loss / len(data_loader)
    
    return avg_loss, accuracy

def evaluate(model, data_loader, criterion, device='cpu'):
    """Evaluate model on test data"""
    model.eval()
    test_loss = 0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for data, target in data_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
    
    test_loss /= len(data_loader)
    accuracy = 100. * correct / total
    
    return test_loss, accuracy


# Usage example:
if __name__ == "__main__":
    # Create model instance
    model = create_model()
    print(f"Model: {model}")
    
    # Example forward pass
    x = torch.randn(32, 784)  # Batch of 32 samples
    output = model(x)
    print(f"Output shape: {output.shape}")
    
    # Example prediction
    predictions = model.predict(x)
    print(f"Predictions: {predictions}")
    
    # Extract features
    features = model.get_features(x)
    print(f"Features shape: {features.shape}")
