import os
import cv2
from PIL import Image
import numpy as np
base_dir =  r'C:\Users\dream\OneDrive\바탕 화면\animal'
folders = os.listdir(base_dir)
for folder in folders :
    folder_dir = os.path.join(base_dir,folder)
    images = os.listdir(folder_dir)
    for image in images :
        if image.endswith('json') :
            os.remove(os.path.join(folder_dir, image))