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

subimages_path = f"{root_data_path}/Subimages/"
create_folder(subimages_path)

normal_subimage_path = f"{subimages_path}/Normal"
pos_sub_path = f"{normal_subimage_path}/Positive"
neg_sub_path = f"{normal_subimage_path}/Negative"

# Cut images
cut_size = (100,100)

# all subimages path
data_original_all = [f for f in os.listdir(normal_subimage_path) if f.endswith(".jpg")]
all_normal_subimages_path = [f for f in os.listdir(normal_subimage_path) if f.endswith(".jpg")]
all_normal_pos_subimages_path = [f for f in os.listdir(pos_sub_path) if f.endswith(".jpg")]
all_normal_neg_subimages_path = [f for f in os.listdir(neg_sub_path) if f.endswith(".jpg")]

normal_subimages_whole_dir = []

for root, dirs, files in os.walk(normal_subimage_path):
    for file in files:
        if file.endswith(".jpg"):
             normal_subimages_whole_dir.append(os.path.join(root, file))
