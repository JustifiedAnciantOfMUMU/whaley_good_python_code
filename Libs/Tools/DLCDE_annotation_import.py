import sys, os, librosa, numpy as np

sys.path.append(os.getcwd())
from Libs.Files.Excel_import import ExcelFile
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Tools.Done import Done

export_path = r''
D1_folder_path = r'E:\Thesis\DCLDE 2024\30July2018'
D2_folder_path = r'E:\Thesis\DCLDE 2024\31July2018'

D1_Rows = ExcelFile().extract_rows_from_sheet('annotations 7-30', r'E:/Thesis/DCLDE 2024/annotations.xlsx')
D2_Rows = ExcelFile().extract_rows_from_sheet('annotations 7-31', r'E:/Thesis/DCLDE 2024/annotations.xlsx')

_dict = {}
i = 0

def extract(day_label, rows):
    __dict = {}
    __dict['up'], __dict['gs'] = [], []
    for row in rows:
        if rows[row]['call_type'] == 'up':
            __dict['up'].append({'file':rows[row]['file'], 'start':rows[row]['starttime_since_startrec_sec'], 'score':rows[row]['score']}) 
        if rows[row]['call_type'] == 'gs':
            __dict['gs'].append({'file':rows[row]['file'], 'start':rows[row]['starttime_since_startrec_sec'], 'score':rows[row]['score']})

    return __dict

_dict['D1'] = extract('D1', D1_Rows)
_dict['D2'] = extract('D2', D2_Rows)


def extract_calls (__dict, folderpath):
    # i = 0
    # for index in __dict['up']:
    #     print(i)
    #     extract_call(index, folderpath, 'up', i)
    #     i+=1

    i = 0
    for index in __dict['gs']:
        print(i)
        extract_call(index, folderpath, 'gs', i)
        i+=1

def extract_call(index, folderpath, label, i):
    filepath = folderpath + '/' + index['file'] #[:-4] + '_demux.wav'
    if os.path.exists(filepath):
        wav = librosa.load(filepath, sr=1000, mono=True)
        start_sample = int((index['start']+1.2) * 1000)
        end_sample = start_sample + (3 * 1000)
        audio = wav[0][start_sample:end_sample]
        f, t, _spectrogram = Spectrogram.create_spectrgram_from_bufer(audio, 1000)
        _spectrogram_log = 10 * np.log10(_spectrogram)
        _denoised_spectrogram = Spectrogram().denoise_median(_spectrogram_log)
        #Spectrogram.plot_spectrogram(t, f, _denoised_spectrogram, 0, 500)
        directory_name = out_folder_path +'/'+ label, '/'+label+'_call_'+str(i)+'.png'

        if not os.path.exists(directory_name[0]):
            # Create the directory
            os.makedirs(directory_name[0])

        Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, directory_name[0], directory_name[1], 0, 500)      

#out_folder_path = r'E:\Thesis\Datasets\051023_DCLDE2024\D2'
#extract_calls(_dict['D2'], D2_folder_path)

out_folder_path = r'E:\Thesis\Datasets\051023_DCLDE2024\D1'
extract_calls(_dict['D1'], D1_folder_path)

Done()