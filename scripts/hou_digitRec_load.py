# hou

node = hou.pwd()
geo = node.geometry()

# modules

import numpy as np

import torch

import torch.nn as nn
import torch.optim as optim

from torch.utils import backcompat
from torch.utils.data.dataset import Dataset

import torchvision
import torchvision.transforms as transforms

from datetime import datetime

# cpu device config

device = torch.device('cpu')

# Parameters

input_size = 784 # 28 x 28 pixels
hidden_size = 100
num_classes = 10 # 10 digits 
num_epochs = 20
batch_size = 1
learning_rate = 0.001

# Model Output Location

PATH = "`$HIP`/model/model.pth"

# data shape

h = 28
w = h
c = 1 # grayscale = 1 | rgb = 3

data = np.zeros((h,w,c), dtype=np.uint8) # this has to be the same shape as before
shape = data.shape

# count points

N = len(geo.points())

# create numpy array from input and target

numpy_input = np.zeros((N,784), 'float32')
numpy_output =  np.zeros((N,1), 'float32')

for i,point in enumerate(geo.points()):
    numpy_input[i] = np.asarray(point.attribValue('input'))
    numpy_output[i] = np.asarray(point.attribValue('target'))

# Transformer

class ReshapeToTensor:
    def __init__(self):
        pass

    def __call__(self, sample):
        inputs, targets = sample
        input_np = np.asarray(inputs.astype(np.uint8)).reshape(shape) # reshape to numpy image dimensions ( X, Y, C )
        input_np = np.swapaxes(input_np,0,1)
        inputs = torchvision.transforms.functional.to_tensor(input_np) # performs axes swap from ( X, Y, C ) to ( C, X, Y) and converts from 0-255 uint8 to 0-1 floats
        targets = torch.from_numpy(targets)
        targets = torch.max(targets, 0)[0]
        targets = targets.type(torch.LongTensor)
        return inputs, targets

transform = ReshapeToTensor()

# Dataset  

class digitDataset(Dataset):
    def __init__(self, transform=None):
        self.n_samples = numpy_input.shape[0]
        self.input = numpy_input
        self.target = numpy_output
        self.transform = transform

    def __getitem__(self, index):
        sample = self.input[index], self.target[index]
        if self.transform:
            sample = self.transform(sample)
        return sample

    def __len__(self):
        return self.n_samples

dataset = digitDataset(transform=transform)
  

# Prediciton Set
      
pred_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=False)

# Sanity Check 

'''
examples = iter(pred_loader)
example_data, example_targets = examples.next()
 
#print("Example Input:\n", example_data[0])
print('--------------------------')
print("Example Input Shape:   ",example_data[0].shape)
print('--------------------------')
print("Example Target:        ",example_targets[0])
print('--------------------------')
print("Example Target Shape:  ",example_targets[0].shape)
print('--------------------------')
print("Example Target Shape:  ",example_targets[0].type())
print('--------------------------')
print("Pred Set Batch Shape:  ", example_data.shape)
print('--------------------------')
print("Pred Set Length:       ", dataset.__len__())
print('--------------------------')
'''

# Model

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        return out

model = NeuralNet(input_size, hidden_size, num_classes)

# Import Trained Model

model.load_state_dict(torch.load(PATH, map_location=device))
model.eval()
    
# Prediction

with torch.no_grad():

    for i, (input, target) in enumerate(pred_loader):
        input = input.reshape(-1, 28*28).to(device)
        target = target.to(device)
        outputs = model(input)
        
        _, predicted = torch.max(outputs.data, 1)
       
        #probabilities
        sm = torch.nn.Softmax()
        probabilities = sm(outputs) 
        fp = probabilities.ravel()
        fp = fp.numpy()
        
    prediction = predicted[i].item()
    
    # print('--------------------------')
    # print("Predicted Output:  ",prediction)

    for i,point in enumerate(geo.points()):
        point.setAttribValue("pred", prediction)  
        
    for i,point in enumerate(geo.points()):
        point.setAttribValue("prob", fp.astype(np.float64))

# print('--------------------------')
# print(datetime.now())