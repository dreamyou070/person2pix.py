import os
from PIL import Image

base_dir2 = r'C:\Users\dream\OneDrive\바탕 화면\final2'
if not os.path.exists(base_dir2) : os.mkdir(base_dir2)

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\final'
folders = os.listdir(base_dir)
for folder in folders :
    folder_dir2 = os.path.join(base_dir2, folder)
    if not os.path.exists(folder_dir2): os.mkdir(folder_dir2)

    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    images = sorted(images)
    for n, image in enumerate(images, 1) :
        image_dir = os.path.join(folder_dir, image)
        image_type = image.split('.')[-1]
        new_pure_name = folder + '_' + str(n) + '.' + image_type
        new_image_dir = os.path.join(folder_dir2,new_pure_name)

        pil = Image.open(image_dir)
        pil.save(new_image_dir)

