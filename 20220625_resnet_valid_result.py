import os
from PIL import Image

result_file = r'C:\Users\dream\OneDrive\바탕 화면\valid_epoch_12.txt'
epoch_number = result_file.split('_')[-1].split('.')[0]

data_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\data\valid'

new_file_name = 'model_classified_epoch_' + str(epoch_number)
raw_dir = r'C:\Users\dream\OneDrive\바탕 화면'
model_classified_save_dir = os.path.join(raw_dir,new_file_name)

if not os.path.exists(model_classified_save_dir) : os.mkdir(model_classified_save_dir)
"""
with open(result_file,'r', encoding='utf-8') as f :
    contents = f.readlines()
    saved_imgs = []
    for n, line in enumerate(contents) :
        if n > 0 :
            class_number = int(line.split('\t')[0])
            model_class_dir = os.path.join(model_classified_save_dir , 'class_'+str(class_number))
            if not os.path.exists(model_class_dir): os.mkdir(model_class_dir)
            img_dir = line.split('\t')[1].split('valid')[-1].strip()[1:]
            folder = img_dir.split('/')[0]
            pure_name  = img_dir.split('/')[-1]
            valid_img_dir = os.path.join(data_base_dir,folder,pure_name)
            try :
                pil_img = Image.open(valid_img_dir)
                new_dir = os.path.join(model_class_dir,pure_name)
                pil_img.save(new_dir)
                os.remove(valid_img_dir)

            except :
                print(img_dir)
"""
folders  = os.listdir(data_base_dir)
for folder in folders:
    folder_dir = os.path.join(data_base_dir, folder)
    images = os.listdir(folder_dir)
    if len(images) == 0 :
        os.rmdir(folder_dir)
