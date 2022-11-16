import os

import numpy as np
import pandas as pd


from torch.utils.data import TensorDataset, DataLoader, Dataset
import torchvision.transforms as transforms
from torchvision import models
import torch.nn.functional as F
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from dataset_images import TestComicDataset

path = r"C:\Users\Gabriel\Documents\_Documents\Etudes\3A\9.6 Deep Learning\Projet DL\data"
genres = ["Advocacy", "Animal"]
dataset = TestComicDataset(path,genres)
print(len(dataset))

# Data
# Train and test dataloaders: ....
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [len(dataset)-500, 500],
                                                            generator=torch.Generator().manual_seed(631))

train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)
test_dataloader  = torch.utils.data.DataLoader(test_dataset,  batch_size=8, shuffle=False)

# # Exploratory stats
# # Iterating over the training dataset and storing the target class for each sample
# classes = []
# for batch_idx, data in enumerate(train_dataloader, 0):
#     x, y = data
#     classes.append(y)

# # Calculating the unique classes and the respective counts and plotting them
# unique, counts = np.unique(classes, return_counts=True)
# names = list(dataset.class_to_idx.keys())
# plt.bar(names, counts)
# plt.xlabel("Target Classes")
# plt.ylabel("Number of training instances")
# plt.show()


# Define the model
class CNNNetwork(nn.Module):

    def __init__(self):
        super().__init__()
        # 4 conv blocks / flatten / linear / softmax
        self.model = nn.Sequential(
        nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3), nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3), nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3), nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3), nn.ReLU(), nn.MaxPool2d(kernel_size=2),
        nn.Flatten(),
        nn.Linear(176640, 32), nn.ReLU(),
        nn.Linear(32,2))

    def forward(self, input_data):
        return self.model(input_data)


def train_optim(model, epochs, log_frequency, device, learning_rate=1e-1):
    model.to(device)  # we make sure the model is on the proper device

    # Multiclass classification setting, we use cross-entropy
    # note that this implementation requires the logits as input
    # logits: values prior softmax transformation
    loss_fn = torch.nn.CrossEntropyLoss(reduction='mean')

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for t in range(epochs):

        model.train()  # we specify that we are training the model

        # At each epoch, the training set will be processed as a set of batches
        for batch_id, batch in enumerate(train_dataloader):

            images, labels = batch
            

            # we put the data on the same device
            images, labels = images.to(device), labels.to(device)
            # plt.subplots(figsize=(1414/plt.rcParams['figure.dpi'] , 1000/plt.rcParams['figure.dpi'] )); plt.axis("off")
            # plt.imshow(images.moveaxis(0,2))
            # plt.show()

            y_pred = model(images)  # forward pass output=logits

            loss = loss_fn(y_pred, labels)

            if batch_id % log_frequency == 0:
                print("epoch: {:03d}, batch: {:03d}, loss: {:.3f} ".format(t + 1, batch_id + 1, loss.item()))

            optimizer.zero_grad()  # clear the gradient before backward
            loss.backward()  # update the gradient

            optimizer.step()  # update the model parameters using the gradient

        # Model evaluation after each step computing the accuracy
        model.eval()
        total = 0
        correct = 0
        for batch_id, batch in enumerate(test_dataloader):
            images, labels = batch
            images, labels = images.to(device), labels.to(device)
            y_pred = model(images)  # forward computes the logits
            sf_y_pred = torch.nn.Softmax(dim=1)(y_pred)  # softmax to obtain the probability distribution
            _, predicted = torch.max(sf_y_pred, 1)  # decision rule, we select the max

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print("[validation] accuracy: {:.3f}%\n".format(100 * correct / total))


model = CNNNetwork()
device = torch.device("cuda:0")
# train_optim(...)

#%%

model = CNNNetwork()

train_optim(model, 10, 100, "cuda")