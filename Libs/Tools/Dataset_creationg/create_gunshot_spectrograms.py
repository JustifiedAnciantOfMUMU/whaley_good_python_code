import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot

config_dict = ConfigDict().dict

def val_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("Folder created:", path)
    else:
        print("Folder already exists:", path)

call_folder = config_dict['Gunshot_dataset'] + r'\call'
nocall_folder = config_dict['Gunshot_dataset'] + r'\nocall'

#convert spectrograms

def convert_to_spec(folder_path, out_folder_path):
    for file in os.listdir(folder_path):
        file_path = folder_path + r'\\' + file
        if os.path.exists(file_path):
            f, t, _spectrogram = Spectrogram().create_spectrgram(file_path, 0.1)
            _spectrogram_log = 10 * np.log10(_spectrogram)
            _denoised_spectrogram = Spectrogram().denoise_median(_spectrogram_log)
            Spectrogram().plot_spectrogram(t, f, _denoised_spectrogram)
            Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, out_folder_path, file[:-4], lowerthresh=100, upperthresh=1000)

out_call_folder = config_dict['Gunshot_spectrogram_dataset'] + r'\call'
out_nocall_folder = config_dict['Gunshot_spectrogram_dataset'] + r'\nocall'
val_folder(out_call_folder)
val_folder(out_nocall_folder)

convert_to_spec(call_folder, out_call_folder)
#convert_to_spec(nocall_folder, out_nocall_folder)

Done()