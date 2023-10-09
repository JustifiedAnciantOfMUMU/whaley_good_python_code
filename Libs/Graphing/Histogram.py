import matplotlib.pyplot as plt
import numpy as np, os
import keras, cv2
from keras.optimizers import Adam
from keras.utils import load_img, img_to_array


# dir = r'E:/Thesis/Datasets/230905_Gunshot_likeupcall_Dataset/val'
# dir = r'E:/Thesis/Datasets/230903_Gunshot_datasets/spectrograms/val'
dir = r'E:\Thesis\Datasets\230904_Combined\val'
call_files = os.listdir(dir + r'/call')
nocall_files = os.listdir(dir + r'/nocall')

# model = keras.models.load_model(r'C:\\Users/Jon/Documents/UNI/Thesis/code/Libs/Models/Trained_models/230904_resnet50_gunshot')
model = keras.models.load_model(r'E:/Thesis/230905_resnet50_joint')

model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

calls, nocalls = [], []

def predict_list_files(files_array, predict_array, label):
    for file in files_array:
        # img = cv2.imread(dir + label + '/' + file)
        # img = cv2.resize(img,(240,240))
        # img = np.reshape(img,[1,240,240,3])
        filepath = dir + label + '/' + file
        if os.path.exists(filepath):
            img = load_img(filepath, target_size=(224, 224))
            img_tensor = img_to_array(img)
            img_tensor = np.expand_dims(img_tensor, axis=0)    
            predict_array.append(1 - model.predict(img_tensor)[0][0])
        else:
            print(filepath)

predict_list_files(call_files, calls, r'/call')
predict_list_files(nocall_files, nocalls, r'/nocall')

bins = np.linspace(0, 1, 20)
plt.hist(nocalls, bins, alpha=0.25, label='no call', edgecolor='blue')
plt.hist(calls, bins, alpha=0.25, label='call', edgecolor='orange')
plt.legend(loc='upper right')
plt.xlim(0,1)
plt.ylim(0,550)
plt.title('Histogram Of ResNet50 Predictions - Combined Data Set')
plt.xlabel('Prediction Value'), plt.ylabel('Number Of Samples')
plt.show()

print('Done')
