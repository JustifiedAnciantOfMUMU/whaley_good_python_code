import os
data_dir = r'E:\Thesis\Datasets\230831_upsweep_wav\val\nocall'

for root, directories, files in os.walk(data_dir):
    for filename in files:
        my_dest =data_dir + '/'  + filename[:-4] + '_nocall.wav'
        os.rename((data_dir + '/' + filename), my_dest)