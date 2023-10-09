import os, numpy as np, sys, math
import keras, cv2, librosa, tensorflow as tf
from keras.optimizers import Adam
from keras.utils import load_img, img_to_array

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Tools.Done import Done

data_dir = r'E:\Thesis/Datasets/230831_upsweep_spectrogram/val'
audio_files = []
labels =[]

for root, directories, files in os.walk(data_dir + r'/call'):
    for filename in files:
        audio_files.append(os.path.join(root, filename)) 
        labels.append(0)

for root, directories, files in os.walk(data_dir + r'/nocall'):
    for filename in files:
        audio_files.append(os.path.join(root, filename))
        labels.append(1)

num_files = len(audio_files)

LSTM = keras.models.load_model(r'D:/231006_resnet50')
LSTM.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

BiLSTM = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230831_resnet152_upsweep')
BiLSTM.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

def McNemars_img(A, B):
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0
    thresh = 0.5
    for i in range(len(audio_files)):
        img = load_img(audio_files[i], target_size=(224, 224))
        img_tensor = img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)    
        
        predA = A.predict(img_tensor)[0][0]
        math.floor(predA) if predA < (math.floor(predA) + thresh) else math.ceil(predA)
        predB = B.predict(img_tensor)[0][0]
        math.floor(predB) if predB < (math.floor(predB) + thresh) else math.ceil(predB)

        if labels[i] == predA and labels[i] == predB:n11+=1
        elif labels[i] != predA and labels[i] != predB:n00+=1
        elif labels[i] == predA and labels[i] != predB:n10+=1
        elif labels[i] != predA and labels[i] == predB:n01+=1

    return n00, n01, n10, n11

def McNemars_wav(A, B):
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0
    thresh = 0.5
    for i in range(len(audio_files)):
        audio, _ = librosa.load(audio_files[i], sr=1000, mono=True)
        audio = np.pad(audio, (0, 3001 - len(audio)), mode='edge')
        input = np.array(audio)
        input = np.expand_dims(input, axis=1)
        input = np.expand_dims(input, axis=1)
        predA = A.predict(input)[0][0]
        math.floor(predA) if predA < (math.floor(predA) + thresh) else math.ceil(predA)
        predB = B.predict(input)[0][0]
        math.floor(predB) if predB < (math.floor(predB) + thresh) else math.ceil(predB)

        if labels[i] == predA and labels[i] == predB:n11+=1
        elif labels[i] != predA and labels[i] != predB:n00+=1
        elif labels[i] == predA and labels[i] != predB:n10+=1
        elif labels[i] != predA and labels[i] == predB:n01+=1
    return n00, n01, n10, n11

matrix_values = McNemars_img(LSTM, BiLSTM)
print(matrix_values)
McNemars_value = math.pow((int(matrix_values[1] - matrix_values[2]) - 1), 2) / (matrix_values[1] + matrix_values[2])
print(McNemars_value)

Done()