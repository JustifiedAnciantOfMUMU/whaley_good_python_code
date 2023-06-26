import numpy as np, matplotlib.pyplot as plt, scipy.io.wavfile as wavfile
from scipy.signal import spectrogram

class Spectogram():
    def __init__(self, audio_filepath) -> None:
        f, t, spectrogram_data = self.create_spectrgram(audio_filepath)
        spectrogram_data_log = 10 * np.log10(spectrogram_data)

    @staticmethod
    def create_spectrgram(audio_filepath, window_size=0.256, nfft=3050):
        sample_rate, audio_data = wavfile.read(audio_filepath)

        nperseg = int (window_size * sample_rate)
        noverlap = (nperseg * 0.88)
        window = np.hamming(nperseg)
        return spectrogram(audio_data, fs=sample_rate, window=window, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
    
    @staticmethod
    def denoise_median():
        median = np.median(spectrogram_data_log)
        spectrogram_data_median = spectrogram_data_log - median #subtract medium of spectogram 
        for freq_band in spectrogram_data_median:
            median = np.median(freq_band)  
            freq_band = freq_band - median   

    @staticmethod
    def plot_spectrogram(t, f, spectrogram_data):
        plt.figure()
        plt.pcolormesh(t, f, spectrogram_data, shading='auto')
        plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
        plt.ylim(0, 400)
        plt.colorbar(label='Power Spectral Density (dB/Hz)')
        plt.title('Spectrogram')

if __name__ == '__main__':
    # Load the audio file
    wav_file_path = r'C:\Users\Jon\Documents\UNI\Thesis\code\Test Calls\moan_ex1.wav'
    #wav_file_path = r'C:\Users\Jon\Documents\UNI\Thesis\code\Test Calls\up_ex2.wav'
    wav_file_path = r'C:\Users\Jon\Documents\UNI\Thesis\code\Test Calls\A_1770.wav'
    sample_rate, audio_data = wavfile.read(wav_file_path)

    window_size = 0.256
    nfft = 3050
    nperseg = int (window_size * sample_rate)
    noverlap = (nperseg * 0.88)
    window = np.hamming(nperseg)
    f, t, spectrogram_data = spectrogram(audio_data, fs=sample_rate, window=window, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

    spectrogram_data_log = 10 * np.log10(spectrogram_data)
    plt.figure()
    plt.pcolormesh(t, f, spectrogram_data_log, shading='auto')
    plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
    plt.ylim(0, 400)
    plt.colorbar(label='Power Spectral Density (dB/Hz)')
    plt.title('Spectrogram')
    #plt.show()

    """median denoising"""
    median = np.median(spectrogram_data_log)
    spectrogram_data_median = spectrogram_data_log - median #subtract medium of spectogram 
    for freq_band in spectrogram_data_median:
        median = np.median(freq_band)  
        freq_band = freq_band - median   

    plt.figure()
    plt.pcolormesh(t, f, np.clip(spectrogram_data_median, 0, None), shading='auto')
    plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
    plt.ylim(0, 400)
    plt.colorbar(label='Power Spectral Density (dB/Hz)')
    plt.title('Spectrogram - median')
    #plt.show()

    """PCEN denoising"""
    s = 0.025 # smoothing coefficent
    M = spectrogram_data_log
    epsilon = 10**-6 # small arbitary constant
    alpha = 0.1     # gain strength 0-1
    r = 0.5
    delta = 2

    for freq_band in M:
          # smoothed frequency band
        for i in range(len(freq_band)):
            x = (1-s)*freq_band[i-1]
            y = s*freq_band[i]
            freq_band[i] = x + y
        
    G = spectrogram_data_log / np.power((M + epsilon), alpha)

    PCEN = (G + delta)**r - delta**r

    plt.figure()
    plt.pcolormesh(t, f, PCEN, shading='auto')
    plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
    plt.ylim(0, 400)
    plt.colorbar(label='Power Spectral Density (dB/Hz)')
    plt.title('Spectrogram - PCEN')
    plt.show()


    

    print('done')