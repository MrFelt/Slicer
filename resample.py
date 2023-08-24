import os
import subprocess
import sys
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

def resample_audio(input_audio, output_audio):
    logging.info(f'Starting resampling for {input_audio}')
    try:
        # Using FFmpeg to resample and convert to FLAC format
        command = [
            "ffmpeg", "-i", input_audio, "-ar", "48000", "-ac", "1", "-c:a", "flac",
            "-sample_fmt", "s32", "-b:a", "256k", output_audio
        ]
        subprocess.run(command, check=True)
        logging.info(f"Resampled: {input_audio} to {output_audio}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error resampling {input_audio}: {e}")
        print(f"Error resampling {input_audio}: {e}")

def main():
    logging.info('Initiating resampling process')

    if len(sys.argv) != 2:
        print("Usage: python resample.py <input_audio_file>")
        return

    input_audio_file = sys.argv[1]
    output_audio_file = os.path.join("temp_folder", "resample", "resampled_" + os.path.basename(input_audio_file))
    resample_audio(input_audio_file, output_audio_file)

    logging.info('Resampling process completed')

if __name__ == "__main__":
    main()
