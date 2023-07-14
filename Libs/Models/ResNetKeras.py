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

def display_dataset_sample(train_ds):
    plt.figure(figsize=(10, 10))

    for images, labels in train_ds.take(1):
      for var in range(6):
        ax = plt.subplot(3, 3, var + 1)
        plt.imshow(images[var].numpy().astype("uint8"))
        plt.axis("off")

class resnet_base():
    model = Sequential()
    dir = os.getcwd() + '/Libs/Models/Trained_models'

    def __init__(self, model_name=None) -> None:
      if model_name == None:
        self.model_name = 'unnamed'
      else:
        self.model_name = model_name
    
    def save_model(self):
      filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + self.model_name
      save_model(self.model, filepath)

    # def save_weightings(self):
    #   filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + self.model_name
    #   self.model.save_weights(filepath, overwrite=True, save_format=None, options=None)

    
    def load_model(self, model_name=None):
      self.__init__(model_name)
      filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + self.model_name
      self.model = load_model(filepath)
    
    # def load_weightings(self, model_name=None):
    #   self.__init__(model_name)
    #   self._build()
    #   self.model.compile(optimizer=Adam(lr=0.001), loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    #   filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + self.model_name
    #   self.model.load_weights(filepath, skip_mismatch=False, by_name=False, options=None)
    
    def train_model(self, dataset_dir, epochs=20, save_weights_only=False):
      filepath = os.getcwd() + r'\Libs\Models\Trained_models/' + self.model_name
      self._build()
      train_set, validation_set = self._prep_dataset(dataset_dir)
      self.model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy',metrics=['accuracy'])
      #Stop once overfitting starts to occur
      #es=EarlyStopping(monitor='val_accuracy', mode='max', verbose=1, patience=4)
      #Save the best model
      mc = ModelCheckpoint(filepath, monitor='val_accuracy', mode='max')
      self.model.fit(train_set, validation_data=validation_set, epochs=epochs, callbacks=[mc])
    
    def predict(self, file_path):
      image = Image.open(file_path)
      image_resized = image.resize((500, 400))
      #image_array = np.expand_dims(np.array(image_resized), axis=0)
      image=np.expand_dims(image_resized,axis=0)
      model_pred= self.model.predict(image)
      return model_pred


    def _build(self):
        self.model = Sequential()
        self.model.add(ResNet50(include_top = False, pooling = 'avg', classes=1))
        for each_layer in self.model.layers:
          each_layer.trainable=False
        self.model.add(Flatten())
        self.model.add(Dense(512, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.layers[0].trainable = False
        self.model.summary()

    @staticmethod
    def _prep_dataset(dataset_filepath, batch_size = 32, img_height=500, img_width=400):
      image_data_generator = ImageDataGenerator(validation_split=0.1)
      train_ds = image_data_generator.flow_from_directory(dataset_filepath, target_size=(img_height, img_width), batch_size=batch_size, class_mode='binary', subset='training', seed=123)
      validation_ds = image_data_generator.flow_from_directory(dataset_filepath, target_size=(img_height, img_width), batch_size=batch_size, class_mode='binary', subset='validation', seed=123)

      return train_ds, validation_ds

if __name__ == '__main__':
  
  config_dict = ConfigDict().dict
  #Train
  res50 = resnet_base('230710_res50')
  res50.train_model(config_dict['dataset_from_kiresbom'], 100)

  #load
  # res50=resnet_base()
  # res50.load_model('230708_res50')
  # print(res50.predict(r'E:\Thesis\Datasets\Kiresbom_dataset\call\A_64.png'))
  # print(res50.predict(r'E:\Thesis\Datasets\Kiresbom_dataset\no_call\A_0.png'))

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