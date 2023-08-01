import tensorflow as tf, numpy as np, os, itertools, sys, random, cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.core import Dense
from keras.models import Sequential, load_model, save_model
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input
from keras.optimizers import Adam

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Tools.Done import Done

def save_to_csv(csv_file, label, features):
    features = features.reshape((features.shape[0], 7 * 7 * 2048))
    vec = ",".join([str(v) for v in features[0]])
    csv_file.write("{},{}\n".format(label, vec))

def convert_file(file_path, csv_file):
    img = cv2.imread(file_path)
    processed_img = preprocess_input(img)
    processed_img = np.expand_dims(processed_img, axis=0)
    
    features = model.predict(processed_img)
    label = file_path[-5]
    save_to_csv(csv_file, label, features)

def convert_files(file_list, csv_file):
    for file in file_list:
        convert_file(file, csv_file)

config_dict = ConfigDict().dict
directory_path = config_dict['dataset_from_kiresbom'] + '/call/'
list_of_files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
directory_path = config_dict['dataset_from_kiresbom'] + '/no_call/'
list_of_files += [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

random.shuffle(list_of_files)

num_validation_files = int(len(list_of_files) / 10)
train_files = list_of_files[:(num_validation_files * -1)]
val_files = list_of_files[(num_validation_files * -1):]

# Load the pre-trained ResNet50 model without top classification layers
model = ResNet50(include_top=False)

csvPath = config_dict['resnet50_features_from_kiresbom'] + r'/train_dataset.csv'
print()
train_csv = open(csvPath, "w")
csvPath = config_dict['resnet50_features_from_kiresbom'] + r'/val_dataset.csv'
val_csv = open(csvPath, "w")

convert_files(train_files, train_csv)
convert_files(val_files, val_csv)







Done()

# config_dict = ConfigDict().dict
# dirpath = config_dict['resnet50_features_from_kiresbom']
# list_of_file_names = [os.path.join(dirpath, f) for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
# random.shuffle(list_of_file_names)
# num_validation_files = int(len(list_of_file_names) / 10)
# train_files = list_of_file_names[:(num_validation_files * -1)]
# val_files = list_of_file_names[(num_validation_files * -1):]

# def gen():
#     for i in itertools.count(1):
#         data1 = np.load(list_of_file_names[i%len(list_of_file_names)])
#         data2 = np.where(data1 > 1, data1, 1)
#         yield tf.convert_to_tensor(np.where(data2>0, 20*np.log10(data2), 0))

# train_dataset = tf.data.Dataset.from_generator(gen(), (tf.float32))
# val_dataset = tf.data.Dataset.from_generator(gen(), (tf.float32))

# model = Sequential()
# model.add(Dense(512, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# model.layers[0].trainable = False
# model.build((None, 2048))
# model.summary()

# model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
# history = model.fit(train_dataset, validation_data=val_dataset, epochs=1)

####### take 2 ######

# config_dict = ConfigDict().dict
# dirpath = config_dict['resnet50_features_from_kiresbom']

# list_of_file_names = [os.path.join(dirpath, f) for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))]
# random.shuffle(list_of_file_names)
# num_validation_files = int(len(list_of_file_names) / 10)
# train_files = list_of_file_names[:(num_validation_files * -1)]
# val_files = list_of_file_names[(num_validation_files * -1):]

# def train_gen():
#     for i in itertools.count(1):
#         data1 = np.load(train_files[i%len(train_files)])
#         data2 = np.where(data1 > 1, data1, 1)
#         yield tf.convert_to_tensor(np.where(data2>0, 20*np.log10(data2), 0))
        
# def val_gen():
#     for i in itertools.count(1):
#         data1 = np.load(val_files[i%len(val_files)])
#         data2 = np.where(data1 > 1, data1, 1)
#         yield tf.convert_to_tensor(np.where(data2>0, 20*np.log10(data2), 0))

# train_dataset = tf.data.Dataset.from_generator(train_gen, (tf.float32), output_shapes=((1, 7, 7, 2048)))
# val_dataset = tf.data.Dataset.from_generator(val_gen, (tf.float32), output_shapes=((1, 7, 7, 2048)))

# model = Sequential()
# model.add(Dense(512, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# model.layers[0].trainable = False
# model.build((None, 2048))
# model.summary()

# model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])
# history = model.fit(train_dataset, validation_data=val_dataset, epochs=1)

