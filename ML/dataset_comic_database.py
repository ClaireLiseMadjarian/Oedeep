# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 11:54:06 2022

@author: Gabriel
"""

import os
from torchvision.io import read_image
import torch
from torch.utils.data import Dataset

import torchvision.transforms as tr
import pandas as pd

class ComicDataset(Dataset):
    def __init__(self, path, index_name="index.csv"):
        self.path = path
        dataframe = pd.read_csv(path+"/"+index_name, index_col=0)
        self.labels =  dataframe["genre"]
        self.database_ids = dataframe["ids"]
        self.transforms = tr.Resize((768,512))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.path, self.database_ids[idx]) + ".jpg"
        print(img_path)
        image =  read_image(img_path)
        image = self.transforms(image)
        return image.float(), self.labels[idx]
    
