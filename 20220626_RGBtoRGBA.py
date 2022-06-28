import os
from PIL import Image
import numpy as np
import cv2
# --------------------------------------------------------

folder = 'test'
files = os.listdir(folder)
for file in files :
    print(file)
    file_dir = os.path.join(folder, file)
    pil = Image.open(file_dir)
    if pil.mode != 'RGBA' :
        rgba_pil = pil.convert('RGBA')
        rgba_np = np.array(rgba_pil)
        R = rgba_np[:, :, 0]
        G = rgba_np[:, :, 1]
        B = rgba_np[:, :, 2]
        alpha = rgba_np[:, :, 3]
        new = np.zeros(shape = rgba_np.shape)
        RGB = rgba_np[:, :, :-1]
        sum_map = np.sum(RGB, axis=2)
        h,w = sum_map.shape
        values = set()
        for h_index in range(h) :
            for w_index in range(w) :
                value = sum_map[h_index, w_index]
                if value == 0 : # 검정색 부분
                    new[h_index, w_index, :] = [255,255,255,0]
                else :
                    new[h_index, w_index, :] = [0,0,0,255]
        new_cv = np.array(new, dtype = np.uint8)
        if 'back_white' in file :
            pure_name = '_'.join(file.split('_')[-2:])
            pure_name = 'object_empty_' + pure_name
        else :
            pure_name = '_'.join(file.split('_')[-2:])
            pure_name = 'background_empty_' + pure_name

        new_save_dir = os.path.join(folder, pure_name)
        cv2.imwrite(new_save_dir,new_cv)
"""
# --------------------------------------------------------
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\valid'
folders = os.listdir(base_dir)
for folder in folders :
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    for image in images :
        if 'RGBA_RGB_back_white' in image :
            image_dir = os.path.join(folder_dir, image)
            pil_image = Image.open(image_dir)
            pure_name = '_'.join(image.split('_')[-2:])
            pure_name = 'object_empty_' + pure_name
            pil_image.save(pure_name)
            os.remove(image_dir)
        elif 'RGBA_RGB_back_black' in image :
            image_dir = os.path.join(folder_dir, image)
            pil_image = Image.open(image_dir)
            pure_name = '_'.join(image.split('_')[-2:])
            pure_name = 'background_empty_' + pure_name
            pil_image.save(pure_name)
            os.remove(image_dir)
"""