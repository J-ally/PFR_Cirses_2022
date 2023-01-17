from change_hue import change_hue
from subimage_creation import SubimageCreator
import cv2
from random import randint

sushi = SubimageCreator("DJI_0202.JPG", size=(100, 100))
sushi.cut()
for subimage in sushi.subimages:
    path=sushi.output_dir+"/"+subimage
    img = cv2.imread(path)
    image_hued=change_hue(img,randint(10,60))
    cv2.imwrite(sushi.output_dir+"/"+"hued_"+subimage,image_hued)
sushi.rebuild("hued_")