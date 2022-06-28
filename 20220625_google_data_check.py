# 1.라이브러리
import torch
from torch.utils.data import Dataset
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torchvision
from torchvision.io import read_image
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import numpy as np
import time, os, copy
from PIL import Image
from datetime import datetime
from pytz import timezone
import shutil
# ------------------------------------------------------------------------------------------------------------------------
def get_time () :
    now = datetime.now(timezone('Asia/Seoul'))
    date = str(now).split(' ')[0]
    hour = str(now).split(' ')[1].split(':')[:-1][0]
    min = str(now).split(' ')[1].split(':')[:-1][1]
    time = str(hour) + ' : ' + str(min)
    return date +' / ' + time
# ------------------------------------------------------------------------------------------------------------------------
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\valid'

temp_dir = r'C:\Users\dream\OneDrive\바탕 화면\temp'
if not os.path.exists(temp_dir) : os.mkdir(temp_dir)
P_dir = r'C:\Users\dream\OneDrive\바탕 화면\temp\P'
if not os.path.exists(P_dir) : os.mkdir(P_dir)
L_dir = r'C:\Users\dream\OneDrive\바탕 화면\temp\L'
if not os.path.exists(L_dir) : os.mkdir(L_dir)
RGBA_dir = r'C:\Users\dream\OneDrive\바탕 화면\temp\RGBA'
if not os.path.exists(RGBA_dir) : os.mkdir(RGBA_dir)

def get_image (dir) :
    P_mode_files = []
    L_mode_files = []
    RGBA_mode_files = []
    mode_dict = {}
    folders = os.listdir(dir)
    for folder in folders :
        folder_dir = os.path.join(dir, folder)
        images = os.listdir(folder_dir)
        for image_name in images :
            image_dir = os.path.join(folder_dir, image_name)
            pil = Image.open(image_dir)
            mode = pil.mode
            if mode == 'P':
                P_mode_files.append(image_dir)
                new_dir = os.path.join(P_dir,image_name)
                pil.save(new_dir)
            if mode == 'L':
                L_mode_files.append(image_dir)
                new_dir = os.path.join(L_dir,image_name)
                pil.save(new_dir)
            if mode == 'RGBA':
                RGBA_mode_files.append(image_dir)
                new_dir = os.path.join(RGBA_dir,image_name)
                pil.save(new_dir)
    for P_mode_file in P_mode_files :
        os.remove(P_mode_file)
    for L_mode_file in L_mode_files :
        os.remove(L_mode_file)
    for RGBA_mode_file in RGBA_mode_files :
        os.remove(RGBA_mode_file)
get_image (base_dir)


#temporary_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\temporary'
#temporary_rgb_base_dir = r'C:\Users\dream\OneDrive\바탕 화면\temporary_rgb'
#if not os.path.exists(temporary_rgb_base_dir) :  os.mkdir(temporary_rgb_base_dir)
#RGBA2RBG(temporary_base_dir)



# ---------------------------------------------------------- RGBA 파일 확인하기
def check_rgba (dir, phase) :
    removes = []
    folders = os.listdir(dir)
    for folder in folders :
        folder_dir = os.path.join(dir, folder)
        images = os.listdir(folder_dir)
        for image_name in images :
            image_dir = os.path.join(folder_dir, image_name)
            pil = Image.open(image_dir)
            mode = pil.mode
            if mode == 'RGBA':
                # ------------------------------------------------------------------------------------------
                # 1. 임시로 저장해 두기
                print(image_dir)
                temporary_folder_dir =  os.path.join(temporary_base_dir, folder)
                if not os.path.exists(temporary_folder_dir) : os.mkdir(temporary_folder_dir)
                new_image_dir = os.path.join(temporary_folder_dir, image_name)
                pil.save(new_image_dir)
                # ------------------------------------------------------------------------------------------
                # 2. 버릴 것 저장하기
                removes.append(image_dir)
    for remove_file in removes :
        os.remove(remove_file)
    return removes

# ---------------------------------------------------------- RGB 로 변환시켜 보기
def RGBA2RBG (dir) :
    folders = os.listdir(dir)
    for folder in folders :
        folder_dir = os.path.join(dir, folder)
        images = os.listdir(folder_dir)
        for image in images :
            image_dir = os.path.join(folder_dir,image)
            rgba_pil_image = Image.open(image_dir)
            rgb_pil_image  = rgba_pil_image.convert('RGB')

            rgb_folder_dir = os.path.join(temporary_rgb_base_dir, folder)
            if not os.path.exists(rgb_folder_dir) :  os.mkdir(rgb_folder_dir)
            rgb_image_dir = os.path.join(rgb_folder_dir,image)
            rgb_pil_image.save(rgb_image_dir)




