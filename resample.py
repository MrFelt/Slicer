import os
import subprocess
import sys
import concurrent.futures
import logging

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    filename=os.path.join(log_directory, 'resample.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def resample_audio(input_audio, output_folder):
    logging.info(f'Starting resampling for {input_audio}')

    # Output file path
    output_file = os.path.join(output_folder, "resampled_" + os.path.basename(input_audio))

    try:
        # Using FFmpeg to resample and convert to FLAC format
        command = [
            "ffmpeg", "-i", input_audio, "-ar", "48000", "-ac", "1", "-c:a", "flac",
            "-sample_fmt", "s32", "-b:a", "256k", output_file
        ]
        subprocess.run(command, check=True)
        logging.info(f"Resampled: {input_audio}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error resampling {input_audio}: {e}")
        print(f"Error resampling {input_audio}: {e}")


def main():
    logging.info('Initiating resampling process')

    if len(sys.argv) < 2:
        print("Usage: python resample.py <audio_file1> [<audio_file2> ...]")
        return

    input_audio_files = sys.argv[1:]

    cpu_count = os.cpu_count()
    max_workers = int((cpu_count / 2) * 0.4)  # Calculate max_workers based on CPU thread count
    max_workers = max(max_workers, 1)  # Ensure at least 1 worker

    logging.info(f'Starting resampling with {max_workers} workers')

    # Output folder
    output_folder = os.path.join(os.getcwd(), "temp", "resample")
    os.makedirs(output_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for input_audio in input_audio_files:
            executor.submit(resample_audio, input_audio, output_folder)  # Pass output folder

    logging.info('Resampling process completed')


if __name__ == "__main__":
    main()
