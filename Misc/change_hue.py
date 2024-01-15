import cv2

def change_hue(image,color=60):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:,0] = color
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image

if __name__ == '__main__':
    img = cv2.imread(r"DJI_0202\DJI_0202_0_3800.jpg")
    image_hue=change_hue(img,60)
    #cv2.imshow("Green",image_hue)
    #cv2.waitKey(0)
    cv2.imwrite(r"DJI_0202\DJI_0202_0_3800_Green.jpg",image_hue)
    