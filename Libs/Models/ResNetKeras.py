import matplotlib.pyplot as plt, numpy as np, PIL as image_lib, pathlib, tensorflow as tflow, numpy as np, os, sys
from PIL import Image
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras.applications import ResNet50, ResNet50V2

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done

def display_dataset_sample(train_ds):
    plt.figure(figsize=(10, 10))

    for images, labels in train_ds.take(1):
      for var in range(6):
        ax = plt.subplot(3, 3, var + 1)
        plt.imshow(images[var].numpy().astype("uint8"))
        plt.axis("off")

class resnet_base():
    model = Sequential()

    def __init__(self) -> None:
      self.model.add(ResNet50(include_top = False, pooling = 'avg', classes=2))
      for each_layer in self.model.layers:
        each_layer.trainable=False
      self.model.add(Flatten())
      self.model.add(Dense(512, activation='relu'))
      self.model.add(Dense(5, activation='softmax'))
      self.model.layers[0].trainable = False
    
    def save_model(self, file_name):
      self.model = load_model(os.path.join(os.getcwd(), r'Libs/Models/Trained_models', file_name))
    
    def load_model(self, file_name):
      self.model = load_model(os.path.join(os.getcwd(), r'Libs/Models/Trained_models', file_name))
    
    def train_model(self, train_dir, val_dir):
      train_set, validation_set = self._prep_dataset(train_dir, val_dir) #look at size!!!!!!!
      #Stop once overfitting starts to occur
      es=EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=4)
      #Save the best model
      mc = ModelCheckpoint('Model/best_model_Certainty.h5', monitor='val_accuracy', mode='max')
      history = self.model.fit(train_set, validation_data=validation_set, epochs=10)
    
    @staticmethod
    def _prep_dataset(train_filepath, val_filepath, batch_size = 32, img_height=180, img_width=180):

        train_ds = tflow.keras.preprocessing.image_dataset_from_directory(train_filepath, validation_split=0.2, subset="training", seed=123, 
                                                                label_mode='categorical', image_size=(img_height, img_width), batch_size=batch_size)
    
        validation_ds = tflow.keras.preprocessing.image_dataset_from_directory(val_filepath, validation_split=0.2, subset="training", seed=123, 
                                                                label_mode='validation', image_size=(img_height, img_width), batch_size=batch_size)
        
        return train_ds, validation_ds



if __name__ == '__main__':
  
  Done()

  # demo_dataset = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
  # directory = tflow.keras.utils.get_file('flower_photos', origin=demo_dataset, untar=True)
  # data_directory = pathlib.Path(directory)
  # all_sunflowers = list(data_directory.glob('sunflowers/*'))
  # train_set = tflow.keras.preprocessing.image_dataset_from_directory(data_directory,validation_split=0.2,subset="training",seed=123,image_size=(180,180),batch_size=32)
  # validation_set = tflow.keras.preprocessing.image_dataset_from_directory(data_directory,validation_split=0.2,subset="validation",seed=123,image_size=(180,180),batch_size=32)

  # dnn_model = Sequential()
  # imported_model= tflow.keras.applications.ResNet50(include_top=False,input_shape=(180,180,3),pooling='avg',classes=5,weights='imagenet')
  # for layer in imported_model.layers:
  #   layer.trainable=False

  # dnn_model.add(imported_model)
  # dnn_model.add(Flatten())
  # dnn_model.add(Dense(512, activation='relu'))
  # dnn_model.add(Dense(5, activation='softmax'))
  # dnn_model.summary()

  # dnn_model.compile(optimizer=Adam(lr=0.001), loss='sparse_categorical_crossentropy',metrics=['accuracy'])
  # history = dnn_model.fit( train_set, validation_data=validation_set, epochs=10)

  # image = Image.open(str(all_sunflowers[1]))
  # image_resized = image.resize((180, 180))
  # image_array = np.expand_dims(np.array(image_resized), axis=0)
  # image=np.expand_dims(image_resized,axis=0)
  # model_pred=dnn_model.predict(image)

  # print('done')