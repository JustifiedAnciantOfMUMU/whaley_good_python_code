# Loading all necessary libraries and modules
import os, sys, numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from matplotlib import gridspec

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input
from keras.callbacks import ModelCheckpoint

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict

def convert_file(folder_path, file, sub_folder):
    img = cv.imread(folder_path + sub_folder + '/' + file)
    processed_img = preprocess_input(img)
    processed_img = np.expand_dims(processed_img, axis=0)
    
    features = model.predict(processed_img)
    filepath = config_dict['resnet50_features_from_kiresbom'] + sub_folder + file[:-4] + '.npy'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.save(filepath, features)
    #print(features)

def convert_folder(folder_path, sub_folder):
    file_list = os.listdir(folder_path + sub_folder)
    for file in file_list:
        convert_file(folder_path, file, sub_folder)


config_dict = ConfigDict().dict
model = ResNet50(weights = 'imagenet', include_top = False)
convert_folder(config_dict['dataset_from_kiresbom'], '/call/')
convert_folder(config_dict['dataset_from_kiresbom'], '/no_call/')
