import sys, os

def folder_rename(folder_path, file_extension):
    for file in os.listdir(folder_path):
        if file[-4:] == file_extension:
            new_name = file[:-5] + r'0.wav'
            new_path = os.path.join(folder_path, new_name)
            os.rename(os.path.join(folder_path, file), new_path)

if __name__ == '__main__':
    folder_rename(r'E:\Thesis\Datasets\Gunshot_spectrogram_dataset\call', r'.png')
    folder_rename(r'E:\Thesis\Datasets\Gunshot_dataset\call', r'.wav')