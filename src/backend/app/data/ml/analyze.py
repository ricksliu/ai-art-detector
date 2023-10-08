from matplotlib import pyplot as plt


def plot_loss(train_losses: list[float], val_losses: list[float], path: str):
    """
    Plots loss vs epoch.

    Arguments:
        train_losses: The list of train losses over the epochs.
        val_losses: The list of validation losses over the epochs.
        path: The path to save the plot to.
    """

    plt.clf()
    plt.plot([i + 1 for i in range(len(train_losses))], train_losses, label='Train')
    plt.plot([i + 1 for i in range(len(val_losses))], val_losses, label='Validation')
    plt.title('Loss vs Epoch\nTrain: {:.4f}, Validation: {:.4f}'.format(train_losses[-1], val_losses[-1]))
    plt.legend(loc='upper center')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig(path)


def plot_accuracy(train_accuracies: list[float], val_accuracies: list[float], path: str):
    """
    Plots accuracy vs epoch.

    Arguments:
        train_accuracies: The list of train accuracies over the epochs.
        val_accuracies: The list of validation accuracies over the epochs.
        path: The path to save the plot to.
    """

    plt.clf()
    plt.plot([i + 1 for i in range(len(train_accuracies))], [100 * i for i in train_accuracies], label='Train')
    plt.plot([i + 1 for i in range(len(val_accuracies))], [100 * i for i in val_accuracies], label='Validation')
    plt.title('Accuracy vs Epoch\nTrain: {:.4f}, Validation: {:.4f}'.format(train_accuracies[-1], val_accuracies[-1]))
    plt.legend(loc='upper center')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.savefig(path)


def plot_confusion_matrix(tp: int, fp: int, tn: int, fn: int, path: str):
    """
    Plots the confusion matrix.

    Arguments:
        tp: The number of true positives.
        fp: The number of false negatives.
        tn: The number of true positives.
        fn: The number of false negatives.
        path: The path to save the plot to.
    """

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    confusion_matrix = [[tn, fp], [fn, tp]]

    plt.clf()
    plt.title('Confusion Matrix\nPrecision: {:.4f}, Recall: {:.4f}'.format(precision, recall))
    plt.xticks([0, 1])
    plt.xlabel('Predicted')
    plt.yticks([0, 1])
    plt.ylabel('Actual')
    plt.imshow(confusion_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(2):
        for j in range(2):
            plt.text(x=j, y=i, s=confusion_matrix[i][j], va='center', ha='center')
    plt.savefig(path)
