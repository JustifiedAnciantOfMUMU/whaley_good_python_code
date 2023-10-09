import os, numpy as np, sys
import keras, cv2, librosa
from keras.optimizers import Adam
from keras.preprocessing import image
from keras.utils import load_img, img_to_array

dir = os.getcwd()
#data_dir = r'E:/Thesis/Datasets/230831_upsweep_spectrogram/val'
#data_dir = r'E:/Thesis/Datasets/230903_Gunshot_datasets/spectrograms/val'
#data_dir = r'E:\Thesis\Datasets\230905_Gunshot_likeupcall_Dataset\val'
data_dir = r'E:\Thesis\Datasets\051023_DCLDE2024\D1 - Datasets\comb'
#model = keras.models.load_model(r'D:/231006_resnet50 - Copy')
#model = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230905_resnet50_gunshot_long')
model = keras.models.load_model(r'E:/Thesis/230905_resnet50_joint')
model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
audio_files = []
labels =[]

for root, directories, files in os.walk(data_dir + r'/call'):
    for filename in files:
        audio_files.append(os.path.join(root, filename)) 
        labels.append(1)

for root, directories, files in os.walk(data_dir + r'/nocall'):
    for filename in files:
        audio_files.append(os.path.join(root, filename))
        labels.append(0)

num_files = len(audio_files)

def predict_set(model):
    pred = []
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(audio_files)):
        # img = cv2.imread(audio_files[i])
        # img = cv2.resize(img,(224,224))
        # img = np.reshape(img,[1,224,224,3])
        img = load_img(audio_files[i], target_size=(224, 224))
        img_tensor = img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)    
        #img_tensor /= 255.  
        _pred = model.predict(img_tensor)
        _pred = 1 - _pred[0][0]
        pred.append(_pred)
        if _pred > 0.5 and labels[i]==1:TP+=1
        elif _pred > 0.5 and labels[i]==0:FP+=1
        elif _pred <= 0.5 and labels[i]==0:TN+=1
        elif _pred <= 0.5 and labels[i]==1:FN+=1
    return pred, TP, TN, FP, FN

def predict_set_wav(model):
    pred = []
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(audio_files)):
        audio, _ = librosa.load(audio_files[i], sr=1000, mono=True)
        audio = np.pad(audio, (0, 3001 - len(audio)), mode='edge')
        input = np.array(audio)
        input = np.expand_dims(input, axis=1)
        input = np.expand_dims(input, axis=1)
        _pred = model.predict(input)
        _pred = _pred[0][0]
        pred.append(_pred)
        if _pred > 0.5 and labels[i]==1:TP+=1
        elif _pred > 0.5 and labels[i]==0:FP+=1
        elif _pred <= 0.5 and labels[i]==0:TN+=1
        elif _pred <= 0.5 and labels[i]==1:FN+=1
    return pred, TP, TN, FP, FN

_predictions = predict_set(model)
print(_predictions)