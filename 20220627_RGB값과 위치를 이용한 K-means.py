import numpy  as np
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
# --------------------------------------------------------
# 1. 이미지 데이터 자체를 불러오기
save_base_dir = r'F:\001_pixar\quantized'
if not os.path.exists(save_base_dir) : os.mkdir(save_base_dir)
base_dir = r'F:\001_pixar\model'
images = os.listdir(base_dir)
for image_name in images :
    print(image_name)
    new_folder = image_name.split('_')[3:][0].split('.')[0].strip()
    save_folder_dir = os.path.join(save_base_dir, new_folder)

    target_img_dir = os.path.join(base_dir, image_name)
    image = cv2.imread(target_img_dir)
    # --------------------------------------------------------
    # 2. 히스토그램을 그려서 이미지 확인하기
    #height, width = image.shape[:2]
    #pixels = []
    #for h_index in range(height) :
    #    for w_index in range(width) :
    #        pixel = image[h_index,w_index, :].tolist()
    #        pixel.append(h_index)
    #        pixel.append(w_index)
    #        pixels.append(pixel)

    #pixels = np.array(pixels).reshape(-1,5)
    image = image.reshape((-1,3))
    z = np.float32(image)
    #z = np.float32(pixels)

    #R = image[:,:,0]
    #R_ = R.reshape((-1,1))
    #G = image[:,:,1]
    #G_ = G.reshape((-1,1))
    #B = image[:,:,2]
    #B_ = B.reshape((-1,1))
    #z = np.hstack((R_,G_,B_))
    #z = np.float32(z)

    # --------------------------------------------------------
    # 3. 색상 양자화 ------------------------
    cluster_nums = range(10,11)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)
    attemp_rounds = 10
    for cluster_num in cluster_nums :
        compactness, labels, centers = cv2.kmeans(z, cluster_num, None, criteria, attemp_rounds,cv2.KMEANS_PP_CENTERS)

        centers = np.uint8(centers)
        #segmentation_map = labels.reshape((height, width))
        # ------------------------------------------------------------------------------------------------------------
        # 1. RGB Channel 만들기
        labels = labels.flatten()
        res = centers[labels]
        quantized_image = res.reshape((image.shape))
        cv2.imshow('quantized_image',quantized_image)
        cv2.waitKey(0)
        break
        # ------------------------------------------------------------------------------------------------------------
        # 2. 각 class 에서 해당 class 만 투명으로 만들기
        #segment_vector = segmentation_map.flatten()
        #segments = np.unique(segmentation_map)

        #for segment in segments :
        #    r_channel = []
        #    g_channel = []
        #    b_channel = []
        #    alpha_channel = []
        #    for index, value in enumerate(segment_vector) :
        #        if value == segment :
        #            alpha = 0
        #            r,g,b = 0,0,0
        #        else :
        #            alpha = 255
        #            r, g, b = 0,0,0
        #        r_channel.append(r)
        #        g_channel.append(g)
        #        b_channel.append(b)
        #        alpha_channel.append(alpha)

        #    r_channel     = np.array([r_channel])
        #    g_channel     = np.array([g_channel])
        #    b_channel     = np.array([b_channel])
        #    alpha_channel = np.array([alpha_channel])

        #    r_channel     = r_channel.reshape((image.shape[:2]))
        #    g_channel     = g_channel.reshape((image.shape[:2]))
        #    b_channel     = b_channel.reshape((image.shape[:2]))
        #    alpha_channel = alpha_channel.reshape((image.shape[:2]))

        #    rgba_image = np.ones(shape = (height, width,4))
        #    rgba_image[:, :, 0] = r_channel
        #    rgba_image[:, :, 1] = g_channel
        #    rgba_image[:, :, 2] = b_channel
        #    rgba_image[:, :, 3] = alpha_channel
        #    rgba_image = np.uint8(rgba_image)
        #    rgba_pil = Image.fromarray(rgba_image)
        #    new_dir = os.path.join(save_folder_dir, 'all_black_multi_mask_' + str(segment) + '_cluster_'+str(cluster_num)+'_' + os.path.split(target_img_dir)[-1] )
        #    rgba_pil.save(new_dir)
