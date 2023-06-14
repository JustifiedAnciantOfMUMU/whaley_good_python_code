import numpy as np, matplotlib.pyplot as plt, scipy.io.wavfile as wavfile
from scipy.signal import spectrogram

class SpectrogramBase:
    def create_spectrogram(self, audio_data, sample_rate, window_size = 0.256):
        nfft = 3050
        nperseg = int (window_size * sample_rate)
        noverlap = (nperseg * 0.88)
        window = np.hamming(nperseg)

        f, t, spectrogram_data = spectrogram(audio_data, fs=sample_rate, window=window, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
        return t, f, spectrogram_data

    def plot_spectrogram(self, spectrogram_data, t, f, title='Spectrogram'):
        spectrogram_data_log = 10 * np.log10(spectrogram_data)
        plt.figure()
        plt.pcolormesh(t, f, spectrogram_data_log, shading='auto')
        plt.xlabel('Time (s)'), plt.ylabel('Frequency (Hz)')
        plt.colorbar(label='Power Spectral Density (dB/Hz)')
        plt.title('Spectrogram')
        plt.show()

    @staticmethod
    def denoise_spectrogram(spectrogram_data, method='PCEN'):
        pass
        #subtract medium of each frequency

    @staticmethod
    def PCEN(spectrogram):
        E = 0 # filter bank energy
        m = 0 # smoothed version of filter bank energy
        epsolon = 10^-6
        s = 0 #smoothing coefficient
        alpha = 0
        delta = 0
        r = 0


    def median_normilisation(spectrogram_data):
        median = np.median(spectrogram_data)
        spectrogram_data = spectrogram_data - median #subtract medium of spectogram
        for frequency_band in spectrogram:
            frequency_band = frequency_band - np.median(frequency_band)
        return spectrogram_data


class WavSpectrogram(SpectrogramBase):
    def __init__(self, wav_filepath):
        self.wav_filepath = wav_filepath
        self.sample_rate, self.audio_data = wavfile.read(wav_filepath)
    
    def generate_and_plot_spectrogram(self, reduce_noise=True):
        t, f, spectrogram_data = self.create_spectrogram(self.audio_data, self.sample_rate)
        #if reduce_noise == True: spectrogram_data = self.denoise_spectrogram(spectrogram_data)
        self.plot_spectrogram(t, f, spectrogram_data, title='Spectrogram of {}'.format(self.wav_filepath))

        return spectrogram_data


if __name__ == '__main__':
    # Load the audio file
    wav_file_path = r'C:\Users\Jon\Documents\UNI\Thesis\code\Test Calls\up_ex1.wav'
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