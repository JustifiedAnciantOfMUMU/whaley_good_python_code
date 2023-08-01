import sys, os, scipy.io.wavfile as wavfile, wave, math, numpy as np

sys.path.append(os.getcwd())
from Config.import_config import ConfigDict
from Libs.Files.mat_file import NOPP_mat_import
from Libs.Tools.Done import Done
from Libs.Graphing.Spectrogram import Spectrogram
from Libs.Graphing.plot import plot

config_dict = ConfigDict().dict
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
for event in events:
    audio_filepath = config_dict['NOPP_Gunshot_data'] + r'/SBNMS_' + event['file_name'][6:14] + '_' + event['file_timestamp'] + '.wav'
    sample_rate, audio_data = wavfile.read(audio_filepath)
    start_sample = event['time_into_file'] * sample_rate
    end_sample = int(start_sample + (event['duration']*sample_rate))
    buffer = audio_data[start_sample:end_sample]

    spec = Spectrogram().create_spectrgram_from_bufer(buffer, sample_rate)
    thresh = 250 #threshold index in array
    # Spectrogram().plot_spectrogram(spec[1], spec[0][thresh:], spec[2][:][thresh:])

    #square of time domain across spectrogram
    square = []
    for time in range(len(spec[1])):
        sum = 0
        for freq in spec[2][:][thresh:]:
            sum += freq[time]
        square.append(math.pow(sum, 2))
        
    #plot([spec[1]], [square], ['plot'], ['Time', 'power level'])
    peak_index = square.index(max(square))

    x=0
    try:
        while True:
            gradient = square[peak_index-(x-1)] - square[peak_index-x]
            x-=1
            if gradient > -1.4 or x == 0: break
    except:
        print(f'event {i} has failed')
        
    start_sample = int(spec[1][peak_index-x] * sample_rate)
    end_sample = int(start_sample + (0.5 * sample_rate))
    buffer_cropped = buffer[start_sample:end_sample]
    #spec = Spectrogram().create_spectrgram_from_bufer(buffer_cropped, sample_rate)
    #Spectrogram().plot_spectrogram(spec[1], spec[0], spec[2][:])

    filename = '/gunshot_' + str(i) + '_1.wav'
    wav_file = wave.open(config_dict['Gunshot_dataset']+filename, 'wb')
    wav_file.setnchannels(1)  # Mono audio
    wav_file.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(buffer_cropped)
    wav_file.close()
    print(str(i+1) +'/'+ str(len(events)))
    i+=1


Done()