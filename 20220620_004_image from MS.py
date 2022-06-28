import os
import matplotlib.pyplot as plt
from PIL import Image

base_dir = r'F:\icon_samples'
folders = os.listdir(base_dir)

column = 10

for folder in folders :
    folder_dir = os.path.join(base_dir, folder)
    images = os.listdir(folder_dir)
    for n, image in enumerate(images, 1) :
        image_dir = os.path.join(folder_dir, image)
        r = n % column
        if r == 1 :
            fig = plt.figure(figsize = (5,2))
        if r == 0 :
            r = column
        pil = Image.open(image_dir)
        ax = fig.add_subplot(2,column/2,r)
        ax.imshow(pil)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if r == column :
            plt.show()


