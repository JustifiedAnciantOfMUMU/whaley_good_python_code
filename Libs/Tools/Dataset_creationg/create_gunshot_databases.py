import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot

config_dict = ConfigDict().dict

audio_ds_filepath = r'E:\\Thesis/Datasets/230903_Gunshot_datasets/audio'
spectrogram_ds_filepath = r'E:\\Thesis/Datasets/230903_Gunshot_datasets/spectrograms'

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
    end_sample = int(start_sample + (event['duration']*sample_rate))
    buffer = audio_data[start_sample:end_sample]

    spec = Spectrogram().create_spectrgram_from_bufer(buffer, sample_rate)
    thresh = 250 #threshold index in array
    #Spectrogram().plot_spectrogram(spec[1], spec[0][thresh:], spec[2][:][thresh:])

    #square of time domain across spectrogram
    square = []
    for time in range(len(spec[1])):
        sum = 0
        for freq in spec[2][:][thresh:]:
            sum += freq[time]
        square.append(math.pow(sum, 2))
        
    #plot([spec[1]], [square], ['plot'], ['Time', 'power level'])
    peak_index = square.index(max(square))

    start_sample = int((spec[1][peak_index] - 0.2) * sample_rate)
    end_sample = start_sample + int(0.5 * sample_rate)
    buffer_cropped = buffer[start_sample:end_sample]

    filename = 'gunshot_' + str(i) + '_1.wav'
    wav_file = wave.open(audio_ds_filepath+ r'/all/' +filename, 'wb')
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(buffer_cropped)
    wav_file.close()
    print(str(i+1) +'/'+ str(len(events)))

    start_index = peak_index -4 
    end_index = peak_index + 12

    thresh = 100
    closest_index = 0
    for _i in range(1, len(spec[0])):
        if abs(spec[0][_i] - 100) < abs(spec[0][closest_index] - 100):
            closest_index = _i

    c_fb = []
    for fb in range(len(spec[2][closest_index:])):
        c_fb.append(spec[2][fb + closest_index][start_index:end_index])
    #Spectrogram().plot_spectrogram(spec[1][start_index:end_index], spec[0][closest_index:], c_fb)
    try:
        Spectrogram().save_spectrogram(spec[1][start_index:end_index], spec[0][closest_index:], c_fb, 
                                       spectrogram_ds_filepath + r'/all/', filename[:-4]+'.png', 
                                       spec[0][closest_index], spec[0][-1])
    except:
        pass
    i+=1
 
Done()
