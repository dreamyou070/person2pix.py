# 1차 filtering : . P mode 를 통해서 1차 필터링
# 2차 filtering : Face Detection

import dlib, cv2, os
import imutils
from imutils import face_utils
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
"""
# ----------------------------------------------------------------------------------------------------
dog_detector  = dlib.cnn_face_detection_model_v1('dogHeadDetector.dat')
face_detector = dlib.get_frontal_face_detector()


# ----------------------------------------------------------------------------------------------------
new_image_dir = r'F:\2_Pixar_Dog'
if not os.path.exists(new_image_dir) : os.mkdir(new_image_dir)
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
image_dir = r'F:\data_type_pixar_sing'
folders = os.listdir(image_dir)
for folder in folders :
    folder_dir = os.path.join(image_dir, folder)
    images = os.listdir(folder_dir)
    for img in images :
        img_dir = os.path.join(folder_dir,img)
        cv2_img = cv2.imread(img_dir)
        face = dog_detector(cv2_img)
        if len(face) > 0 :
            print(len(face))
            pil_img = Image.open(img_dir)
            new = os.path.join(new_image_dir, img)
            pil_img.save(new)
            #os.remove(img_dir)
"""