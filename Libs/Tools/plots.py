import sys, os

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Graphing.plot import plot_performance
from Libs.Tools.Done import Done
from Libs.Files.Excel_import import ExcelFile

columns = ExcelFile().extract_colum_from_sheet('Sheet1', r'C:\Users\Jon\Downloads\classification_model data.xlsx')

# plot_performance([columns[0], columns[0], columns[0], columns[0][:11]], [columns[1], columns[3], columns[5], columns[7][:11]] , ['Resnet50', 'VGG16', 'Resnet152', 'ConvNeXtXLarge'], ['Epoch', 'Training_Accuracy'], 'Training Accuracy of Frequency Domain Models')

#plot_performance([columns[0], columns[0], columns[0], columns[0][:11]], [columns[2], columns[4], columns[6], columns[8][:11]] , ['Resnet50', 'VGG16', 'Resnet152', 'ConvNeXtXLarge'], ['Epoch', 'Validation_Accuracy'], 'Validation Accuracy of Frequency Domain Models')

# plot_performance([columns[0], columns[0]], [columns[1], columns[2]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy of Resnet50 Model')

# plot_performance([columns[0], columns[0]], [columns[3], columns[4]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy of VGG16 Model')
 
# plot_performance([columns[0], columns[0]], [columns[5], columns[6]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy of Resnet152 Model')

# plot_performance([columns[0][:11], columns[0][:11]], [columns[7][:11], columns[8][:11]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy of ConvNeXtXLarge Model')

#plot_performance([columns[0][:11], columns[0][:11],columns[0][:11], columns[0][:11]], [columns[7][:11], columns[8][:11], columns[5][:11], columns[6][:11]] ,['ConvNeXt - Training Accuracy', 'ConvNeXt - Validation Accuracy', 'Resnet152 - Training Accuracy', 'Resnet152 - Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy of ConvNeXtXLarge and Resnet152 Models in first 10 epochs')
#plot_performance([columns[0], columns[0],columns[0], columns[0]], [columns[9], columns[10], columns[11], columns[12]] ,['0.5 s Spectrograms- Training Accuracy', '0.5 s Spectrograms- Validation Accuracy', '3 s - Training Accuracy', '3 s - Validation Accuracy'], ['Epoch', 'Accuracy'], 'Effect of Gunshot Data Format Accuracy Across Training')



#plot_performance([columns[0], columns[0]], [columns[1], columns[2]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy\'s of Resnet50 Model Trained on NARW Upcall Data set')
#plot_performance([columns[0], columns[0]], [columns[11], columns[12]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy\'s of Resnet50 Model Trained on NARW 3 s Gunshot Data set')
#plot_performance([columns[0], columns[0]], [columns[13], columns[14]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Accuracy\'s of Resnet50 Model Trained on NARW Joint Dataset')


#####time domain graphs
#plot_performance([columns[0][:50], columns[0][:50], columns[0][:50]], [columns[15][:50], columns[19][:50], columns[23][:50]] ,['RNN- Training Accuracy', 'LSTM- Training Accuracy', 'Bi-LSTM - Training Accuracy'], ['Epoch', 'Accuracy'], 'Time Domain Models Training Accuracy - Upsweep data')
#plot_performance([columns[0][:50], columns[0][:50], columns[0][:50]], [columns[16][:50], columns[20][:50], columns[24][:50]] ,['RNN- Validation Accuracy', 'LSTM- Validation Accuracy', 'Bi-LSTM - Validation Accuracy'], ['Epoch', 'Accuracy'], 'Time Domain Models Validation Accuracy - Upsweep data')

#plot_performance([columns[0][:50], columns[0][:50]], [columns[15][:50], columns[16][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - RNN For Upsweep Call Detection')
# plot_performance([columns[0][:50], columns[0][:50]], [columns[19][:50], columns[20][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - LSTM For Upsweep Call Detection')
#plot_performance([columns[0][:50], columns[0][:50]], [columns[23][:50], columns[24][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - Bi-LSTM For Upsweep Call Detection')

plot_performance([columns[0][:50], columns[0][:50], columns[0][:50]], [columns[17][:50], columns[21][:50], columns[25][:50]] ,['RNN- Training Accuracy', 'LSTM- Training Accuracy', 'Bi-LSTM - Training Accuracy'], ['Epoch', 'Accuracy'], 'Time Domain Models Training Accuracy - Gunshot data')
plot_performance([columns[0][:50], columns[0][:50], columns[0][:50]], [columns[18][:50], columns[22][:50], columns[26][:50]] ,['RNN- Validation Accuracy', 'LSTM- Validation Accuracy', 'Bi-LSTM - Validation Accuracy'], ['Epoch', 'Accuracy'], 'Time Domain Models Validation Accuracy - Gunshot data')

plot_performance([columns[0][:50], columns[0][:50]], [columns[17][:50], columns[18][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - RNN For Gunshot Call Detection')
plot_performance([columns[0][:50], columns[0][:50]], [columns[21][:50], columns[22][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - LSTM For Gunshot Call Detection')
plot_performance([columns[0][:50], columns[0][:50]], [columns[25][:50], columns[26][:50]] , ['Training Accuracy', 'Validation Accuracy'], ['Epoch', 'Accuracy'], 'Training And Validation Accuracys - Bi-LSTM For Gunshot Call Detection')


Done()


