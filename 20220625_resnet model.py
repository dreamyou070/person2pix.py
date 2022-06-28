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
# ------------------------------------------------------------------------------------------------------------------------
def get_time () :
    now = datetime.now(timezone('Asia/Seoul'))
    date = str(now).split(' ')[0]
    hour = str(now).split(' ')[1].split(':')[:-1][0]
    min = str(now).split(' ')[1].split(':')[:-1][1]
    time = str(hour) + ' : ' + str(min)
    return date +' / ' + time
# ------------------------------------------------------------------------------------------------------------------------
# 2.
base_dir = r'C:\Users\dream\OneDrive\바탕 화면\data'
# ------------------------------------------------------------------------------------------------------------------------
# 3. datset 및 Loader
class Icon_Dataset(torch.utils.data.Dataset):
    def __init__(self, image_base_dir, transform=None):
        self.image_base_dir = image_base_dir
        self.transform = transform
        folders = os.listdir(self.image_base_dir)
        lst_input = []
        image_dirs = []
        annotation_dirs = []
        class_list = []
        for folder in folders:
            class_list.append(folder)
            image_folder_dir = os.path.join(self.image_base_dir, folder)
            images = os.listdir(image_folder_dir)
            for image in images:
                image_dir = os.path.join(image_folder_dir,image)
                image_dirs.append(image_dir)
                lst_input.append(image)
        class_list = sorted(class_list)
        class_dic = {}
        for k, name in enumerate(class_list) :
            class_dic[name] = k
        self.class_dic = class_dic
        self.lst_input = lst_input
        self.image_dirs = image_dirs
        self.transform = transform
    def __len__(self):
        return len(self.lst_input)
    def __getitem__(self, idx):
        file_name = self.lst_input[idx]
        image_dir = self.image_dirs[idx]
        class_name = image_dir.split('\\')[-2]
        class_num = int(self.class_dic[class_name])
        image = read_image(image_dir)
        image = image / 255
        if self.transform:
            image = self.transform(image)
        data = {'input': image, 'file_name': file_name, 'class_num': class_num, 'image_dir' : image_dir}
        return data
# ----------------------------------------------------------------------------------------------------------------------------------------------------
train_dir = os.path.join(base_dir, 'train')
valid_dir = os.path.join(base_dir, 'valid')
data_transforms = {'train': transforms.Compose([transforms.RandomResizedCrop(224),transforms.RandomHorizontalFlip(),   transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])    ]),
                   'valid': transforms.Compose([  transforms.Resize(256),   transforms.CenterCrop(224),   transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])    ]),}
train_dataset = Icon_Dataset (image_base_dir =train_dir , transform=data_transforms['train'])
valid_dataset = Icon_Dataset (image_base_dir =valid_dir , transform=data_transforms['valid'])
image_datasets = {'train' : train_dataset, 'valid' : valid_dataset}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,num_workers=4)  for x in ['train', 'valid']}
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
dataloaders = {'train' : train_loader, 'valid' : valid_loader}
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
class_numbers = len(train_dataset.class_dic)
# ----------------------------------------------------------------------------------------------------------------------------------------------------
result_base_dir = r'F:/001_pixar/result_datas'
if not os.path.exists(result_base_dir) : os.makedirs(result_base_dir)
saved_model_base_dir = r'F:/001_pixar/model_results'
if not os.path.exists(saved_model_base_dir) : os.makedirs(saved_model_base_dir)
num_epoch = 15
if __name__ == '__main__':
    def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
        since = time.time() # 시간을 초로 환산한 것
        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0
        for epoch in range(1, num_epoch +1) :
            print('EPOCH : %2d/%2d  |  TIME : '%(epoch,num_epoch),get_time())
            for phase in ['train','valid'] :
                print('Phase : %s  |  TIME : ' % (phase), get_time())
                # ---------------------------------------------------------------------------- 파일은 valid 인 경우에만 만든다.
                if phase == 'valid' :
                    image_name_list = []
                    pred_class_num_list = []
                if phase == 'train' :  model.train()
                else : model.eval()
                running_loss = 0.0
                running_corrects = 0
                # -------------------------------------------------------------------------------------------------------------------
                # data = {'input': input, 'file_name': file_name, 'class_num': class_num}
                for batch_index, data in enumerate(dataloaders[phase],1) :
                    inputs     = data['input'].to(device)
                    labels     = data['class_num'].to(device)
                    if phase == 'valid' :
                        image_dirs  = data['image_dir']
                        for idir in image_dirs : image_name_list.append(idir)
                    optimizer.zero_grad()
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, pred_class_nums = torch.max(outputs, 1)
                        if phase == 'valid' :
                            pred_class_nums = pred_class_nums.numpy()
                            for pred_class_num in pred_class_nums :
                                pred_class_num_list.append(int(pred_class_num))
                        loss = criterion(outputs, labels)
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(pred_class_nums == labels.data)

                if phase == 'valid' :
                    file = 'valid_epoch_' + str(epoch) + '.txt'
                    text_phase_dir = os.path.join(result_base_dir, file)
                    with open(text_phase_dir, 'w') as file :
                        for image_name, class_num in zip(image_name_list,pred_class_num_list) :
                            file.write(image_name + '\t' + class_num + '\n')


                if phase == 'train':
                    scheduler.step()
                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects / dataset_sizes[phase]
                print(f'           {phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
                # deep copy the model
                if phase == 'valid' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
                    model.load_state_dict(best_model_wts)
                    model_name = 'resnet101_epoch_' + str(epoch) + '_.pt'
                    model_save_path = os.path.join(saved_model_base_dir, model_name)
                    torch.save(model.state_dict(), model_save_path)
            print()
        time_elapsed = time.time() - since
        print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        print(f'Best val Acc: {best_acc:4f}')
        # load best model weights
        model.load_state_dict(best_model_wts)
        return model









    ## 그 밖의 부수적인 variable
    num_data_train = len(train_dataset)
    num_batch_train = np.ceil(num_data_train / batch_size)
    num_data_valid = len(valid_dataset)
    num_batch_valid = np.ceil(num_data_valid / batch_size)
    dataset_sizes = { 'train' : num_data_train, 'valid' : num_data_valid }
    # ------------------------------------------------------------------------------------------------------------------
    ## 그 밖의 부수적인 variable
    fn_tonumpy = lambda x : x.to('cpu').detach().numpy()#.transpose(0,2,3,1)
    ## summary writer
# ------------------------------------------------------------------------------------------------------------------
    model_ft = models.resnet101(pretrained=True)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, class_numbers)
    model_ft = model_ft.to(device)
    criterion = nn.CrossEntropyLoss()
    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)
    model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,num_epochs=num_epoch)

















