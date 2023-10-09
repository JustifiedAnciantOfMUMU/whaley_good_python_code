import numpy as np, os,sys, librosa, keras
from pydub import AudioSegment
from tensorflow import keras
from keras import layers
from keras.utils import to_categorical

sys.path.append(os.getcwd())
from Libs.Tools.Done import Done
from Config.import_config import ConfigDict

class audio_time_series_generator (keras.utils.Sequence):

    def __init__ (self, data_dir, batch_size=32, sample_rate=1000):
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
        self.num_files = len(self.audio_files)
        self.index = 0

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
            if audio_file[-10:-4] == 'nocall':
                batch_Y.append(0)
            else:
                batch_Y.append(1)

            index += 1

        # Pad sequences to have the same length within the batch
        max_length = max(len(audio) for audio in batch_X)
        # assert all(len(x) == max_length for x in batch_X), [len(x) for x in batch_X]
        try:
            batch_X = [np.pad(audio, (0, max_length - len(audio)), mode='edge') for audio in batch_X]
        except:
            print(audio)
        return np.array(batch_X), np.array(batch_Y)


sample_rate = 2000
training_clip_length = 0.5
time_step = 0.1
learning_rate = 0.01
model_name = '230923_BiLSTM_Gunshots'
epochs = 50

model = keras.Sequential([
    keras.layers.Bidirectional(keras.layers.LSTM(120)),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.build((1, 1, 1))

train_ds = audio_time_series_generator(r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\train', sample_rate=sample_rate)
validation_ds = audio_time_series_generator(r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\val', sample_rate=sample_rate)

filepath = os.getcwd() + r'\Libs\Models\Trained_models\\' + model_name
hs = model.fit(train_ds, validation_data=validation_ds, epochs=epochs)
print(hs)
accuracy = hs.history['accuracy']
val_accuracy = hs.history['val_accuracy']

print(accuracy)
print('\n/n')
print(val_accuracy)
Done()


# inputs = keras.Input(shape=(int(training_clip_length * sample_rate), 1), batch_size=32)
# x = layers.Bidirectional(layers.LSTM(120, return_sequences=True))(input)
# x = layers.Dense(activation="relu")(x)
# x = layers.Dense(activation="relu")(x)
# outputs = layers.Dense(1, activation="sigmoid")(x)
# model = keras.Model(inputs, outputs)