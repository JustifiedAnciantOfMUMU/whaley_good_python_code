import matplotlib.pyplot as plt, numpy as np, PIL as image_lib, pathlib, tensorflow as tflow, numpy as np, os, sys, sklearn
from PIL import Image
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.models import Sequential, load_model, save_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.applications import ResNet50, ResNet50V2, VGG16

import matplotlib.pyplot as plt
import numpy as np, os
import keras, cv2
from keras.optimizers import adam

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done
from Config.import_config import ConfigDict

model_name = '091023_adapted_resnet50_upsweep'
epochs = 20

model = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230817_resnet50_upsweep')
model.compile(optimizer=Adam(0.0001), loss='binary_crossentropy',metrics=['accuracy'])

image_data_generator = ImageDataGenerator()
train_ds = image_data_generator.flow_from_directory(r'E:\Thesis\Datasets\230831_upsweep_spectrogram\train', target_size=(224, 224), batch_size=32, class_mode='binary', seed=123)
validation_ds = image_data_generator.flow_from_directory(r'E:\Thesis\Datasets\230831_upsweep_spectrogram\val', target_size=(224, 224), batch_size=32, class_mode='binary', seed=123)

filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + model_name
mc = ModelCheckpoint(filepath, monitor='val_accuracy', mode='max')
hs = model.fit(train_ds, validation_data=validation_ds, epochs=epochs, callbacks=[mc])

accuracy = hs.history['accuracy']
val_accuracy = hs.history['val_accuracy']

print(accuracy)
print('\n/n')
print(val_accuracy)
Done()