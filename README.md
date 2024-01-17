# PFR_Cirses_2022

Cirses are herbaceous plants, biennial or perennial, belonging to the family Asteraceae (or Compositae) and the genus Cirsium. Cirsium arvense, known as Canada thistle or Field thistle, is a very common species in Europe. It is a weed of most crops and meadows. It multiplies quickly by its numerous seeds which, thanks to their egrets, can be disseminated at great distance.

The problem we are trying to solve is thus to know how to detect in the various affected zones and the intensity of the invasion by the thistle on these zones; and what is their kinetics of propagation on the scale of the whole of the considered fields.

To answer this question, we will be analyzing the images taken by a drone.

## Files and folders gestion

In order for the repo to work correctly, you must follow the following rules:
 - The folders architecture must be respected :
    - The folder `Images` (created in `[subimage_creation.py](https://github.com/J-ally/PFR_Cirses_2022/blob/main/subimage_creation.py)`) must contain the data files = images taken with the drone
    - The folder `Images/Subimages`(created in [annotation.py](https://github.com/J-ally/PFR_Cirses_2022/blob/main/annotation.py)) will contain the segmentated images (segmented with the script [subimage_creation.py](https://github.com/J-ally/PFR_Cirses_2022/blob/main/subimage_creation.py))
    - The folders `Images/Subimages/Negative` must contain the negative subimages -not containing cirses- (annotated with the script [annotation.py](https://github.com/J-ally/PFR_Cirses_2022/blob/main/annotation.py))
    - The folders `Images/Subimages/Positive` must contain the positive subimages -ontaining cirses-  (annotated with the script [annotation.py](https://github.com/J-ally/PFR_Cirses_2022/blob/main/annotation.py))

 - Images must be in the format `.jpg`

## Steps

0) Place the Images you want to annotate in the `Images` folder
1) Modify and Run the `GLOBAL_VAR.py` script to adapt all the paths of the repo.
2) Run the `preprocesing.py` script. It will create the folders and the subimages for each type of preprocessing applied to the images.
3) Run the `annotation.py` script to annotate the subimages present in the `Images/Normal/Subimages` folder into positive (presence of cirses) or negative (absence of cirses)
4) Run the `match_annotations.py`, it will match the annotations made on the Normal images for the other preprocesses (Excess Green and Skeletonization)

# Contact Us

- [Joseph Allyndrée](mailto:joseph.allyndree@agroparistech.fr)
- [Norat Picaut](mailto:nora.picaut@agroparistech.fr)
- [Amine Kabeche](mailto:amine.kabeche@agroparistech.fr)
- [Delpierot Augustin](mailto:delpierot.augustin@agroparistech.fr)