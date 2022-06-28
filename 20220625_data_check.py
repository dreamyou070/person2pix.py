import os
from PIL import Image

new_base = r'C:\Users\dream\OneDrive\바탕 화면\dataset_name'
if not os.path.exists(new_base) : os.mkdir(new_base)

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\dataset'
folders = os.listdir(base_dir)
for folder in folders :
    new_folder_dir = os.path.join(new_base, folder)
    if not os.path.exists(new_folder_dir ): os.mkdir(new_folder_dir )
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    image_dir_dict = {}
    for image in images :
        image_dir = os.path.join(folder_dir, image)
        pil_img = Image.open(image_dir)
        shape = pil_img.size
        image_dir_dict[image_dir] = shape
    sort_size_images = sorted(image_dir_dict.items(), key = lambda x : x[1])
    for k, sort_item in enumerate(sort_size_images,1) :
        image_dir, shape = sort_item
        image_type = image_dir.split('.')[-1]
        pure_name = folder + '_' + str(k) +'.' + image_type
        new_dir = os.path.join(new_folder_dir ,pure_name)
        Image.open(image_dir).save(new_dir)

