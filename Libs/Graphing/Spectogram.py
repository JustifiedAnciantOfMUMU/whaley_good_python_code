import numpy as np, matplotlib.pyplot as plt, scipy.io.wavfile as wavfile 
from scipy.signal import spectrogram

class SpectrogramGenerator:
    def create_spectrogram(self, audio_data, sample_rate):
        f, t, spectrogram_data = spectrogram(audio_data, fs=sample_rate, window=('hamming', 0.256))
        return spectrogram_data
    
    def plot_spectrogram(self, spectrogram_data, title='Spectrogram'):
        plt.figure()
        plt.imshow(spectrogram_data, aspect='auto', cmap='inferno')
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()

class WavSpectrogramGenerator(SpectrogramGenerator):
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.sample_rate, self.audio_data = wavfile.read(wav_file)
    
    def generate_and_plot_spectrogram(self):
        spectrogram_data = self.create_spectrogram(self.audio_data, self.sample_rate)
        self.plot_spectrogram(spectrogram_data, title='Spectrogram of {}'.format(self.wav_file))

        return spectrogram_data


if __name__ == '__main__':
    # Load the audio file
    wav_file_path = 'path_to_your_wav_file.wav'
    spectrogram_generator = WavSpectrogramGenerator(wav_file_path)
    spectrogram_generator.generate_and_plot_spectrogram()



# class spectogram_base():
#     def generate_spectogram(self, waveform, sample_rate):
#         self.frequencies, self.times, self.spectrogram_data = spectrogram(waveform, sample_rate)

#     def plot_spectogram(self):
#         pass

#     def plot_spectogram_scipy(self):
#         # Convert power spectrogram to dB scale
#         spectrogram_data_db = 10 * np.log10(self.spectrogram_data)

#         # Display the spectrogram
#         plt.figure(figsize=(10, 4))
#         plt.imshow(spectrogram_data_db, aspect='auto', origin='lower', cmap='inferno')
#         plt.colorbar(format='%+2.0f dB')
#         plt.title('Spectrogram')
#         plt.xlabel('Time')
#         plt.ylabel('Frequency')
#         plt.show()

# class spectogram_wav(spectogram_base):
#     """Class to produce a spectogram from the filepath to a wave file"""
#     def __init__(self, file_path) -> None:
#         sample_rate, waveform = wavfile.read(file_path)
#         self.generate_spectogram(waveform, sample_rate)

# class spectogram_samples(spectogram_base):
#     """Class to produce the spectogram from a buffer of samples and their sample rate"""
#     def __init__(self, samples, sample_rate) -> None:
#         self.generate_spectogram(samples, sample_rate)
