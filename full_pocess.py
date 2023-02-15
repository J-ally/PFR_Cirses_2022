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
# $ python full_process.py --preprocess True --photo 00000000.jpg --subimage_size (100, 100) 
#               --data_augmentation True


import os
import sys
import cv2
import argparse
from preprocessing import Preprocessor

###############################################################################
#                                 GLOBALS                                     #
###############################################################################

IMAGES = [f for f in os.listdir("Images/") if f.endswith(".jpg")]
SUBIMAGES_POS = [f for f in os.listdir("Images/Subimages/Positive") if f.endswith(".jpg")]

###############################################################################
#                                  PARSER                                     #
###############################################################################

# python train_KE_cls.py --epochs 200 --num_generations 11 --name resetlayer4_flower_resnet18 
# --weight_decay 0.0001 --arch Split_ResNet18 --reset_layer_name layer4 --set Flower102 
# --data $DATA_DIR --no_wandb

def make_parser() :
    """
    Parser function for the arguments of the pipeline
    Inputs :
    Returns : the parser itself
    """
    
    parser = argparse.ArgumentParser(description='Data Pipeline for Cirses Recognition.')
    parser.add_argument('--preprocess', type=bool, default=True, help='Preprocess the images (default: True)')
    parser.add_argument('--subimage_size', type=tuple, default=(100, 100), help='The size of the subimages (default: (100, 100))')
    parser.add_argument('--data_augmentation', type=bool, default=True, help='Data augmentation (default: True)')
    
    return parser

def main():
    parser = make_parser()
    args = parser.parse_args()
    
    if args.preprocess :
        for photos in IMAGES :
            print("Preprocessing the image : ", photos)
            preprocessor = Preprocessor(f"/Images/{photos}", args.subimage_size) 
            preprocessor.cut() #cutting the images into subimages
            preprocessor.rebuild(prefix="", image_type="Normal") #rebuilding the images

    if args.data_augmentation :
        for sub in SUBIMAGES_POS :
            print("Data augmentation of the image : ", sub)
            
            
if __name__ == "__main__" :
    print(IMAGES[0])
    main()