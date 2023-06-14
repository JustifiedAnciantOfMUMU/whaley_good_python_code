import librosa, scipy.io.wavfile as wavfile, numpy as np, matplotlib.pyplot as plt
from scipy.signal import spectrogram



# Example usage
wav_file_path = r'C:\Users\Jon\Documents\UNI\Thesis\code\Test Calls\gunshot_ex1.wav'
sample_rate, audio_data = wavfile.read(wav_file_path)

window_size = 0.256
nfft = 3050
nperseg = int (window_size * sample_rate)
noverlap = (nperseg * 0.88)
window = np.hamming(nperseg)
f, t, spectrogram_data = spectrogram(audio_data, fs=sample_rate, window=window, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

spectrogram_data_log = 10 * np.log10(spectrogram_data)
pcen_spectrogram = librosa.pcen(spectrogram_data_log, sr=sample_rate, hop_length=(sample_rate * 0.256), gain=0.98, eps= 10**-6, power=0.0)

plt.figure()
plt.pcolormesh(t, f, np.clip(pcen_spectrogram, 0, None), shading='auto')
plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
plt.ylim(0, 400)
plt.colorbar(label='Power Spectral Density (dB/Hz)')
plt.title('Spectrogram - PCEN')
plt.show()

print('done')