import os
import subprocess
import sys
import whisper

def find_audio_files(directory):
    audio_extensions = ['.mp3', '.wav', '.flac']  # Add more extensions if needed
    audio_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in audio_extensions:
                audio_files.append(os.path.join(root, file))

    return audio_files


def main():
    if len(sys.argv) != 2:
        print("Usage: python main_script.py <directory_path>")
        return

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return

    audio_files = find_audio_files(directory_path)

    if not audio_files:
        print("No audio files found in the given directory.")
        return

        resample_script = "resample.py"

        for audio_file in audio_files:
            subprocess.run(["python", resample_script, audio_file])

            # Assuming the resample script generates a resampled audio file in the same directory
            resampled_audio_file = os.path.join(os.path.dirname(audio_file),
                                                "resampled_" + os.path.basename(audio_file))

            # Call whisper.py here
            whisper_script = "whisper.py"
            subprocess.run(["python", whisper_script, resampled_audio_file])

    if __name__ == "__main__":
        main()