import os
from copy import deepcopy
import cv2
import numpy as np


class Preprocessor():
    def __init__(self, image_path: str, size: tuple = (100, 100)):
        self.image = cv2.imread(image_path)
        self.original_image_size = self.image.shape
        self.image_path = image_path
        self.output_dir = "Images/Subimages"
        self.size = size
        self.image_name = os.path.splitext(os.path.basename(image_path))[0]
        self.subimages = []
        self.subimages_skeleton = []
        self.subimages_ExG = []
        # apply preprocessing steps to the image
        # create ExG image
        blue, green, red = cv2.split(self.image)
        ExG = cv2.add(cv2.multiply(green, 2), cv2.multiply(red, -1))
        ExG = cv2.add(ExG, cv2.multiply(blue, -1))
        # we need to keep a copy of the image because the thresholding function changes the image
        self.image_ExG = deepcopy(ExG)
        # create skeleton image
        _, thresh = cv2.threshold(
            ExG, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU, ExG)
        self.image_skeleton = cv2.ximgproc.thinning(thresh)
        # create a dict that links the subimages to the original image
        self.dict_preprocessing = {"Normal": {"image": self.image, "subimages": self.subimages},
                                   "ExG": {"image": self.image_ExG, "subimages": self.subimages_ExG},
                                   "Skeleton": {"image": self.image_skeleton, "subimages": self.subimages_skeleton}
                                   }

    def cut(self):
        """Method that cuts the image into subimages"""
        # getting the name of the image without the extension
        for process in self.dict_preprocessing.keys():
            if not os.path.exists(self.output_dir+"/"+process):
                os.makedirs(self.output_dir+"/"+process)

        # We iterate over the rows and columns the image and for each self.size pixel we create a subimage
        for process, dictionary in self.dict_preprocessing.items():
            for i in range(0, dictionary["image"].shape[0], self.size[0]):
                for j in range(0, dictionary["image"].shape[1], self.size[1]):
                    # we extract the subimage
                    subimage = dictionary["image"][i:i +
                                                   self.size[0], j:j+self.size[1]]
                    # if the subimage is smaller than the size, we pad it with zeros
                    if subimage.shape[0] < dictionary["image"].shape[0] or subimage.shape[1] < dictionary["image"].shape[1]:
                        subimage = cv2.copyMakeBorder(
                            subimage, 0, self.size[0]-subimage.shape[0], 0, self.size[1]-subimage.shape[1], cv2.BORDER_CONSTANT, value=0)
                    # We generate the name of the subimage, adding the coordinates of the subimage in the image
                    subimage_name = f"{process}_{self.image_name}_{i}_{j}.jpg"
                    dictionary["subimages"].append(subimage_name)

                    # Saving the subimage
                    cv2.imwrite(os.path.join(
                        self.output_dir, process, subimage_name), subimage)

    def rebuild(self, prefix: str = "", image_type="Normal"):
        """Rebuilds the image from the subimages that were created with the cut method.
        Can optionnally add a prefix to the name of the subimages

        Args:
            prefix (str, optional): prefix that must be found before the name of the subimages. Defaults to "".
            image (str, optional): image that's to be rebuilt, chosen amongst "list_preprocessing". Defaults to "Normal".

        Returns:
            matrix_image: ndarray of the rebuilt image

        """
        # on prends la liste des images
        path_list = self.dict_preprocessing[image_type]["subimages"]
        path_list = [prefix+x for x in path_list]
        # getting the dimensions of the image to be rebuilt (can be different
        # from the original image's because of the padding)
        number_of_subimage_x = int(self.original_image_size[0]/self.size[0]) if self.original_image_size[0] % self.size[0] == 0 else int(
            self.original_image_size[0]/self.size[0])+1
        number_of_subimage_y = int(self.original_image_size[1]/self.size[1]) if self.original_image_size[1] % self.size[1] == 0 else int(
            self.original_image_size[1]/self.size[1])+1
        length_image = number_of_subimage_x*(self.size[0])
        height_image = number_of_subimage_y*(self.size[1])
        # Empty matrix of size (length_image,height_image,3)
        matrix_image = np.zeros(
            (length_image, height_image, 3), dtype=np.uint8)

        # Filling the matrix with the subimages

        for file in path_list:
            subimage = cv2.imread(f"{self.output_dir}/{image_type}/{file}")
            subimage_name = os.path.splitext(os.path.basename(file))[0]
            xstart = int(subimage_name.split('_')[-1])
            ystart = int(subimage_name.split('_')[-2])
            xend = xstart+self.size[0]
            yend = ystart+self.size[1]
            matrix_image[ystart:yend, xstart:xend] = subimage
        cv2.imwrite(
            f"Images/{image_type}_{self.image_name}_{prefix}reconstruction.jpg", matrix_image)
        print(
            f"Rebuilt an image of size {matrix_image.shape} from an image of size {self.original_image_size} and subimages of size {self.size}")
        return matrix_image


if __name__ == "__main__":
    image_path = "DJI_0202.JPG"
    size = (100, 100)
    processor = Preprocessor(image_path, size)
    processor.cut()
    processor.rebuild(prefix="", image_type="Normal")
    processor.rebuild(prefix="", image_type="ExG")
    processor.rebuild(prefix="", image_type="Skeleton")
