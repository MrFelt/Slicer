import os
import subprocess
import sys
import logging
from datetime import datetime

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

current_time_log = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_directory, f'init_log_{current_time_log}.txt')

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,  # DEBUG level for extensive logging
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

    # Check for directory argument or ask for input
    directory_path = sys.argv[1] if len(sys.argv) == 2 else input("Please enter the directory path: ")

    if not os.path.isdir(directory_path):
        logging.error("Invalid directory path provided.")
        print("Invalid directory path.")
        return

    audio_files = find_audio_files(directory_path)
    if not audio_files:
        logging.warning("No audio files found.")
        print("No audio files found.")
        return

    # Temp folder setup
    temp_folder = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_folder, exist_ok=True)

    python_interpreter = sys.executable

    try:
        # Run scripts
        logging.info(f'Running resample.py on {audio_files}')
        subprocess.run([python_interpreter, "resample.py"] + audio_files)

        logging.info('Running whisper.py')
        subprocess.run([python_interpreter, "whisper.py"])

        logging.info('Running split.py')
        subprocess.run([python_interpreter, "split.py"])

        logging.info('Processing completed.')
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Uncomment to clean temp folder
    # finally:
    #     shutil.rmtree(temp_folder)
    #     logging.info('Temp folder cleaned up.')


if __name__ == "__main__":
    main()
