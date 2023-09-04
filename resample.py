import os
import subprocess
import sys
import json
import concurrent.futures
import logging
from datetime import datetime

# Set up logging
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

current_time_log = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_directory, f'resample_log_{current_time_log}.txt')

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,  # DEBUG level for extensive logging
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_audio_info(input_audio):
    # Use ffprobe to get audio information
    command = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        input_audio
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = process.communicate()
    audio_info = json.loads(output)

    # Extract audio properties
    audio_stream = audio_info['streams'][0]
    sample_fmt = audio_stream.get('sample_fmt', '')
    sample_rate = int(audio_stream.get('sample_rate', 0))
    codec_name = audio_stream.get('codec_name', '')
    bit_depth = audio_stream.get('bits_per_raw_sample', '')

    return sample_fmt, sample_rate, codec_name, bit_depth


def should_skip_resampling(sample_rate, codec_name, bit_depth):
    # Conditions for skipping resampling
    if sample_rate == 48000 and (
            (codec_name == 'flac' and bit_depth == '24') or
            (codec_name == 'pcm_s32le' and bit_depth in ['24', '32']) or
            (codec_name == 'pcm_s24le' and bit_depth == '24')
    ):
        return True
    return False


def resample_audio(input_audio, output_folder):
    logging.info(f'Starting resampling for {input_audio}')

    sample_fmt, sample_rate, codec_name, bit_depth = get_audio_info(input_audio)

    if should_skip_resampling(sample_rate, codec_name, bit_depth):
        logging.info(f'Skipping resampling for {input_audio}')
        return

    # Otherwise, perform resampling
    output_file = os.path.join(output_folder, "resampled_" + os.path.basename(input_audio))
    try:
        command = [
            "ffmpeg", "-i", input_audio, "-ar", "48000", "-ac", "1", "-c:a", "flac",
            "-sample_fmt", "s32", "-b:a", "256k", output_file
        ]
        subprocess.run(command, check=True)
        logging.info(f"Resampled: {input_audio}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error resampling {input_audio}: {e}")


def main():
    logging.info('Initiating resampling process')

    if len(sys.argv) < 2:
        logging.warning("Usage: python resample.py <audio_file1> [<audio_file2> ...]")
        print("Usage: python resample.py <audio_file1> [<audio_file2> ...]")
        return

    input_audio_files = sys.argv[1:]

    cpu_count = os.cpu_count()
    max_workers = int((cpu_count / 2) * 0.4)  # Calculate max_workers based on CPU thread count
    max_workers = max(max_workers, 1)  # Ensure at least 1 worker

    logging.info(f'Starting resampling with {max_workers} workers')

    output_folder = os.path.join(os.getcwd(), "temp", "resample")
    os.makedirs(output_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for input_audio in input_audio_files:
            executor.submit(resample_audio, input_audio, output_folder)

    logging.info('Resampling process completed')


if __name__ == "__main__":
    main()
