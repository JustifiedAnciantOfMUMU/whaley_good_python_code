import os, sys, random

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done

dir = r'E:/Thesis/Datasets/230831_upsweep_spectrogram/val/'
list = os.listdir(dir)

for file in list:
    item_path = os.path.join(dir, file)
    if os.path.isfile(item_path):
        label = file[-5]
        if label == '1':
            os.rename(dir + file, dir + r'call/' + file)
        else:
            os.rename(dir + file, dir + r'no_call/' + file)

Done()
