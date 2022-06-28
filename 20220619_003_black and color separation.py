import os
import cv2
from PIL import Image
import numpy as np
base_dir =  dst_dir = r'G:\animal_singer\데이터셋_20220615\pixar\pil_resized'

black_base_dir =  dst_dir = r'G:\animal_singer\데이터셋_20220615\pixar\pil_resized\black'
if not os.path.exists(black_base_dir) : os.mkdir(black_base_dir)
color_base_dir =  dst_dir = r'G:\animal_singer\데이터셋_20220615\pixar\pil_resized\color'
if not os.path.exists(color_base_dir) : os.mkdir(color_base_dir)

folders = os.listdir(base_dir)
for folder in folders :
    folder_dir = os.path.join(base_dir,folder)
    images = os.listdir(folder_dir)
    for image in images :
        image_dir = os.path.join(folder_dir,image)
        # ------------------------------------------------------------------------------------------------------------------------
        # check 1
        cv_img = cv2.imread(image_dir)
        B = cv_img[:, :, 0]
        G = cv_img[:, :, 1]
        R = cv_img[:, :, 2]
        if B == G and G == R :
            cv2.imwrite(os.path.join(black_base_dir,image),cv_img)
        else :
            pil = Image.open(image_dir)
            dimension = np.array(pil).ndim
            if dimension == 2 :
                cv2.imwrite(os.path.join(black_base_dir, image), cv_img)
            else :
                cv2.imwrite(os.path.join(color_base_dir, image), cv_img)