# -*- coding: utf-8 -*-
"""
Created on Jan 04 2022
@author:  jaly
"""

import os
from PIL import Image, ImageTk 
from tkinter import *
from tkinter import ttk

###############################################################################
#                              WINDOW DEFINITION                              #
###############################################################################

root = Tk()
root.configure(background='white')
root.title("Annotation subimage")
root.resizable(width=None, height=None)

root.grid()

path_image = Image.open("/Images/DJI_0202.JPG") 


###############################################################################
#                                   SCRIPTING                                 #
###############################################################################

def place_positive_image () :
    print("Je suis positive")

def place_negative_image () :
    print("Je suis negative")
    
def update_path_image () :
    pass

### Importation des images

# from PIL import Image, ImageTk 
# import  Tkinter as Tk 
# root = Tk.Tk() 

# image = Image.open("lenna.jpg") 
# photo = ImageTk.PhotoImage(image) 
 
# canvas = Tk.Canvas(root, width = image.size[0], height = image.size[1]) 
# canvas.create_image(0,0, anchor = Tk.NW, image=photo)
# canvas.pack() 
# root.mainloop()

###############################################################################
#                              FRAMES DEFINITION                              #
###############################################################################


image_frame = Frame(root, width=750, height=500)
button_positive = Button(image_frame, text="Positive", command = place_negative_image)

button_positive.pack()
button_negative = Button(image_frame, text="Negative", command = place_positive_image)
button_negative.pack()

###############################################################################
#                                  WINDOW LOOP                                #
###############################################################################

image_frame.pack()

root.mainloop()