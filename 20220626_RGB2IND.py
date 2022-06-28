import os
import cv2
import numpy as np
from PIL import Image

base_dir = r'model'
images = os.listdir(base_dir)
theta = 15
for image in images :

    image_dir = os.path.join(base_dir, image)
    pil = Image.open(image_dir)
    pil_np = np.array(pil)
    height, width, channel = pil_np.shape
    R = pil_np[:, :, 0]
    G = pil_np[:, :, 1]
    B = pil_np[:, :, 2]

    mask = np.ones(shape = (height, width, 4)) * 255
    mask[:, :, 0] = R
    mask[:, :, 1] = G
    mask[:, :, 2] = B

    bgr = cv2.imread(image_dir, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    blue_range = cv2.inRange(hsv, (15 - theta, 0,0), (15 + theta, 255,255))
    blue_mask = cv2.bitwise_and(bgr,bgr,mask = blue_range)
    blue_mask = blue_mask[:,:,::-1]

    new = pil_np - blue_mask
    Image.fromarray(new).show()
    #Image.fromarray(blue_mask).show()