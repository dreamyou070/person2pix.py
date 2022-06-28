import os
import cv2
from PIL import Image
import numpy as np
"""
base = 'test'
folders = os.listdir(base)
for folder in folders :
    folder_dir = os.path.join(base, folder)
    files = os.listdir(folder_dir)
    for file in files :
        if file.startswith('object') :
            file_dir = os.path.join(folder_dir, file)
            os.remove(file_dir)

base = 'test'
folders = os.listdir(base)
for folder in folders:
    folder_dir = os.path.join(base, folder)
    images = os.listdir(folder_dir)
    for image in images :
        if image.startswith('background') :
            new_name = '_'.join(image.split('_')[-2:])
            new_dir = os.path.join(folder_dir, new_name)
    images = os.listdir(folder_dir)
    for image in images :
        if image.startswith('test') :
            image_dir = os.path.join(folder_dir, image)
            pil = Image.open(image_dir)
            pil.save(new_dir)
            os.remove(image_dir)
"""
base = 'test'
folders = os.listdir(base)
for folder in folders:
    folder_dir = os.path.join(base, folder)
    images = os.listdir(folder_dir)
    for image in images :
        if image.startswith('profile') :
            image_dir = os.path.join(folder_dir, image)
            pil = Image.open(image_dir)
            pil.convert('P').show()

            #image_dir = os.path.join(folder_dir, image)
            #os.remove(image_dir)
    #image_dirs = [os.path.join(folder_dir, image) for image in images]
    # --------------------------------------------------------------------------------
#    first = cv2.imread(image_dirs[0])
#    second = cv2.imread(image_dirs[1])
#    result = cv2.add(first, second, dtype=cv2.CV_8U)
#    print(result.shape)
#    cv2.imshow('result', result)
#    cv2.waitKey(0)
    # --------------------------------------------------------------------------------
   # first = Image.open(image_dirs[0])
   # second = Image.open(image_dirs[1])
   # first_array = np.array(first)
   # second_array = np.array(second)
   # sum = first_array + second_array
   # new_dir = os.path.join(folder_dir, 'test.png')
   # Image.fromarray(sum).save(new_dir)
