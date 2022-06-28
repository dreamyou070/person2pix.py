import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

files = os.listdir(r'./')
for file in files :
    if 'png' in file : img_dir1 = file
    elif 'jpg' in file : img_dir2 = file

pil_image1 = Image.open(img_dir1)
background_black = np.zeros(np.array(pil_image1).shape)
alpha_channel = (np.array(pil_image1)[:,:,-1] / 255)
background_black[:,:,0] = alpha_channel
background_black[:,:,1] = alpha_channel
background_black[:,:,2] = alpha_channel
background_black = np.array(background_black[:,:,:-1] , dtype = np.uint8)
background_black = background_black # * 255

#mask = background_black
pil_image1 = Image.open(img_dir1)
background_white = np.zeros(np.array(pil_image1).shape)
alpha_channel = 1 - (np.array(pil_image1)[:,:,-1] / 255)
background_white[:,:,0] = alpha_channel
background_white[:,:,1] = alpha_channel
background_white[:,:,2] = alpha_channel
background_white = np.array(background_white[:,:,:-1] , dtype = np.uint8)
background_white = background_white * 255
mask = background_white


#################################
####### SRC 이미지 ###############
#################################
pil_image2 = Image.open(img_dir2).convert("RGB")
src = np.array(pil_image2)
print(src.shape)
print(background_white.shape)
new = cv2.add(src,background_white)
new = np.array(new, dtype = np.uint8)
pil_new = Image.fromarray(new)

# -----------------------------
#

pil_new.save('new_' + img_dir1)
pil_new.save('new_' + img_dir2)