# -*- coding: utf-8 -*-
"""CNNFashionMnistGPU.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AA3vJLOIu5BAJdlUZ3CNfZEx4iMLZuNC
"""

import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import torch.nn.functional as F
device = 'cuda' if torch.cuda.is_available() else 'cpu'

trainset = torchvision.datasets.FashionMNIST(
    root = './data/FashionMNIST',
    download = True,
    train = True,
    transform = transforms.Compose(
        [transforms.ToTensor()]
    )
)

trainloader = torch.utils.data.DataLoader(trainset, batch_size=100)
batch = next(iter(trainloader))
images,labels = batch

grid = torchvision.utils.make_grid(images,nrow=10)
plt.figure(figsize=(15,15))
plt.imshow(np.transpose(grid, axes=[1,2,0]))
print('Labels: ', labels)

class Net(torch.nn.Module):
  def __init__(self):
    super(Net,self).__init__()
    self.conv1 = torch.nn.Conv2d(in_channels=1,out_channels=6,kernel_size=5)
    self.conv2 = torch.nn.Conv2d(in_channels=6, out_channels=12,kernel_size=5)
    self.fc1 = torch.nn.Linear(12*4*4,120)
    self.fc2 = torch.nn.Linear(120,60)
    self.out = torch.nn.Linear(60,10)

  def forward(self,x):
    x = self.conv1(x)
    x = F.relu(x)
    x = F.max_pool2d(x, kernel_size = 2, stride = 2)
    x = self.conv2(x)
    x = F.relu(x)
    x = F.max_pool2d(x, kernel_size = 2, stride = 2)
    x = self.fc1(x.reshape(-1,12*4*4))
    x = F.relu(x)
    x = self.fc2(x)
    x = F.relu(x)
    return self.out(x)

network = Net()
network.to(device)

#Function to get number of correct predictions
def get_num_correct(datas,label):
  return datas.argmax(dim=1).eq(label).sum().item()

#Defining optimization algorithm
optimizer = torch.optim.Adam(params=network.parameters(), lr=0.01)

for epoch in range(10):
    
    total_loss = 0
    total_correct = 0
    
    for batch in trainloader: # Get Batch
        x,y = batch
        images, labels = x.to(device), y.to(device)

        preds = network(images) # Pass Batch
        loss = F.cross_entropy(preds, labels) # Calculate Loss

        optimizer.zero_grad()
        loss.backward() # Calculate Gradients
        optimizer.step() # Update Weights

        total_loss += loss.item()
        total_correct += get_num_correct(preds, labels)

    print(
        "epoch", epoch, 
        "total_correct:", total_correct, 
        "loss:", total_loss
    )
print('Model Accuary: ',total_correct/len(trainset),'%')