import os
from PIL import Image
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\pixar_sing'
images = os.listdir(base_dir)
for image in images :
    pure_name = image.split('.')[0]
    img_dir = os.path.join(base_dir, image)
    folder_dir = os.path.join(base_dir,pure_name)
    os.mkdir(folder_dir)
    pil = Image.open(img_dir)
    new_name = os.path.join(folder_dir, pure_name +'_'+'1.png')
    pil.save(new_name)

