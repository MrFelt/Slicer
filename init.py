import os
import subprocess
import sys
import logging
import shutil

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

    directory_path = None

    if len(sys.argv) == 2:
        directory_path = sys.argv[1]
        if not os.path.isdir(directory_path):
            print("Invalid directory path.")
            return
    else:
        directory_path = input("Please enter the directory path: ")
        if not os.path.isdir(directory_path):
            print("Invalid directory path.")
            return

    audio_files = find_audio_files(directory_path)

    if not audio_files:
        print("No audio files found in the given directory.")
        return

    # Create a temp folder within the project directory
    temp_folder = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_folder, exist_ok=True)

    python_interpreter = sys.executable

    try:
        logging.info(f'Running resample.py on {audio_files}')
        resample_script = "resample.py"
        subprocess.run([python_interpreter, resample_script] + audio_files)

        logging.info('Running whisper.py')
        whisper_script = "whisper.py"
        subprocess.run([python_interpreter, whisper_script])

        logging.info('Running split.py')
        split_script = "split.py"
        subprocess.run([python_interpreter, split_script])

        logging.info('Processing completed.')
    finally:
        shutil.rmtree(temp_folder)  # Cleanup temp directory


if __name__ == "__main__":
    main()
