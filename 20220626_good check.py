import os
from PIL import Image
import cv2
import numpy as np

# ------------------------------
# RGB Chaeck
base_dir = r'good'
images = os.listdir(base_dir)
for image in images :
    image_dir = os.path.join(base_dir, images[0])
    mode = Image.open(image_dir).mode
    if mode == 'RGBA' :
        rgb_pil = Image.open(image_dir).convert('RGB')
        dir = os.path.join(base_dir, 'good_model_'+image)
        rgb_pil.save(dir)


#image_dirs = [os.path.join(base_dir, image) for image in images]
#first_dir  = image_dirs[0]
#second_dir = image_dirs[1]


#save_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\final_pixar_each_character_profile\color_image\model'
#first_pil = Image.open(first_dir)
#second_pil = Image.open(second_dir)
#first_np = np.array(first_pil)
#second_np = np.array(second_pil)
#first_np = cv2.imread(first_dir)
#second_np = cv2.imread(second_dir)
#sum = cv2.add(first_np,second_np)
#cv2.imshow('sum',sum)
#cv2.imwrite('good_model_profile_koala.png',sum)
