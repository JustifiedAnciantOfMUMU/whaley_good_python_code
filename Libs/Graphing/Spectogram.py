import numpy as np, matplotlib.pyplot as plt, scipy.io.wavfile as wavfile 
from scipy.signal import spectrogram


class spectogram_base():
    def generate_spectogram(self, waveform, sample_rate):
        self.frequencies, self.times, self.spectrogram_data = spectrogram(waveform, sample_rate)

    def plot_spectogram(self):
        # Convert power spectrogram to dB scale
        spectrogram_data_db = 10 * np.log10(self.spectrogram_data)

        # Display the spectrogram
        plt.figure(figsize=(10, 4))
        plt.imshow(spectrogram_data_db, aspect='auto', origin='lower', cmap='inferno')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Spectrogram')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.show()

class spectogram_wav(spectogram_base):
    """Class to produce a spectogram from the filepath to a wave file"""
    def __init__(self, file_path) -> None:
        sample_rate, waveform = wavfile.read(file_path)
        self.generate_spectogram(waveform, sample_rate)

class spectogram_samples(spectogram_base):
    """Class to produce the spectogram from a buffer of samples and their sample rate"""
    def __init__(self, samples, sample_rate) -> None:
        self.generate_spectogram(samples, sample_rate)

# Load the audio file
file_path = "path/to/your/file.wav"
sample_rate, waveform = wavfile.read(file_path)

# Generate the spectrogram
