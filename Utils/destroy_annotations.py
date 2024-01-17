# This script is used to destroy all the annotations, and the preprocessing
# done on the images. It is used when we want to restart the preprocessing and start again from scratch.

# /!\ WARNING /!\ : This script will delete all the annotations and the preprocessing done on the images.

import os

import sys
sys.path.insert(0, '/Users/josephallyndree/Dropbox/Joseph/AgroParisTech/IODAAAAA/Projet Fil Rouge/PFR_Cirses_2022/')
 
from GLOBAL_VAR import *

for root, dirs, files in os.walk(root_data_path):
    for file in files:
        if file.startswith("Normal") or file.startswith("ExG") or file.startswith("Skeleton"):
            # deleting file
            os.remove(os.path.join(root, file))