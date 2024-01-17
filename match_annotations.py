import os
from GLOBAL_VAR import *
from pathlib import Path


# The sklt subimages
all_skeleton_subimages_path = [f for f in os.listdir("./Images/Subimages/Skeleton") if f.endswith(".jpg")]

# The ExG subimages
all_ExG_subimages_path = [f for f in os.listdir("./Images/Subimages/ExG") if f.endswith(".jpg")]


def find_corresponding_file (subimage_name :str, subimage_path_list :list):
    """
    Find the corresponding file in the list of subimages path
    Args:
        subimage_name (str): the name of the subimage
        subimage_path_list (list): the list of subimages path
    Returns:
        str: the path of the corresponding subimage
    """
    subimage_index = subimage_name.strip(".jpg").split("_")[-2:]
    search_str = "_".join(subimage_index) # the coordinate of the subimage
    for element in subimage_path_list:
        try:
            # use the index method to find the first occurrence of the substring
            index = element.index(search_str)
            # if the index method does not raise an exception, it means that the substring was present in the string
            return element
        except ValueError:
            # if the index method raises a ValueError, it means that the substring was not present in the string
            pass
    return None


for subimage in normal_subimages_whole_dir :
    cor_exg_file = find_corresponding_file(subimage, all_ExG_subimages_path)
    cor_sklt_file = find_corresponding_file(subimage, all_skeleton_subimages_path)
    
    if cor_exg_file is None or cor_sklt_file is None :
        print(subimage)
    # move the files to the correct pos or neg folder
    if subimage.split('/')[-1] in all_normal_pos_subimages_path :
        print("Pos")
        # move the files to the pos folder
        Path(f"{subimages_path}/ExG/{cor_exg_file}").rename(f"{subimages_path}/ExG/Positive/{cor_exg_file}")
        Path(f"{subimages_path}/Skeleton/{cor_sklt_file}").rename(f"{subimages_path}/Skeleton/Positive/{cor_sklt_file}")
        
    elif subimage in all_normal_neg_subimages_path :
        print("Neg")
        # move the files to the neg folder
        Path(f"{subimages_path}/ExG/{cor_exg_file}").rename(f"{subimages_path}/ExG/Negative/{cor_exg_file}")
        Path(f"{subimages_path}/Skeleton/{cor_sklt_file}").rename(f"{subimages_path}/Skeleton/Negative/{cor_sklt_file}")
        
    else :
        pass
        
        
        