import os
from PIL import Image
import numpy as np

new_save_dir = r'C:\Users\dream\OneDrive\바탕 화면\final'
if not os.path.exists(new_save_dir) : os.mkdir(new_save_dir)

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\train_numpy_size'
folders = os.listdir(base_dir)
for n, folder in enumerate(folders) :
    save_folder_dir = os.path.join(new_save_dir, folder)
    if not os.path.exists(save_folder_dir): os.mkdir(save_folder_dir)
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    images = sorted(images)
    represent_numbers = []
    for image in images :
        represent_number = image.split('_')[0]
        if represent_number not in represent_numbers :
            image_dir = os.path.join(folder_dir, image)
            pil = Image.open(image_dir)
            new_image_save_dir = os.path.join(save_folder_dir,image)
            pil.save(new_image_save_dir)
            represent_numbers.append(represent_number)

