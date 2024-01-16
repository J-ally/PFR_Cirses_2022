# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os
import shutil

###############################################################################
#                                 FUNCTIONS                                   #
###############################################################################


# def copy_folder (source :str, destination:str):
#     """
#     Copy the images from the source folder to the destination folder
#     Args:
#         source (str): the path of the source folder
#         destination (str): the path of the destination folder
#     """
#     if os.name == 'nt':
#         os.popen(f'copy {source} {destination}') # copying the images to the destination folder
#     else :
#         os.popen(f'cp {source} {destination}') # copying the images to the destination folder

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

pos_sub_path = f"{subimages_path}/Normal/Positive"
neg_sub_path = f"{subimages_path}/Normal/Negative"

# Cut images
cut_size = (100,100)

# all subimages path
data_original_all = [f for f in os.listdir(subimages_path) if f.endswith(".jpg")]

# Data augmentation
#original_path = "C:\Users\Administrateur\Downloads\data-20230124T132215Z-001.zip"
#new_path = "C:\Users\Administrateur\Downloads\augmentation\data-20230124T132215Z-001.zip"
