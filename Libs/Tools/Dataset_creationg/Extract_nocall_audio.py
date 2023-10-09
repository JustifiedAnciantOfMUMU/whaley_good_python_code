import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np, random

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot

config_dict = ConfigDict().dict

max_length = 2.7
sample_rate = 2000
out_length = 3
out_num = 4000
export_filepath = r'E:\Thesis\Datasets\230904_Combined\audio\all\nocall' 

files = [f for f in os.listdir(config_dict['NOPP_Gunshot_data']) if f.endswith('.mat')]
_dict = {}
duration_max=0

for file in files:
    _dict[file], duration = NOPP_mat_import(config_dict['NOPP_Gunshot_data'] + "/" + file)
    duration_max = max(duration_max, duration)



dict = {}
for file in files:
    for i in range(1, len(_dict[file])):
        try:
            x = _dict[file]
            event = x[i]
            h, m, s = event.split(':')
            m_rounded = (int(m) // 15) * 15
            if (file +h+str(m_rounded).zfill(2)+'00') not in dict:
                dict[file +h+str(m_rounded).zfill(2)+'00'] = []

            dict[file + h+str(m_rounded).zfill(2)+'00'].append(((int(m) - m_rounded)*60) + int(s))
        except:
            pass 

for e in dict:
    dict[e] = sorted(dict[e])


segments = 3000
seg_length = out_length * sample_rate
sections_dict = {}

for e in dict:
    sections = []
    start = 0
    for i in range(len(dict[e])):
        sections.append({'start_second':start, 'end_second': dict[e][i]})
        start = dict[e][i] + 2.7
    sections_dict[e] = sections

all_sections = []
step = 5

for e in sections_dict:
    for i in sections_dict[e]:
        start = i['start_second']
        while (start + step) < i['end_second']:
            all_sections.append({'file':e, 'start_second':start})
            start += step
        
i = 0

while i < out_num:
    random_index = random.randint(0, len(all_sections) - 1)
    random_element = all_sections.pop(random_index)

    audio_filepath = config_dict['NOPP_Gunshot_data'] + r'/SBNMS_' +(random_element['file'][:-6])[6:14] + '_' + random_element['file'][-6:] + '.wav'
    sample_rate, audio_data = wavfile.read(audio_filepath)
    start_sample = int(random_element['start_second']) * sample_rate
    end_sample = int(start_sample + (seg_length))
    buffer = audio_data[start_sample:end_sample]

    save_file_name = r'\Nocall_' + str(i) + '_0.wav' 
    wav_file = wave.open(export_filepath + save_file_name, 'wb')
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(buffer)
    wav_file.close()

    spec = Spectrogram().create_spectrgram_from_bufer(buffer, sample_rate)
    cd = []
    for ind in spec[2]:
        cd.append(ind[12:29])
    spec_filename = save_file_name[:-4] + '.png'
    Spectrogram().save_spectrogram(spec[1][12:29], spec[0], cd, 
                                   r'E:\Thesis\Datasets\230904_Combined\Spectrograms\all\no_call',
                                   spec_filename, 200, 1000)
    i+=1

Done()