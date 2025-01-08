import random
import torch
from torch.utils.data import DataLoader

def sample_hyperparameters(param_space):
    """
    Randomly samples hyperparameters from the provided parameter space.
    
    Args:
        param_space (dict): Dictionary of hyperparameter options.
        
    Returns:
        dict: A randomly sampled hyperparameter configuration.
    """
    return {
        'hidden_layers': random.choice(param_space['hidden_layers']),
        'dropout_rate': random.choice(param_space['dropout_rate']),
        'learning_rate': random.choice(param_space['learning_rate']),
        'batch_size': random.choice(param_space['batch_size']),
    }

def train_and_evaluate(params, model_class, input_dim, train_dataset, validate_dataset, criterion, num_epochs=10):
    """
    Trains and evaluates a model with the given hyperparameters.
    
    Args:
        params (dict): Hyperparameter configuration.
        model_class (class): Model class to instantiate.
        input_dim (int): Number of input features.
        train_dataset (Dataset): PyTorch Dataset for training.
        val_dataset (Dataset): PyTorch Dataset for validation.
        criterion (Loss): Loss function for optimization.
        num_epochs (int): Number of training epochs.

    Returns:
        float: Best validation loss achieved.
        dict: The hyperparameter configuration.
    """
    print(f"Testing configuration: {params}")
    
    hidden_layers = params['hidden_layers']
    dropout_rate = params['dropout_rate']
    learning_rate = params['learning_rate']
    batch_size = params['batch_size']
    
    model = model_class(input_dim=input_dim, hidden_layers=hidden_layers, dropout_rate=dropout_rate)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    validate_loader = DataLoader(validate_dataset, batch_size=batch_size)
    
    best_validate_loss = float('inf')
    for epoch in range(num_epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            predictions = model(X_batch)
            loss = criterion(predictions, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        model.eval()
        validate_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in validate_loader:
                predictions = model(X_batch)
                loss = criterion(predictions, y_batch)
                validate_loss += loss.item()
        validate_loss /= len(validate_loader)
        
        if validate_loss < best_validate_loss:
            best_validate_loss = validate_loss

    print(f"Validation Loss: {best_validate_loss:.4f}")
    return best_validate_loss, params