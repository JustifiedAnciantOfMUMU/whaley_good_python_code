import matplotlib.pyplot as plt
import numpy as np, os
import keras, cv2
from keras.optimizers import Adam
from keras.utils import load_img, img_to_array

dir = r'E:/Thesis/Datasets/230831_upsweep_spectrogram/val'
call_files = os.listdir(dir + r'/call')
nocall_files = os.listdir(dir + r'/nocall')

# VGG16 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230831_vgg16_upsweep')
# ResNet50 = keras.models.load_model(r'E:/Thesis/230905_resnet50')
# ResNet152 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230831_resnet152_upsweep')

# VGG16.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
# ResNet50.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
# ResNet152.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

VGG16 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230831_vgg16_upsweep')
ResNet50 = keras.models.load_model(r'D:/231006_resnet50')
ResNet152 = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230831_resnet152_upsweep')

VGG16.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
ResNet50.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
ResNet152.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])



def predict_list_files(files_array, label):
        for file in files_array:
            img = load_img(dir + label + '/' + file, target_size=(224, 224))
            img_tensor = img_to_array(img)
            img_tensor = np.expand_dims(img_tensor, axis=0)    
            VGG16_pred.append(1 - VGG16.predict(img_tensor)[0][0])
            ResNet50_pred.append(1 - ResNet50.predict(img_tensor)[0][0])
            ResNet152_pred.append(1 - ResNet152.predict(img_tensor)[0][0])


def plot (title, ylim):
    bins = np.linspace(0, 1, 20)
    plt.hist([VGG16_pred,ResNet50_pred,ResNet152_pred], bins, label=['VGG16', 'ResNet50', 'ResNet152'])
    plt.legend()
    plt.xlim(0,1)
    plt.ylim(0,ylim)
    plt.title(title)
    plt.show()

# VGG16_pred, ResNet50_pred, ResNet152_pred = [], [], []
# predict_list_files(call_files, r'/call')
# plot('Histogram Of \'Call\' Labeled Sample Prediction Values', 240)

VGG16_pred, ResNet50_pred, ResNet152_pred = [], [], []
predict_list_files(nocall_files, r'/nocall')
plot('Histogram Of \'No Call\' Labeled Sample Prediction Values', 313)

print('Done')