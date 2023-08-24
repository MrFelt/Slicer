import librosa
import numpy as np
import os

def split_audio(file_path, output_folder):
    # Load audio file
    y, sr = librosa.load(file_path, sr=None)

    # Segment analysis
    window_length = int(sr * 0.01)  # 10ms window
    avg_volumes = [np.mean(np.abs(y[i:i+window_length])) for i in range(0, len(y), window_length)]

    # Find quietest parts and split
    min_length = sr * 1  # 1 second
    max_length = sr * 3.7  # 3.7 seconds
    start_idx = 0
    for i, volume in enumerate(avg_volumes[:-1]):
        if volume < avg_volumes[i + 1] and (i + 1) * window_length - start_idx > min_length:
            split_audio = y[start_idx:(i + 1) * window_length]
            if len(split_audio) < min_length:  # Add silence padding
                padding = np.zeros(min_length - len(split_audio))
                split_audio = np.concatenate((split_audio, padding))
            librosa.output.write_wav(os.path.join(output_folder, f'split_{i}.wav'), split_audio, sr)
            start_idx = (i + 1) * window_length

    # Write the remaining part
    split_audio = y[start_idx:]
    if len(split_audio) < min_length:  # Add silence padding
        padding = np.zeros(min_length - len(split_audio))
        split_audio = np.concatenate((split_audio, padding))
    librosa.output.write_wav(os.path.join(output_folder, 'split_last.wav'), split_audio, sr)

def main():
    input_folder = os.path.join("temp_folder", "whisper_output")
    output_folder = os.path.join("outputs", "split_audio")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.wav', '.flac', '.mp3')):
            file_path = os.path.join(input_folder, filename)
            split_audio(file_path, output_folder)

if __name__ == "__main__":
    main()
