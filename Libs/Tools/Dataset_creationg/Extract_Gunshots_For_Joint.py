import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot

config_dict = ConfigDict().dict

audio_ds_filepath = r'E:\Thesis\Datasets\230904_Combined\Audio'
spectrogram_ds_filepath = r'E:\Thesis\Datasets\230904_Combined\Spectrograms'

files = [f for f in os.listdir(config_dict['NOPP_Gunshot_data']) if f.endswith('.mat')]
_dict = {}
duration_max=0

for file in files:
    _dict[file], duration = NOPP_mat_import(config_dict['NOPP_Gunshot_data'] + "/" + file)
    duration_max = max(duration_max, duration)

events = []
for file in files:
    
    for i in range(1, len(_dict[file])):
        try:
            x = _dict[file]
            event = x[i]
            h, m, s = event.split(':')
            m_rounded = (int(m) // 15) * 15
            time_into_file = ((int(m) - m_rounded)*60) + int(s)
            dict_entry = {'file_timestamp':h+str(m_rounded).zfill(2)+'00', 'time_into_file':time_into_file, 'duration':duration_max, 'file_name' : file}
            events.append(dict_entry)
        except:
            pass

i=0
log = []
for event in events:
    audio_filepath = config_dict['NOPP_Gunshot_data'] + r'/SBNMS_' + event['file_name'][6:14] + '_' + event['file_timestamp'] + '.wav'
    sample_rate, audio_data = wavfile.read(audio_filepath)
    start_sample = event['time_into_file'] * sample_rate
    end_sample = int(start_sample + (3 * sample_rate))
    buffer = audio_data[start_sample:end_sample]



    filename = 'gunshot_' + str(i) + '_1.wav'
    wav_file = wave.open(audio_ds_filepath+ r'/all/' +filename, 'wb')
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(buffer)
    wav_file.close()
    print(str(i+1) +'/'+ str(len(events)))

    spec = Spectrogram().create_spectrgram_from_bufer(buffer, sample_rate)
    Spectrogram().save_spectrogram(spec[1], spec[0], spec[2], 
                                       spectrogram_ds_filepath + r'/all/', filename[:-4]+'.png', 
                                       0, 500)
    i+=1