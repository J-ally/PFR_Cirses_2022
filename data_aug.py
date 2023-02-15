# -*- coding: utf-8 -*-
"""
Created on Feb 14 2023
@author:  nora picaut
"""

import torch
import torchvision.transforms.functional as TF


class DataAugmentation():
    def __init__(self, mean=0, std=0.1):
        self.std = std
        self.mean = mean
        
    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean
    
    def create_dataset(self) :
        """"""
        
        return
    
    def rotation_subimages (self, dataset) :
        """rotation de toutes les imagettes"""
        
        imagettes = []
        labels = []

        # on veut multiplier le nombre d'imagettes par 4 donc pour chaque imagettes on fait 3 rotations différentes
        angles = [90, 180, 270]

        for image, label in dataset:
            # on effectue des transformations pour avoir des dimensions de type (1 , 3 , 100, 100)
            # car la fonction rotate ci-dessous ne prends que les dimensions 4 ou 5
            im = image/255
            im = im.unsqueeze(0)
            for degre in angles:
                out = TF.rotate(im, degre)
                imagettes.append((out.squeeze().permute(1,2,0))*255)
            imagettes.append((im.squeeze().permute(1,2,0))*255)
            # on récupère les labels
            labels.append(label)