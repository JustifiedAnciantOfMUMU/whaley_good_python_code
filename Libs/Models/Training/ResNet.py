import numpy as np, os, sys
from keras.layers.core import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Tools.Done import Done

model_name = r'230729_Resnet50'

def csv_feature_generator(inputPath, bs, mode="train"):
	# open the input file for reading
	f = open(inputPath, "r")
	# loop indefinitely
	while True:
		# initialize our batch of data and labels
		data = []
		labels = []
		# keep looping until we reach our batch size
		while len(data) < bs:
			# attempt to read the next row of the CSV file
			row = f.readline()
			# check to see if the row is empty, indicating we have
			# reached the end of the file
			if row == "":
				# reset the file pointer to the beginning of the file
				# and re-read the row
				f.seek(0)
				row = f.readline()
				# if we are evaluating we should now break from our
				# loop to ensure we don't continue to fill up the
				# batch from samples at the beginning of the file
				if mode == "eval":
					break
			# extract the class label and features from the row
			row = row.strip().split(",")
			label = int(row[0])
			features = np.array(row, dtype="float")
			# update the data and label lists
			data.append(features)
			labels.append(label)
		# yield the batch to the calling function
		yield (np.array(data), np.array(labels))
		

config_dict = ConfigDict().dict

#replace
trainPath = config_dict['resnet50_features_from_kiresbom'] + '/train_dataset.csv'
valPath = config_dict['resnet50_features_from_kiresbom'] + '/val_dataset.csv'

# determine the total number of images in the training and validation sets
totalTrain = sum([1 for l in open(trainPath)])
totalVal = sum([1 for l in open(valPath)])

trainGen = csv_feature_generator(trainPath, 32, mode="train")
valGen = csv_feature_generator(valPath, 32, mode="eval")

model = Sequential()
model.add(Dense(256, input_shape=(32, 100353), activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(1, activation='sigmoid'))
model.summary()

model.compile(optimizer=Adam(), loss='binary_crossentropy',metrics=['accuracy'])

#Save the best model
model_path = os.getcwd() + r'\Libs\Models\Trained_models/' + model_name
mc = ModelCheckpoint(model_path, monitor='val_accuracy', mode='max')

H = model.fit(trainGen, steps_per_epoch=totalTrain, validation_data=valGen, validation_steps=totalVal, epochs=20, callbacks=[mc])
print(H)

Done()