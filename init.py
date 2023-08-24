import os
import subprocess
import sys
import logging

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'init.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_audio_files(directory):
    logging.info(f'Searching for audio files in {directory}')
    audio_extensions = ['.mp3', '.wav', '.flac']
    audio_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            _, extension = os.path.splitext(file)
            if extension.lower() in audio_extensions:
                audio_files.append(os.path.join(root, file))

    logging.info(f'Found {len(audio_files)} audio files')
    return audio_files

def main():
    logging.info('Initiating the process')

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
        logging.info(f'Running resample.py on {audio_file}')
        subprocess.run(["python", resample_script, audio_file])

        resampled_audio_file = os.path.join(os.path.dirname(audio_file),
                                            "resampled_" + os.path.basename(audio_file))
        logging.info(f'Running whisper.py on {resampled_audio_file}')
        whisper_script = "whisper.py"
        subprocess.run(["python", whisper_script, resampled_audio_file])

if __name__ == "__main__":
    main()
