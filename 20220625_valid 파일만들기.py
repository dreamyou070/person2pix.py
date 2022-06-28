import os
from PIL import Image

base_dir = r'C:\Users\dream\OneDrive\바탕 화면\final_pixar_each_character'
new_dir =  r'C:\Users\dream\OneDrive\바탕 화면\valid'

folders = os.listdir(base_dir)
for folder in folders :
    new_folder_dir = os.path.join(new_dir, folder)
    os.mkdir(new_folder_dir)