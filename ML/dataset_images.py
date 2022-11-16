# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 11:54:06 2022

@author: Gabriel
"""

import os
import cv2
from torchvision.io import read_image
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import torchvision.transforms as tr
import numpy as np

class TestComicDataset(Dataset):
    def __init__(self, path, labels_list):
        self.path = path
        self.list_name_panels = []
        self.labels = []
        self.labels_list= labels_list
        for i in range(len(labels_list)):
            files =  os.listdir(path+"/"+labels_list[i]+"/jpg_files")
            for f in files:
                if f[-4:] == ".jpg":
                    self.labels.append(i)
                    self.list_name_panels.append(f)
        self.transforms = tr.Resize((768,512))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.path, self.labels_list[self.labels[idx]],
                                "jpg_files",self.list_name_panels[idx])
        # print(img_path)
        # image = cv2.imread(img_path)
        image =  read_image(img_path)
        image = self.transforms(image)
        return image.float(), torch.tensor(self.labels[idx])
    
# path = r"C:\Users\Gabriel\Documents\_Documents\Etudes\3A\9.6 Deep Learning\Projet DL\data"
# genres = ["Advocacy", "Animal"]
# dataset = TestComicDataset(path,genres)
# for i in np.random.randint(0,len(dataset),10):
#     img,l = dataset[i]
    
#     plt.subplots(figsize=(1414/plt.rcParams['figure.dpi'] , 1000/plt.rcParams['figure.dpi'] )); plt.axis("off")
#     plt.imshow(img.moveaxis(0,2))
#     plt.show()
#     print(l)
