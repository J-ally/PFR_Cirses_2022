# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk 


###############################################################################
#                                 GLOBALS                                     #
###############################################################################

ENTRIES = [f for f in os.listdir("Images/Subimages") if f.endswith(".jpg")]
SUBIMAGE_PATH = f"Images/Subimages/{ENTRIES[0]}"

###############################################################################
#                                SCRIPTING                                    #
###############################################################################


def update_globals () :
    global SUBIMAGE_PATH
    
    subimage_name = ENTRIES[0]
    SUBIMAGE_PATH = f"Images/Subimages/{subimage_name}"
    
    ##### Still have to update the canvas with the new subimage !!
    pass


def move_positive_image () :
    """
    Move the current subimage displayed to the positive folder
    Inputs : 
    Returns : Update ENTRIES list and the path of the subimage
    """
    global ENTRIES
    current_subimage_name = ENTRIES[0]
    # moving the subimage to the positive folder
    Path(SUBIMAGE_PATH).rename(f"Images/Subimages/Positive/{current_subimage_name}")
    print(f"Image {current_subimage_name} moved to Positive folder")
    
    # removing the subimage from the list
    ENTRIES.pop(0)
    update_globals()
    print("Globals updated")

def move_negative_image () :
    global ENTRIES
    current_subimage_name = ENTRIES[0]
    # moving the subimage to the negative folder
    Path(SUBIMAGE_PATH).rename(f"Images/Subimages/Negative/{current_subimage_name}")
    print(f"Image {current_subimage_name} moved to Negative folder")
    
    # removing the subimage from the list
    ENTRIES.pop(0)
    update_globals()
    print("Globals updated")
    

###############################################################################
#                              WINDOW DEFINITION                              #
###############################################################################

root = Tk()
root.configure(background='white')
root.title("Annotation subimage")

image = Image.open(SUBIMAGE_PATH) 
photo = ImageTk.PhotoImage(image) 

root_geometry = (image.size[0]+150, image.size[1])
root.geometry(f"{root_geometry[0]}x{root_geometry[1]}")
root.resizable(0, 0)

root.grid()

###############################################################################
#                              FRAMES DEFINITION                              #
###############################################################################

canvas = Canvas(root, width = image.size[0], height = image.size[1])
canvas.pack(side="left", fill="both", expand="yes")
canvas.create_image(0,0, anchor = NW, image=photo)

button_positive = Button(canvas, text="Negative", command = move_negative_image)
button_positive.pack(side="right")

button_negative = Button(canvas, text="Positive", command = move_positive_image)
button_negative.pack(side="right")

###############################################################################
#                                  WINDOW LOOP                                #
###############################################################################

root.mainloop()