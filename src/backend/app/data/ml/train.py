import torch
import torch.utils.data as data


def train_model(model, train_loader: data.DataLoader, val_loader: data.DataLoader, optimizer, loss_fn, num_epochs: int) -> tuple[list[float], list[float]]:
    """
    Trains the model with the given data and hyperparameters.
    Keeps the best-performing epoch (not the last epoch).

    Arguments:
        model: The model to train.
        train_loader: The train data.
        val_loader: The validation data.
        optimizer: The optimizer to use.
        loss_fn: The loss function to use.
        num_epochs: The number of epochs to train for.

    Returns:
        The list of train losses, train accuracies, validation losses and validation accuracies over the epochs.
    """

    no_improvement_patience = 10

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    no_improvement = 0  # Counter for number of consecutive epochs with no improvement
    best_epoch = None  # Epoch with best validation loss
    best_model_state = None  # Model state for best epoch

    for epoch in range(num_epochs):
        # Train model
        model.train()
        correct = 0
        total = 0

        for _, (x, y) in enumerate(train_loader):  # Load training data in batches
            # Move tensors to configured device
            x = x.to(device)
            y = y.to(device)

            optimizer.zero_grad()  # Zero gradients
            pred = model(x)  # Predict
            loss = loss_fn(pred, y)  # Compute loss
            loss.backward()  # Backpropagate
            optimizer.step()  # Update weights

            # Update counters
            _, predicted = torch.max(pred.data, 1)
            correct += sum([x == y for x, y in zip(predicted, y)])
            total += y.size(0)

        # Update performance metrics
        train_losses.append(loss.item())
        train_accuracies.append((correct / total).item())

        # Validate model
        model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for x, y in val_loader:
                # Move tensors to configured device
                x = x.to(device)
                y = y.to(device)

                pred = model(x)  # Predict

                # Update counters
                _, predicted = torch.max(pred.data, 1)
                correct += sum([x == y for x, y in zip(predicted, y)])
                total += y.size(0)

        # Update performance metrics
        val_losses.append(loss_fn(pred, y).item())
        val_accuracies.append((correct / total).item())

        print('- Epoch [{}/{}]: loss = {:.4f}, accuracy = {:.4f}%'.format(epoch + 1, num_epochs, train_losses[-1], 100 * train_accuracies[-1]))

        # Stop training early if no improvement over last few epochs
        if epoch >= 2 and val_losses[-1] >= val_losses[-2]:
            no_improvement += 1
        else:
            no_improvement = 0
        if no_improvement == no_improvement_patience:
            print('- Stopping: no improvement over last {} epochs'.format(no_improvement_patience))
            break

        # Save model state if best epoch so far
        if best_epoch is None or val_losses[-1] <= val_losses[best_epoch]:
            best_epoch = epoch
            best_model_state = model.state_dict()

    model.load_state_dict(best_model_state)
    print('- Best epoch: {}'.format(best_epoch + 1))

    return train_losses, train_accuracies, val_losses, val_accuracies


def test_model(model, test_loader: data.DataLoader) -> tuple[float, float]:
    """
    Tests the model with the given data.

    Arguments:
        model: The model to test.
        train_loader: The test data.

    Returns:
        TP, FP, TN, FN.
    """

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    precision = 0
    recall = 0

    model.eval()
    with torch.no_grad():
        tp = 0
        fp = 0
        tn = 0
        fn = 0

        for x, y in test_loader:
            # Move tensors to configured device
            x = x.to(device)
            y = y.to(device)

            pred = model(x)  # Predict

            # Update counters
            _, predicted = torch.max(pred.data, 1)
            tp += sum([x == 1 and y == 1 for x, y in zip(predicted, y)])
            fp += sum([x == 1 and y == 0 for x, y in zip(predicted, y)])
            tn += sum([x == 0 and y == 0 for x, y in zip(predicted, y)])
            fn += sum([x == 0 and y == 1 for x, y in zip(predicted, y)])

        # Calculate performance measures
        accuracy = (tp + tn) / (tp + fp + tn + fn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)

        print('- Accuracy: {:.4f}%'.format(100 * accuracy))
        print('- Precision: {:.4f}%'.format(100 * precision))
        print('- Recall: {:.4f}%'.format(100 * recall))

    return tp.item(), fp.item(), tn.item(), fn.item()
