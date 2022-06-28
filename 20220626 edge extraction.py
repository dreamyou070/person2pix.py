# 1. 가우시안 블러를 통한 노이즈 제거
# 2. 소벨 커널을 이용하여 1차 미분 이미지를 얻는다. : 수직선과 수평선 검출
# 3. non maximum suppression
# 4. hysteresis thresholding : high threshold : low threshold = 3 : 1 혹은 2 : 1

import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

img_dir = r'F:\002_data\final_pixar_each_character_profile\model_'
images = os.listdir(img_dir)
low_threshold = 0
high_threshold = 500

save_dir = r'F:\002_data\model_edges_' + str(low_threshold) + '_' + str(high_threshold)
if not os.path.exists(save_dir) : os.mkdir(save_dir)

for image_name in images :
    image_dir = os.path.join(img_dir, image_name)
    img = cv2.imread(image_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edge = cv2.Canny(gray, low_threshold, high_threshold)
    reverse = 255 - edge
    reverse_pil = Image.fromarray(reverse)
    reverse_pil = reverse_pil.convert('RGBA')

    # ---------------------------------------------------------------------------------------------------------------------------
    reverse_np = np.array(reverse_pil)
    R = reverse_np[:, :, 0]
    G = reverse_np[:, :, 1]
    B = reverse_np[:, :, 2]
    alpha_channel = reverse_np[:,:,3]

    check1 = np.array_equiv(R, G)
    check2 = np.array_equiv(G, B)
    check3 = np.array_equiv(B, R)

    new_alpha_channel = np.zeros(shape = alpha_channel.shape)
    for row_idx, row in enumerate(alpha_channel) :
        row_list = R[row_idx].tolist()
        if 0 in row_list :
            first_index = row_list.index(0)
            reverse_list = row_list[::-1]
            last_index =
            #for #col_idx, col in enumerate(row):
        #    position = (row_idx, col_idx)
        #    if R[row_idx, col_idx] == 0 : # edge
         #       new_alpha_channel[row_idx, col_idx] = 255
        #    else :
          #      new_alpha_channel[row_idx, col_idx] = 0
    #reverse_np[:, :, 3] = new_alpha_channel
    #frame = Image.fromarray(reverse_np)
    ##new_dir = os.path.join(save_dir, 'frame_'+ image_name)
    #frame.save(new_dir)