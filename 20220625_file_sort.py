import os
from PIL import Image
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\data\train'
folders = os.listdir(base_dir)
size_dict = {}
for folder in folders :
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    for image in images :
        image_dir = os.path.join(folder_dir,image)
        pil_image = Image.open(image_dir)
        size = pil_image.size
        try :
            size_dict[size] += 1
        except :
            size_dict[size] = 1
size_dict = sorted(size_dict.items(), key = lambda x : x[0])
print(size_dict)
# 다양한 사이즈가 있고 가장 작은 것은 길이가 100 인 것이다.