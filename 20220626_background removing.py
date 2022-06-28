from PIL import Image
import numpy as np
import os
# --------------------------------------------------
# 1. 이미지 기본 정보
base_dir =  r'C:\Users\dream\OneDrive\바탕 화면\valid'
folders = os.listdir(base_dir)
for folder in folders :
    if folder == 'gorilla' :
        folder_dir = os.path.join(base_dir, folder)
        images = os.listdir(folder_dir)
        if len(images) > 0 :
            print(folder)
            for image in images :
                image_dir = os.path.join(folder_dir, image)
                pil_img = Image.open(image_dir)
                print(pil_img.mode)

    
                if pil_img.mode == 'RGBA' :
                    np_img = np.array(pil_img)
                    alpha = np_img[:, :, 3]
    
                    back_black = alpha / 255
                    back_black = np.array(back_black, dtype = np.uint8) * 255
    
                    back_white = 255 - alpha
    
                    back_black_pil = Image.fromarray(back_black)
                    dir1 = os.path.join(folder_dir, 'back_black_' + image)
                    back_black_pil.save(dir1)
                    
                    back_white_pil = Image.fromarray(back_white)
                    dir2 = os.path.join(folder_dir, 'back_white_' + image)
                    back_white_pil.save(dir2)


