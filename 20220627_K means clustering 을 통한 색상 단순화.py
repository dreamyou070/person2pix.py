import numpy  as np
import cv2
import matplotlib.pyplot as plt
import os
# --------------------------------------------------------
# 1. 이미지 데이터 자체를 불러오기
save_base_dir = r'F:\001_pixar\quantized'
if not os.path.exists(save_base_dir) : os.mkdir(save_base_dir)
base_dir = r'F:\001_pixar\model'

images = os.listdir(base_dir)
for image_name in images :
    new_folder = image_name.split('_')[3:][0].split('.')[0].strip()
    save_folder_dir = os.path.join(save_base_dir, new_folder)

    if not os.path.exists(save_folder_dir) :
        os.mkdir(save_folder_dir)

    target_img_dir = os.path.join(base_dir, image_name)
    image = cv2.imread(target_img_dir)
    # --------------------------------------------------------
    # 2. 히스토그램을 그려서 이미지 확인하기
    height, width = image.shape[:2]
    R = image[:,:,0]
    R_ = R.reshape((-1,1))
    G = image[:,:,1]
    G_ = G.reshape((-1,1))
    B = image[:,:,2]
    B_ = B.reshape((-1,1))
    z = np.hstack((R_,G_,B_))
    z = np.float32(z)

    # --------------------------------------------------------
    # 3. 색상 양자화 ------------------------
    cluster_nums = range(2,21)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)
    attemp_rounds = 10

    for cluster_num in cluster_nums :
        compactness, labels, centers = cv2.kmeans(z, cluster_num, None, criteria, attemp_rounds,cv2.KMEANS_PP_CENTERS)
        centers = np.uint8(centers)
        labels = labels.flatten()
        res = centers[labels]
        quantized_image = res.reshape((image.shape))
        new_dir = os.path.join(save_folder_dir, 'cluster_'+str(cluster_num)+'_' + os.path.split(target_img_dir)[-1] )
        cv2.imwrite(new_dir, quantized_image)
