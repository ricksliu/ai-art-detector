import torch.nn as nn


class Network(nn.Module):
    """
    CNN used by the model.
    """

    def __init__(self):
        super(Network, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=(3, 3), padding=(1, 1))
        self.conv1_relu = nn.ReLU(inplace=True)

        self.pool1 = nn.MaxPool2d(kernel_size=(2, 2))
        self.norm1 = nn.BatchNorm2d(num_features=32)

        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3), padding=(1, 1))
        self.conv2_relu = nn.ReLU(inplace=True)

        self.pool2 = nn.MaxPool2d(kernel_size=(2, 2))
        self.norm2 = nn.BatchNorm2d(num_features=64)

        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), padding=(1, 1))
        self.conv3_relu = nn.ReLU(inplace=True)

        self.pool3 = nn.MaxPool2d(kernel_size=(2, 2))
        self.norm3 = nn.BatchNorm2d(num_features=128)

        self.lin1 = nn.Linear(in_features=18432, out_features=256)
        self.lin1_relu = nn.ReLU(inplace=True)

        self.drop1 = nn.Dropout(p=0.2)

        self.lin2 = nn.Linear(in_features=256, out_features=2)
        self.lin2_act = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1_relu(self.conv1(x))
        x = self.norm1(self.pool1(x))

        x = self.conv2_relu(self.conv2(x))
        x = self.norm2(self.pool2(x))

        x = self.conv3_relu(self.conv3(x))
        x = self.norm3(self.pool3(x))

        x = x.reshape(x.size(0), -1)

        x = self.lin1_relu(self.lin1(x))
        x = self.drop1(x)
        x = self.lin2_act(self.lin2(x))

        return x
