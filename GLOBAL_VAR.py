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
pos_sub_path = f"{subimages_path}/Positive"
neg_sub_path = f"{subimages_path}/Negative"
sklt_path = f"{subimages_path}/Skeleton"

# all subimages path
data_original_pos = [f for f in os.listdir(pos_sub_path) if f.endswith(".jpg")]
data_original_neg = [f for f in os.listdir(neg_sub_path) if f.endswith(".jpg")]
data_sklt = [f for f in os.listdir(sklt_path) if f.endswith(".jpg")]

# Data augmentation
original_path = "C:\Users\Administrateur\Downloads\data-20230124T132215Z-001.zip"
new_path = "C:\Users\Administrateur\Downloads\augmentation\data-20230124T132215Z-001.zip"
