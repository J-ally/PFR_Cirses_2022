# -*- coding: utf-8 -*-
"""
Created on Feb 14 2023
@author:  jaly
"""

###############################################################################
#    _____ _____ _____   _____ ______  _____      _____  ______ _____ ____  
#   / ____|_   _|  __ \ / ____|  ____|/ ____|    |  __ \|  ____/ ____/ __ \ 
#  | |      | | | |__) | (___ | |__  | (___      | |__) | |__ | |   | |  | |
#  | |      | | |  _  / \___ \|  __|  \___ \     |  _  /|  __|| |   | |  | |
#  | |____ _| |_| | \ \ ____) | |____ ____) |    | | \ \| |___| |___| |__| |
#   \_____|_____|_|  \_\_____/|______|_____/     |_|  \_\______\_____\____/
# 
###############################################################################
#
#  First all the annotations must be done (images must be located in the folder "/Images"  to do so)
#      |-> the annotations are done by running the annotation.py script
#  Then we preprocess them
#      |-> the preprocessing is done by running the preprocessing.py script
#
#
# use it with the following commands, which can be found in the README.md file as well :
# $ python full_process.py --preprocess True --subimages True --subimage_size (100, 100) 
#               --data_augmentation True


import os
import sys
import cv2
import argparse
import numpy as np
import time
import pandas as pd

import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.data import TensorDataset

from torch.optim import Adam
from torch.optim.lr_scheduler import StepLR
from torch.optim.lr_scheduler import StepLR
from torch.utils.data.sampler import SubsetRandomSampler

import torch.nn as nn
from torch.nn import CrossEntropyLoss
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms.functional as TF
from torchvision import transforms

from tqdm import tqdm
from preprocessing import Preprocessor
from data_aug import AddRotation
from data_aug import AddGaussianNoise
from subimage_creation import SubimageCreator

###############################################################################
#                                 GLOBALS                                     #
###############################################################################

IMAGES_PATHS = ["Images/" + f for f in os.listdir("Images/") if f.endswith(".jpg")]
SUBIMAGES_POS_PATHS = ["Images/Subimages/Positive/"+ f for f in os.listdir("Images/Subimages/Positive") if f.endswith(".jpg")]
SUBIMAGE_NEG_PATHS = ["Images/Subimages/Negative/" + f for f in os.listdir("Images/Subimages/Negative") if f.endswith(".jpg")]
SUBIMAGE_TOT_PATHS = SUBIMAGES_POS_PATHS + SUBIMAGE_NEG_PATHS

DATA_PATHS = r"Images/Subimages"


###############################################################################
#                                MODEEEEEL                                    #
###############################################################################

class DataSplit:
    """
    Replace DataLoader !
    Allows to triple Load the data into three differents sets : train, test and val
    The size of the datasets depends on the splits inputed as train_split, val_split and test_split
    It is possible to have the data randomly sampled with the argument shuffle = True
    """
    def __init__(self, dataset, train_split=0.8, val_split=0.1, shuffle=False):
        """
        Initialize the data split based on the splits given in inputs
        Inputs : 
            - dataset : dataset loaded with torchivison.datasets.ImageFolder()
            - train_split, val_split and test_split : the size of the splits in % of the dataset size
            - shuffle : the possibility of sampling randomly through the dataset
        """
        self.dataset = dataset
        dataset_size = len(dataset)
        self.indices = list(range(dataset_size)) #all the indices
 
        #the quantity of data in each section of dataset
        train_split = int(np.floor(train_split * dataset_size))
        val_split = int(np.floor(val_split * dataset_size))
        #test split is what is left not sampled
    
        if shuffle:
            np.random.shuffle(self.indices)
        
        self.train_indices = self.indices[:train_split]
        self.val_indices = self.indices[train_split : train_split + val_split]
        self.test_indices = self.indices[train_split + val_split :]

        self.train_sampler = SubsetRandomSampler(self.train_indices)
        self.val_sampler = SubsetRandomSampler(self.val_indices)
        self.test_sampler = SubsetRandomSampler(self.test_indices)


    def get_split(self, batch_size=64, num_workers=4):
        print('Initializing train-validation-test dataloaders')
        self.train_loader = self.get_train_loader(batch_size=batch_size, num_workers=num_workers)
        self.val_loader = self.get_validation_loader(batch_size=batch_size, num_workers=num_workers)
        self.test_loader = self.get_test_loader(batch_size=batch_size, num_workers=num_workers)
        return self.train_loader, self.val_loader, self.test_loader


    def get_train_loader(self, batch_size=50, num_workers=4):
        print('Initializing train dataloader')
        self.train_loader = DataLoader(self.dataset, batch_size=batch_size, sampler=self.train_sampler, shuffle=False, num_workers=num_workers)
        return self.train_loader


    def get_validation_loader(self, batch_size=50, num_workers=4):
        print('Initializing validation dataloader')
        self.val_loader = DataLoader(self.dataset, batch_size=batch_size, sampler=self.val_sampler, shuffle=False, num_workers=num_workers)
        return self.val_loader


    def get_test_loader(self, batch_size=50, num_workers=4):
        print('Initializing test dataloader')
        self.test_loader = DataLoader(self.dataset, batch_size=batch_size, sampler=self.test_sampler, shuffle=False, num_workers=num_workers)
        return self.test_loader
    
    
class our_pipeline:
    def __init__(self,feature, num_epochs:int, early_stopping_threshold:int):
        
        self.net = feature[0]
        self.model = feature[1]
        self.train = feature[2]
        self.val = feature[3]
        self.test = feature[4]

        self.num_epochs = num_epochs
        self.early_stopping_threshold = early_stopping_threshold
        self.nb_class = len(self.train.dataset.classes)

        self.optimizer = Adam(self.model.parameters())
        #self.scheduler = CyclicLR(self.optimizer, base_lr=0.001, max_lr=0.01, step_size=10, mode='triangular')
        self.criterion = nn.CrossEntropyLoss()
        self.scheduler = StepLR(self.optimizer, step_size=10)

    def performances(self, data):

        #les métriques déjà programmées ne conviennent pas on crée les notres
        #Calcul de la sensibilité et de la spécificité
        nb_correct_pred = [0] * self.nb_class
        nb_total_pred = [0] * self.nb_class

        with torch.no_grad():
            for inputs, labels in data:
                outputs = self.model(inputs)
                #Sorti du model liste de proba d'appartenir à une classe
                #pred = argmax de la liste
                _, predicted = torch.max(outputs.data, 1)

                for i in range(len(labels)):
                    if labels[i] == predicted[i]:
                        nb_correct_pred[labels[i]] += 1
                    nb_total_pred[labels[i]] += 1
                
            self.good_pred = [nb_correct_pred[i] / nb_total_pred[i] for i in range(self.nb_class)]
        return self.good_pred

    def training(self):
        self.model.train()
        for inputs, labels in self.train:
            #réinitialisation du gradient
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

    def row(self, epoch):
        #Pour chaque epoch on veut avoir l'historique des performances sur train
        #et sur val ==> 1 ligne de data frame = perf d'1 epoch
        train_perf = self.performances(self.train)
        val_perf = self.performances(self.val)

        # balanced acc = (sepecificité + sensibilité)/2
        self.bal_acc_val = val_perf[0]+val_perf[1]/self.nb_class
        self.bal_acc_train = train_perf[0]+train_perf[1]/self.nb_class

        self.newrow = pd.DataFrame({'mod': [self.net], 'epoch': [epoch],
                            'true_neg_train':[train_perf[0]], 'true_pos_train':[train_perf[1]],
                            'true_neg_val':[val_perf[0]], 'true_pos_val':[val_perf[1]],
                            'balanced_acc_train': [self.bal_acc_train],
                            'balanced_acc_val': [self.bal_acc_val]
                            },index=[0])
        
        return self.newrow, self.bal_acc_val
        # on renvoi self.bal_acc_val car on s'en sert pour arrêter l'entrainement
        #En cas de surapprentissage

    def training_loop(self, print_res : bool):

        counter = 0
        best_acc = 0.0

        col_names = ['mod', 'epoch', 'true_neg_train', 'true_pos_train',
                        'true_neg_val', 'true_pos_val', 'balanced_acc_train',
                        'balanced_acc_val']

        stats = pd.DataFrame(columns=col_names)

        for epoch in range(self.num_epochs):
            self.training()
            perfs = self.row(epoch)
            if print_res : 
                print("state", self.net, ": ", epoch, "/", self.num_epochs)
                print(perfs[0])
            #A chaque époque on ajoute les stats
            stats = pd.concat([stats, perfs[0]])

            if perfs[1] > best_acc:
                best_acc = perfs[1]
                best_mod = self.model.state_dict()
                counter = 0
            else:
                counter += 1

            if counter >= self.early_stopping_threshold:
                if print_res : 
                    print("Early stopping at epoch: ", epoch+1)
                break
        #Sauvegarde du model avec l'heure
        now = time.time()
        mod_save_path = f"/work/{now}-Models_history/" + self.net + ".pt"
        torch.save(best_mod, mod_save_path)

        #Sauvegarde de l'historique avec l'heure
        stats_save_path = "/work/{now}-Models_history/" + self.net + ".csv"
        stats.to_csv(stats_save_path, index=False)


###############################################################################
#                                  PARSER                                     #
###############################################################################

def make_parser() :
    """
    Parser function for the arguments of the pipeline
    Inputs :
    Returns : the parser itself
    """
    parser = argparse.ArgumentParser(description='Data Pipeline for Cirses Recognition.')
    parser.add_argument('--subimages', type=bool, default=True, help='Creates the subimages (defau: True)')
    parser.add_argument('--preprocess', type=bool, default=True, help='Preprocess the images (default: True)')
    parser.add_argument('--subimage_size', type=tuple, default=(100, 100), help='The size of the subimages (default: (100, 100))')
    parser.add_argument('--data_augmentation', type=bool, default=True, help='Data augmentation (default: True)')
    
    return parser

###############################################################################
#                                MAAAAIIN                                     #
###############################################################################

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    parser = make_parser()
    args = parser.parse_args()
    
    #begin by cutting the images into subimages (if needed)
    if args.subimages :
        for i, image_path in enumerate(IMAGES_PATHS) :
            print(f"Image {i} out of {len(IMAGES_PATHS)} -- Creating subimages for the image : {image_path}")
            sushi = SubimageCreator(image_path, size=(100, 100))
            sushi.cut()
    
    #then annotating the images (if needed)
    if args.annotation :
        os.system("annotation.py")
    
    if args.preprocess : #then preprocess the images (if needed)
        for i, photos in enumerate (IMAGES_PATHS) :
            print(f"Subimage {i} out of {len(IMAGES_PATHS)} -- Preprocessing the image : {photos}")
            preprocessor = Preprocessor(photos, args.subimage_size) #creating the three different preprocessed images
            preprocessor.cut() #cutting the images into subimages
            # preprocessor.rebuild(prefix="", image_type="Normal") #rebuilding the images

    if args.data_augmentation : #then do the data augmentation on the subimages (if needed)
        #gaussian noise
        data_noisy = torchvision.datasets.ImageFolder(root=DATA_PATHS, \
                        transform=transforms.Compose([transforms.ToTensor(),AddGaussianNoise()]))
        #and rotation
        rota = AddRotation(data_noisy)
        rota.rotation_subimages()
        final_data = TensorDataset(rota.imagettes, rota.labels)
        
    else : #no data augmentation
        final_data = torchvision.datasets.ImageFolder(root=DATA_PATHS, transform=transforms.ToTensor())


    ###### THE REAL PIPELINE
    if args.preprocess : # triple the size of the dataset
        B = DataSplit(final_data, shuffle=True, batch_size=32)
        
    B = DataSplit(final_data, shuffle=True)
    train = B.get_train_loader()
    test = B.get_test_loader()
    val = B.get_validation_loader()
        
    
    
if __name__ == "__main__" :
    print(IMAGES_PATHS[0])
    print(SUBIMAGE_TOT_PATHS[0:3])
    main()