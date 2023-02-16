# -*- coding: utf-8 -*-
"""
Created on Feb 14 2023
@author:  nora picaut
"""

import torch
import torchvision.transforms.functional as TF


class AddGaussianNoise():
    def __init__(self, mean=0, std=0.1):
        self.std = std
        self.mean = mean
        
    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean

class AddRotation():
    
    def __init__(self, dataset):
        self.dataset = dataset 
        # dataset = torchvision.datasets.ImageFolder(root=DATA_PATHS, 
        #                   transform=transforms.Compose([transforms.ToTensor(),AddGaussianNoise()]))
        self.imagettes = []
        self.labels = []
    
    
    def rotation_subimages (self) :
        """
        rotation de toutes les imagettes
        change imagettes et labels de la classe !
        """

        # on veut multiplier le nombre d'imagettes par 4 donc pour chaque imagettes on fait 3 rotations différentes
        angles = [90, 180, 270]

        for image, label in self.dataset:
            # on effectue des transformations pour avoir des dimensions de type (1 , 3 , 100, 100)
            # car la fonction rotate ci-dessous ne prends que les dimensions 4 ou 5
            im = image/255
            im = im.unsqueeze(0)
            for degre in angles:
                out = TF.rotate(im, degre)
                # adding the transformed imagettes and labels
                self.imagettes.append((out.squeeze().permute(1,2,0))*255)
                self.labels.append(label)
            # adding the initial imagettes and labels
            self.imagettes.append((im.squeeze().permute(1,2,0))*255)
            self.labels.append(label)
        
    