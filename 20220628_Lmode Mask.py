import os
import numpy  as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

# -------------------------------------------------------------------------
# 1. P mode 만들기
save_dir = r'F:\002_data\final_pixar_each_character_profile\model_P'
if not os.path.exists(save_dir) : os.mkdir(save_dir)
base_dir = r'F:\002_data\final_pixar_each_character_profile\model_RGB'
images = os.listdir(base_dir)
for image in images :
    image_dir = os.path.join(base_dir, image)
    pil = Image.open(image_dir)
    p_pil = pil.convert('P')
    new = os.path.join(save_dir, image)
    p_pil.save(new)

# -------------------------------------------------------------------------
# 2. Mask 만들기
save_mask_dir = r'F:\002_data\final_pixar_each_character_profile\madel_mask_test'
if not os.path.exists(save_mask_dir) : os.mkdir(save_mask_dir)
base_dir = r'F:\002_data\final_pixar_each_character_profile\model_P'
images = os.listdir(base_dir)
for image_name in images :

    new_folder = image_name.split('_')[3:][0].split('.')[0].strip()
    save_folder_dir = os.path.join(save_mask_dir, new_folder)
    if not os.path.exists(save_folder_dir): os.mkdir(save_folder_dir)

    target_img_dir = os.path.join(base_dir, image_name)
    image = cv2.imread(target_img_dir)
    image_pil = Image.open(target_img_dir)
    image_pil_np = np.array(image_pil)  # 499 * 252 = 125748

    pixel_feature = image_pil_np.reshape((-1, 1))

    height, width = image_pil_np.shape
    positions = []
    for h_index in range(height) :
        for w_index in range(width) :
            position = [h_index, w_index]
            positions.append(position)
    position_feature = np.array(positions)
    z = np.hstack((pixel_feature,position_feature))
    z = np.float32(z)
    # --------------------------------------------------------
    # 3. 색상 양자화
    cluster_nums = range(3, 12)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)
    attemp_rounds = 10
    for cluster_num in cluster_nums:
        compactness, labels, centers = cv2.kmeans(z, cluster_num, None, criteria, attemp_rounds, cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        segmentation_map = labels.reshape((height, width))
        # ------------------------------------------------------------------------------------------------------------
        # 2. 각 class 에서 해당 class 만 투명으로 만들기
        segment_vector = segmentation_map.flatten()
        segments = np.unique(segmentation_map)
        for segment in segments:
            r_channel = []
            g_channel = []
            b_channel = []
            alpha_channel = []
            for index, value in enumerate(segment_vector):
                if value == segment:
                    alpha = 255
                    r, g, b = 0, 0, 0
                else:
                    alpha = 255
                    r, g, b = 255, 255, 255
                r_channel.append(r)
                g_channel.append(g)
                b_channel.append(b)
                alpha_channel.append(alpha)
            r_channel = np.array([r_channel])
            g_channel = np.array([g_channel])
            b_channel = np.array([b_channel])
            alpha_channel = np.array([alpha_channel])
            r_channel = r_channel.reshape((height, width))
            g_channel = g_channel.reshape((height, width))
            b_channel = b_channel.reshape((height, width))
            alpha_channel = alpha_channel.reshape((height, width))
            rgba_image = np.ones(shape=(height, width, 4))
            rgba_image[:, :, 0] = r_channel
            rgba_image[:, :, 1] = g_channel
            rgba_image[:, :, 2] = b_channel
            rgba_image[:, :, 3] = alpha_channel
            rgba_image = np.uint8(rgba_image)
            rgba_pil = Image.fromarray(rgba_image)
            new_dir = os.path.join(save_folder_dir, 'test_sy' + str(segment) + '_cluster_' + str(cluster_num) + '_' +
                                   os.path.split(target_img_dir)[-1])
            rgba_pil.save(new_dir)
