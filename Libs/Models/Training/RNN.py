from pandas import read_csv
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math, librosa, os, sys
import matplotlib.pyplot as plt
from keras.optimizers import Adam
import numpy as np, os,sys, librosa, keras
from pydub import AudioSegment
from tensorflow import keras
from keras import layers
from keras.utils import to_categorical

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done
from Config.import_config import ConfigDict

class audio_time_series_generator (keras.utils.Sequence):

    def __init__ (self, data_dir, batch_size=64, sample_rate=1000):
        self.batch_size = batch_size
        self.sample_rate = sample_rate
        self.audio_files = []
        for root, directories, files in os.walk(data_dir + r'/call'):
            for filename in files:
                self.audio_files.append(os.path.join(root, filename)) 

        for root, directories, files in os.walk(data_dir + r'/nocall'):
            for filename in files:
                self.audio_files.append(os.path.join(root, filename)) 

        np.random.shuffle(self.audio_files)
        np.random.shuffle(self.audio_files)
        np.random.shuffle(self.audio_files)
        self.num_files = len(self.audio_files)

    def on_epoch_end(self):
        np.random.shuffle(self.audio_files)

    def __len__(self):
        return self.num_files // self.batch_size

    def __getitem__(self, index):
        batch_X = []
        batch_Y = []

        for _ in range(self.batch_size):
            if index >= self.num_files:
                # index = 0
                # np.random.shuffle(audio_files)
                break

            audio_file = self.audio_files[index]
            audio, _ = librosa.load(audio_file, sr=self.sample_rate, mono=True)
            batch_X.append(audio)
            _extract = audio_file[-10:-4]
            if _extract == 'nocall':
                batch_Y.append(0)
            else:
                batch_Y.append(1)

            index += 1

        #Pad sequences to have the same length within the batch
        max_length = max(len(audio) for audio in batch_X)
        batch_X = [np.pad(audio, (0, max_length - len(audio)), mode='edge') for audio in batch_X]
        return np.array(batch_X), np.array(batch_Y)

model = Sequential()
model.add(SimpleRNN(120))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer=Adam(0.0001), metrics=['accuracy'])
model.build((1, 1, 1))

sample_rate = 1000
model_name = '091023_RNN_gunshot'
epochs = 50

train_ds = audio_time_series_generator(r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\train', sample_rate=1000)
validation_ds = audio_time_series_generator(r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\val', sample_rate=1000)

filepath = r'C:/Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/' + model_name
hs = model.fit(train_ds, validation_data=validation_ds, epochs=epochs)
accuracy = hs.history['accuracy']
val_accuracy = hs.history['val_accuracy']

print(accuracy)
print('\n/n')
print(val_accuracy)
Done()