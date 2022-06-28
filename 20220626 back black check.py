import os
import cv2
import numpy as np
from PIL import Image
# --------------------------------------------------
# 1. 이미지 기본 정보
re_dir =  r'C:\Users\dream\OneDrive\바탕 화면\valid'

base_dir = r'test'
images = os.listdir(base_dir)
for image in images:
    image_dir = os.path.join(base_dir, image)
    #image_dir = os.path.join(base_dir, image)
    #img = cv2.imread(image_dir)
    #new_dir = os.path.join(base_dir, 'RGB_'+ image)
    #cv2.imwrite(new_dir, img)
    # --------------------------------------------------
    # 2. 위치 변동
    folder_name = image.split('_')[-1].split('.')[0]
    pure_name = image.split('_')[-1]
    re_img_dir = os.path.join(re_dir, folder_name, image)
    Image.open(image_dir).save(re_img_dir)