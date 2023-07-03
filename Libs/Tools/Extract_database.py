import sys, os, csv, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Files.Excel_import import ExcelFile
from Libs.Tools.Done import Done

class KirsebomDatabase():
    def __init__(self, data_dir, dataset_dir) -> None:
        self.data_dir = data_dir
        self.dataset_dir = dataset_dir

    def extract(self):
        train_paths = [r'/clips/dataset_A/train', r'/clips/dataset_B/train']
        val_paths = [r'/clips/dataset_A/val', r'/clips/dataset_B/val']
        dataset_catagories = [r'call', r'no_call']

        #checking dataset folder is correctly setup
        for cat in dataset_catagories:
            self._validate_folder_path(os.path.join(self.dataset_dir, cat))

        #for folder in train_paths:
        #    self._extract_folder(self.data_dir + folder, 1)
        #for folder in val_paths:
        #    self._extract_folder(self.data_dir + folder, 1)

        self._extract_folder(self.data_dir + r'/clips/dataset_C/train', 4)

    def _extract_folder(self, folder_path, val_col=1):

        #import csv
        file_list = os.listdir(folder_path)
        csv_file = [file_name for file_name in file_list if file_name.endswith(".csv")]
        csv = self._import_csv(os.path.join(folder_path, csv_file[0]))
        _dict = self._csv_to_dict(csv, val_col)
        
        file_names = self.get_files_in_folder(os.path.join(folder_path, 'audio') )

        for file in file_names:
            f, t, _spectrogram = Spectrogram().create_spectrgram(folder_path + '/audio/' + file)
            _spectrogram_log = 10 * np.log10(_spectrogram)
            _denoised_spectrogram = Spectrogram().denoise_median(_spectrogram_log)
            if _dict[file] == str(1):
                Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, (self.dataset_dir + '/call'), self._get_file_name(file, _dict[file]))
            else:
                #Spectrogram().plot_spectrogram(t, f, _denoised_spectrogram)
                Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, (self.dataset_dir + '/no_call'), self._get_file_name(file, _dict[file]))


    @staticmethod
    def _validate_folder_path(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print("Folder created:", folder_path)
        else:
            print("Folder already exists:", folder_path)

    
    @staticmethod
    def get_files_in_folder(folder_path):
        file_names = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_names.append(file)
        return file_names
    
    @staticmethod
    def _import_csv(file_path):
        data = []
        
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        return data
    
    @staticmethod
    def _csv_to_dict(csv, val_col=1):
        _dict = {}
        for row in csv[1:]:
            values = row[0].split(";")
            _dict[values[0]] = values[val_col]
        return _dict

    @staticmethod
    def _get_file_name(wav_name, classification):
        file_name =  wav_name[:-4] + '_' + classification + '.jpg'
        return file_name

    

if __name__ == '__main__':
    ## Kirsebom
    config_dict = ConfigDict().dict
    database_kirsebom = KirsebomDatabase(config_dict['kirsebom_data'], config_dict['dataset_from_kiresbom'])
    database_kirsebom.extract()
    Done()