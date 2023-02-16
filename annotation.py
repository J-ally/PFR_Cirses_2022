# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os
import shutil
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk 


###############################################################################
#                                 GLOBALS                                     #
###############################################################################

ENTRIES = [f for f in os.listdir("Images/Subimages") if f.endswith(".jpg")]
PHOTO_NAME = ENTRIES[0][:8] # The name of the photo is the first 8 characters of the first subimage

if not os.path.exists("Images/Subimages/Positive"):
    os.makedirs("Images/Subimages/Positive")
    
if not os.path.exists("Images/Subimages/Negative"):
    os.makedirs("Images/Subimages/Negative")

###############################################################################
#                                SCRIPTING                                    #
###############################################################################

def move_positive_image () :
    """
    Move the current subimage displayed to the positive folder
    Inputs : 
    Returns : calls the update_globals_and_image function
    """
    global ENTRIES
    current_subimage_name = ENTRIES[0]
    # moving the subimage to the positive folder
    Path(SUBIMAGES_PATH[0]).rename(f"Images/Subimages/Positive/{current_subimage_name}")
    print(f"Image {current_subimage_name} moved to Positive folder")
    update_globals_and_image()


def move_negative_image () :
    """
    Move the current subimage displayed to the negative folder
    Inputs : 
    Returns : calls the update_globals_and_image function
    """
    global ENTRIES
    current_subimage_name = ENTRIES[0]
    # moving the subimage to the negative folder
    Path(SUBIMAGES_PATH[0]).rename(f"Images/Subimages/Negative/{current_subimage_name}")
    print(f"Image {current_subimage_name} moved to Negative folder")

    update_globals_and_image()
    

###############################################################################
#                              WINDOW DEFINITION                              #
###############################################################################

root = Tk()
root.configure(background='white')
root.title("Annotation subimage")

SUBIMAGES_CONT = [ImageTk.PhotoImage(Image.open(f"Images/Subimages/{f}")) for f in ENTRIES]
SUBIMAGES_PATH = [f"Images/Subimages/{f}" for f in ENTRIES]

try :
    current_subimage = SUBIMAGES_CONT[0]
except IndexError :
    print("No subimages to annotate")
    exit()

# print(SUBIMAGES_CONT)

root_geometry = (250, 250)
root.geometry(f"{root_geometry[0]}x{root_geometry[1]}")
root.resizable(0, 0)

root.grid()

###############################################################################
#                              FRAMES DEFINITION                              #
###############################################################################


frame = Frame(root, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

label = Label(frame)
label.pack()
label.config(image=SUBIMAGES_CONT[0])

canvas = Canvas(frame, width = 600, height = 400)
canvas.pack(side="left", fill="both", expand="yes")

button_positive = Button(canvas, text="Negative", command = move_negative_image)
button_positive.pack(side="right")

button_negative = Button(canvas, text="Positive", command = move_positive_image)
button_negative.pack(side="right")


def update_globals_and_image () :
    """
    Updates the images and the globals
    Inputs : 
    Returns : Update ENTRIES, SUBIMAGES_PATH and SUBIMAGES_CONT list 
    """
   
    global SUBIMAGES_PATH, SUBIMAGES_CONT, ENTRIES
    
    SUBIMAGES_CONT.pop(0)
    SUBIMAGES_PATH.pop(0)
    ENTRIES.pop(0)
    
    try :
        label.config(image=SUBIMAGES_CONT[0])
    except IndexError :
        print("No more subimages to annotate")
        shutil.make_archive(f"Images/{PHOTO_NAME}_annotated", "zip", "Images")
        exit()
        
    print("Globals updated")
    pass

###############################################################################
#                                  WINDOW LOOP                                #
###############################################################################

if __name__ == '__main__' :
    root.mainloop()
    