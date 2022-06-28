import os
import numpy as np
from PIL import Image
from PIL import ImageFilter
from pytesseract import *
"""
image_dir = r'./pinterest_3/miss_crawly_size_1/miss crawly_size_1_17.jpg'
cmd = '
img = Image.open(image_dir)
image_to_string(img, lang='eng')
#original_image = Image.open(image_dir)
#gray_image = original_image.convert("L")
#final = gray_image.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))
#final.show()




c_img = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)
cv2.imshow('image', c_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

threshold1 = 0
threshold2 = 360
edge_img = cv2.Canny(c_img, threshold1, threshold2)
cv2.imshow('image', edge_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(edge_img)

cv2.imwrite('sample_edge.jpg', edge_img)
"""