import matplotlib.pyplot as plt
import numpy as np, os
import keras, cv2
from keras.optimizers import Adam
from keras.utils import load_img, img_to_array

def predict_list_files(model, files_array, predict_array):
    for file in files_array:
        # img = cv2.imread(dir + label + '/' + file)
        # img = cv2.resize(img,(240,240))
        # img = np.reshape(img,[1,240,240,3])
        filepath = dir + '/' + file
        if os.path.exists(filepath):
            img = load_img(filepath, target_size=(224, 224))
            img_tensor = img_to_array(img)
            img_tensor = np.expand_dims(img_tensor, axis=0)    
            predict_array.append(1 - model.predict(img_tensor)[0][0])
        else:
            print(filepath)

#dir = r'E:\Thesis\Datasets\230904_Combined\val\nocall'
dir = r'E:\Thesis\Datasets\051023_DCLDE2024\D1\nocall'
#dir = r'E:/Thesis/Datasets/230831_upsweep_spectrogram/val/call'
#dir = r'E:\Thesis\Datasets\230831_upsweep_spectrogram\val/nocall'
call_files = os.listdir(dir)

model1, model2, model3 = [], [], []

model_1 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/231006_resnet50')
model_1.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
predict_list_files(model_1, call_files, model1)

model_2 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230905_resnet50_gunshot_long')
model_2.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
predict_list_files(model_2, call_files, model2)


model_3 = keras.models.load_model(r'E:/Thesis/230905_resnet50_joint')
model_3.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
predict_list_files(model_3, call_files, model3)

bins = np.linspace(0, 1, 20)
plt.hist([model1, model2, model3], bins, label=['Upsweep Model', 'Gunshot Model', 'Combined Model'])
plt.legend()
plt.xlim(0,1)
plt.ylim(0,320) #275, 538
plt.title('Predictions Of ResNet50 Models - DCLDE D1 Gunshots')
plt.xlabel('Prediction Value'), plt.ylabel('Number Of Samples')
plt.show()

print('Done')