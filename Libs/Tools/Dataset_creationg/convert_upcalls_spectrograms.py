import sys, os, csv, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Files.Excel_import import ExcelFile
from Libs.Tools.Done import Done

config_dict = ConfigDict().dict
folder_path = r'E:\Thesis\Datasets\_3_second_nocalls'
out_folder_path = config_dict['dataset_from_kiresbom'] + r'\no_call'

for file in os.listdir(folder_path) :
    f, t, _spectrogram = Spectrogram().create_spectrgram(folder_path + r'\\' + file)
    _spectrogram_log = 10 * np.log10(_spectrogram)
    _denoised_spectrogram = Spectrogram().denoise_median(_spectrogram_log)
    Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, (out_folder_path), 'D_'+file[:-4])

Done()