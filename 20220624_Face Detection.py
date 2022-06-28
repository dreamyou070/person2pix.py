import cmake
import dlib
import os
from PIL import Image
import cv2

face_detector = dlib.get_frontal_face_detector( )

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\cropped_goole'

folders = os.listdir(base_dir)
for folder in folders :
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    for image in images :
        image_dir = os.path.join(folder_dir, image)
        cv2_image = cv2.imread(image_dir)
        faces = face_detector(cv2_image)

        #face = facedetector(cv2_image)
        #print(len(face))

