# Script to train model
# python -m data.train

import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.utils.data as data
import torch.optim as optim
from datetime import datetime
from pathlib import Path

from ..ml.network import Network
from ..ml.train import train_model, test_model
from ..ml.analyze import plot_loss, plot_accuracy, plot_confusion_matrix

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
from django.conf import settings  # noqa: E402


batch_size = 128
num_epochs = 100
learning_rate = 0.001


def read_dataset(path: str, batch_size: int) -> data.DataLoader:
    """
    Constructs a Pytorch `DataLoader` from a path to a dataset.

    Arguments:
        path: The path to read.
        batch_size: The batch size for the dataset.

    Returns:
        The Pytorch `DataLoader` for the dataset.
    """

    df = pd.read_pickle(path)

    x = np.array([np.array(i) for i in df['image'].to_numpy()])
    x = np.moveaxis(x, 3, 1)  # Reshape image channel ordering to what PyTorch expects
    y = np.array([1 if i is True else 0 for i in df['is_ai_generated'].to_numpy()])

    dataset = data.TensorDataset(torch.Tensor(x), torch.Tensor(y).type(torch.LongTensor))
    loader = data.DataLoader(dataset, batch_size)

    return loader


def main():
    MODEL_PATH = settings.MODELS_DIR + 'model-{}/'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))

    print('Loading dataset')
    train_loader = read_dataset(settings.TRAIN_SET_PATH, batch_size)
    test_loader = read_dataset(settings.TEST_SET_PATH, batch_size)

    print('Creating model')
    model = Network()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, weight_decay=0.005, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()

    # Move model to configured device
    if torch.cuda.is_available():
        model.cuda()

    print('Training model:')
    train_losses, train_accuracies, val_losses, val_accuracies = train_model(model, train_loader, test_loader, optimizer, loss_fn, num_epochs)

    print('Testing model:')
    tp, fp, tn, fn = test_model(model, test_loader)

    Path(MODEL_PATH).mkdir(parents=True, exist_ok=True)
    plot_loss(train_losses, val_losses, MODEL_PATH + 'loss_plot.png')
    plot_accuracy(train_accuracies, val_accuracies, MODEL_PATH + 'accuracy_plot.png')
    plot_confusion_matrix(tp, fp, tn, fn, MODEL_PATH + 'confusion_matrix.png')

    print('Saving model')
    torch.save(model.state_dict(), MODEL_PATH + settings.MODEL_NAME)


if __name__ == "__main__":
    main()
