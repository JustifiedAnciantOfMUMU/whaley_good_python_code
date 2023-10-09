import os
import wave

# Directory containing .wav files
directory_path = r'E:\Thesis\Datasets\231004_Gunshot_datasets\audio\val\call'  # Replace with the path to your directory

# Loop through the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".wav"):
        # Create the full file path
        file_path = os.path.join(directory_path, filename)
        
        try:
            # Open the .wav file and get the number of frames (samples)
            with wave.open(file_path, 'rb') as wav_file:
                num_frames = wav_file.getnframes()
                if num_frames != 1000:
                    print(f"File: {filename}, Number of Samples: {num_frames}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
