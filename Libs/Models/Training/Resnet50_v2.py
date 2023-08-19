import matplotlib.pyplot as plt, numpy as np, PIL as image_lib, pathlib, tensorflow as tflow, numpy as np, os, sys, sklearn
from PIL import Image
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.models import Sequential, load_model, save_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.applications import ResNet50, ResNet50V2

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done
from Config.import_config import ConfigDict

config_dict = ConfigDict().dict
model_name = r'230817_resnet50'
epochs = 100

#build model
model = Sequential()
model.add(ResNet50(include_top = False, pooling = 'avg', classes=1))
for each_layer in model.layers:
  each_layer.trainable=False
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(1, activation='sigmoid'))
model.layers[0].trainable = False
model.summary()
model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

image_data_generator = ImageDataGenerator(validation_split=0.05)
train_ds = image_data_generator.flow_from_directory(config_dict['dataset_from_kiresbom_cropped_snr'], target_size=(224, 224), batch_size=32, class_mode='binary', subset='training', seed=123)
validation_ds = image_data_generator.flow_from_directory(config_dict['dataset_from_kiresbom_cropped_snr'], target_size=(224, 224), batch_size=32, class_mode='binary', subset='validation', seed=123)

filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + model_name
mc = ModelCheckpoint(filepath, monitor='val_accuracy', mode='max')
hs = model.fit(train_ds, validation_data=validation_ds, epochs=epochs, callbacks=[mc])
print(hs)
accuracy = hs.history['accuracy']
val_accuracy = hs.history['val_accuracy']
Done()

#remove low snr
#Check dataset import
#