# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os

###############################################################################
#                                 FUNCTIONS                                   #
###############################################################################


def copy_folder (source :str, destination:str):
    """
    Copy the images from the source folder to the destination folder
    Args:
        source (str): the path of the source folder
        destination (str): the path of the destination folder
    """
    if os.name == 'nt':
        os.popen(f'copy {source} {destination}') # copying the images to the destination folder
    else :
        os.popen(f'cp {source} {destination}') # copying the images to the destination folder

def create_folder(path :str):
    """
    Create a folder
    Args:
        path (str): the path of the folder
    """
    if not os.path.exists(path):
        os.makedirs(path)
        
# Annotation 

root_data_path = "./Images"
all_images_path = [os.path.join(root_data_path,f) for f in os.listdir(root_data_path) 
                   if os.path.isfile(os.path.join(root_data_path,f))]

subimages_path = f"{root_data_path}/Subimages"
create_folder(subimages_path)
    
pos_sub_path = f"{subimages_path}/Positive"
create_folder(pos_sub_path)
    
neg_sub_path = f"{subimages_path}/Negative"
create_folder(neg_sub_path)

# Skeleton preprocessing
# Setting the source and the destination folders
sklt_path = "./Img_Skeleton"
create_folder(sklt_path)
copy_folder(root_data_path, sklt_path)
all_images_sklt_path = [os.path.join(sklt_path,f) for f in os.listdir(sklt_path) 
                   if os.path.isfile(os.path.join(sklt_path,f))]

# ExG preprocessing
EXG_path = "./Img_ExG"
create_folder(EXG_path)
copy_folder(root_data_path, EXG_path)
all_images_exg_path = [os.path.join(EXG_path,f) for f in os.listdir(EXG_path) 
                   if os.path.isfile(os.path.join(EXG_path,f))]

# Cut images
cut_size = (100,100)

# all subimages path
data_original_all = [f for f in os.listdir(subimages_path) if f.endswith(".jpg")]
data_original_pos = [f for f in os.listdir(pos_sub_path) if f.endswith(".jpg")]
data_original_neg = [f for f in os.listdir(neg_sub_path) if f.endswith(".jpg")]
data_sklt = [f for f in os.listdir(sklt_path) if f.endswith(".jpg")]

# Data augmentation
#original_path = "C:\Users\Administrateur\Downloads\data-20230124T132215Z-001.zip"
#new_path = "C:\Users\Administrateur\Downloads\augmentation\data-20230124T132215Z-001.zip"
