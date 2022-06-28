import numpy  as np
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
# -----------------------------------------------------------------------------------------
# 1. 이미지 데이터 자체를 불러오기
save_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\cloth_from_model'
base_dir = r'F:\001_pixar\model'
images = os.listdir(base_dir)
for image_name in images :
    new_folder = image_name.split('_')[3:][0].split('.')[0].strip()
    save_folder_dir = os.path.join(save_base_dir, new_folder)
    target_img_dir = os.path.join(base_dir, image_name)

    # --------------------------------------------------------------------------------------
    # 2.
    image = cv2.imread(target_img_dir)
    image_np = np.array(image)

    Z = image.reshape((-1, 3))
    z = np.float32(Z)
    # --------------------------------------------------------
    # 3. 색상 양자화 ------------------------
    cluster_nums = range(3,11)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)
    attemp_rounds = 10
    for cluster_num in cluster_nums :
        compactness, labels, centers = cv2.kmeans(z, cluster_num, None, criteria, attemp_rounds,cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        #print(image.shape[:2])
        segmentation_map = labels.reshape(image.shape[:2])
        # ------------------------------------------------------------------------------------------------------------
        # 1. RGB Channel 만들기
        labels = labels.flatten()
        res = centers[labels]
        quantized_image = res.reshape((image.shape))

        # ------------------------------------------------------------------------------------------------------------
        # 2. 각 class 에서 해당 class 만 투명으로 만들기
        segment_vector = segmentation_map.flatten()
        segments = np.unique(segmentation_map)

        for segment in segments :
            r_channel = []
            g_channel = []
            b_channel = []
            alpha_channel = []
            for index, value in enumerate(segment_vector) :
                if value == segment :
                    alpha = 0
                    r,g,b = 0,0,0
                else :
                    alpha = 0
                    r, g, b = 255,255,255
                r_channel.append(r)
                g_channel.append(g)
                b_channel.append(b)
                alpha_channel.append(alpha)

            r_channel     = np.array([r_channel])
            g_channel     = np.array([g_channel])
            b_channel     = np.array([b_channel])
            alpha_channel = np.array([alpha_channel])

            r_channel     = r_channel.reshape((image.shape[:2]))
            g_channel     = g_channel.reshape((image.shape[:2]))
            b_channel     = b_channel.reshape((image.shape[:2]))
            alpha_channel = alpha_channel.reshape((image.shape[:2]))
            height, width = image.shape[:2]

            rgba_image = np.ones(shape = (height, width,4))
            rgba_image[:, :, 0] = r_channel
            rgba_image[:, :, 1] = g_channel
            rgba_image[:, :, 2] = b_channel
            rgba_image[:, :, 3] = alpha_channel
            rgba_image = np.uint8(rgba_image)
            rgba_pil = Image.fromarray(rgba_image)

            new_dir = os.path.join(save_folder_dir, 'test_sy' + str(segment) + '_cluster_'+str(cluster_num)+'_' + os.path.split(target_img_dir)[-1] )
            rgba_pil.save(new_dir)
