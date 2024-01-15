# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os

# Annotation 
root_data_path = './Images'
all_images_path = [os.path.join(root_data_path,f) for f in os.listdir(root_data_path) 
                   if os.path.isfile(os.path.join(root_data_path,f))]

subimages_path = f"{root_data_path}/Subimages"
if not os.path.exists(subimages_path):
    os.makedirs(subimages_path)
    
pos_sub_path = f"{subimages_path}/Positive"
if not os.path.exists(pos_sub_path):
    os.makedirs(pos_sub_path)
    
neg_sub_path = f"{subimages_path}/Negative"
if not os.path.exists(neg_sub_path):
    os.makedirs(neg_sub_path)
    
sklt_path = "./Img_Skeleton"
if not os.path.exists(sklt_path):
    os.makedirs(sklt_path)

# all subimages path
data_original_all = [f for f in os.listdir(subimages_path) if f.endswith(".jpg")]
data_original_pos = [f for f in os.listdir(pos_sub_path) if f.endswith(".jpg")]
data_original_neg = [f for f in os.listdir(neg_sub_path) if f.endswith(".jpg")]
data_sklt = [f for f in os.listdir(sklt_path) if f.endswith(".jpg")]

# Data augmentation
original_path = "C:\Users\Administrateur\Downloads\data-20230124T132215Z-001.zip"
new_path = "C:\Users\Administrateur\Downloads\augmentation\data-20230124T132215Z-001.zip"
