import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np, random, math, librosa

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot
from Libs.Files.Excel_import import ExcelFile

D1_folder_path = r'E:\Thesis\DCLDE 2024\30July2018'
D2_folder_path = r'E:\Thesis\DCLDE 2024\31July2018'
export_path = r'E:\Thesis\Datasets\051023_DCLDE2024'


D1_Rows = ExcelFile().extract_rows_from_sheet('annotations 7-30', r'E:/Thesis/DCLDE 2024/annotations.xlsx')
D2_Rows = ExcelFile().extract_rows_from_sheet('annotations 7-31', r'E:/Thesis/DCLDE 2024/annotations.xlsx')

_dict = {}
i = 0

def extract(day_label, rows):
    __dict = {}
    gaps_dict = {}
    for row in rows:
        __dict[rows[row]['file']] = []
    for row in rows:
        __dict[rows[row]['file']].append(math.floor(float(rows[row]['starttime_since_startrec_sec']) + 1.2))

    for file in __dict:
        list.sort(__dict[file])

        gaps_dict[file] = []
        s = 0
        for i in range(len(__dict[file])):
            if (__dict[file][i] - s) > 3:
                gaps_dict[file].append({'start':s, 'end':__dict[file][i]})
            s = __dict[file][i] + 4

    return gaps_dict


def extract_audio(gaps, num, folder_path):
    all_gaps = []
    for file in gaps:
        for gap in gaps[file]:
            intervals = (gap['end'] - gap['start']) % 3
            for interval in range(intervals):
                all_gaps.append({'file':file, 'start':(gap['start']+(3*interval))})

    for i in range(num):

        random_index = random.randint(0, len(all_gaps) - 1)
        random_element = all_gaps.pop(random_index)
        
        audio_filepath = folder_path + '/' + random_element['file'][:-4] + '_demux.wav'
        
        #sample_rate, audio_data = wavfile.read(audio_filepath)
        audio, sample_rate = librosa.load(audio_filepath, sr=1000)
        seg_length = 3 * sample_rate
        start_sample = int(random_element['start']) * sample_rate
        end_sample = int(start_sample + (seg_length))
        buffer = audio[start_sample:end_sample]
        # mono_buffer = []
        # for sample in range(len(buffer)):
        #     mono_buffer.append(buffer[sample][0])

        save_file_name = r'\Nocall_' + str(i+105+212+232+66+146) + '_0.wav' 
        # wav_file = wave.open(export_path + label + save_file_name, 'wb')
        # wav_file.setnchannels(1)  # Mono audio
        # wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
        # wav_file.setframerate(sample_rate)
        # wav_file.writeframes(buffer)
        # wav_file.close()

        f, t, _spectrogram = Spectrogram().create_spectrgram_from_bufer(buffer, sample_rate, 0.256)
        _spectrogram_log = 10 * np.log10(_spectrogram)
        _denoised_spectrogram = Spectrogram().denoise_median(_spectrogram_log)
        spec_filename = save_file_name[:-4] + '.png'
        Spectrogram().save_spectrogram(t, f, _denoised_spectrogram, 
                                       export_path,
                                       spec_filename)
        

        print(i)







# gaps = extract('D1', D1_Rows)
# label = r'\D1\\'
# extract_audio(gaps, 311, D1_folder_path)


gaps = extract('D2', D2_Rows)
label = r'\D2\\'
extract_audio(gaps, 703-213-232-66-146, D2_folder_path)

Done()