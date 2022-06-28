import os
import cv2
from PIL import Image
import numpy as np


dst_dir = r'G:\animal_singer\데이터셋_20220615\pixar\pil_resized'
if not os.path.exists(dst_dir) : os.mkdir(dst_dir)


source = r'G:\animal_singer\데이터셋_20220615\pixar\image_collection'
folders = os.listdir(source)


for folder in folders :
    if folder != 'cat' and folder != 'dunkkey' and folder != 'pig' and folder != 'pumba' and folder != 'remy' and folder != 'simba' and folder != 'zazu ':
        print(folder)

        folder_dir = os.path.join(source, folder)
        src_images = os.listdir(folder_dir)

        folder_dst_dir = os.path.join(dst_dir, folder)
        if not os.path.exists(folder_dst_dir): os.mkdir(folder_dst_dir)



        for src_image in src_images :

            src_image_dir = os.path.join(folder_dir, src_image)

            pil_img = Image.open(src_image_dir)
            if pil_img.mode == 'RGB' :
                w,h,c = np.array(pil_img).shape
                # ------------------------------------------------------------------------
                if w > h : regular = h
                else : regular = w
                ratio = 800 / regular
                new_w = int(ratio * w)
                new_h = int(ratio * h)
                img_resize = pil_img.resize((new_h,new_w), Image.LANCZOS)
                # ------------------------------------------------------------------------
                save_dir = os.path.join(folder_dst_dir, src_image.split('.')[0] + '_pil_resize.jpg')
                img_resize.save(save_dir)