import os
import wave

# Directory containing WAV files
input_directory = r'E:\Thesis\Datasets\230903_Gunshot_datasets\audio\val\nocall'  # Replace with the path to your directory
output_directory = r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\val\nocall'  # Replace with the path to your output directory

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".wav"):
        input_wav_file = os.path.join(input_directory, filename)
        output_wav_file = os.path.join(output_directory, filename)
        
        with wave.open(input_wav_file, 'rb') as wav_file:
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            audio_data = wav_file.readframes(-1)

        cropped_audio_data = audio_data[:1000 * num_channels * sample_width]

        with wave.open(output_wav_file, 'wb') as wav_file:
            wav_file.setnchannels(num_channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(frame_rate)
            wav_file.writeframes(cropped_audio_data)

        print(f'Cropped and saved to "{output_wav_file}"')