from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from datetime import datetime
import logging

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

current_time_log = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_directory, f'split_log_{current_time_log}.txt')

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def split_at_quietest_point(segment, window_len=10):
    quietest_avg = float('inf')
    quietest_point = 0
    for i in range(0, len(segment) - window_len, window_len):
        window = segment[i:i + window_len]
        window_avg = window.dBFS
        if window_avg < quietest_avg:
            quietest_avg = window_avg
            quietest_point = i

    # Check to avoid an indefinite loop
    if quietest_point == 0 or quietest_point == len(segment):
        return segment, AudioSegment.silent(duration=0)

    return segment[:quietest_point], segment[quietest_point:]


def split_audio(file_path, output_folder, segment_counter):
    logging.info(f'Loading audio file: {file_path}')
    audio = AudioSegment.from_file(file_path)
    logging.info(f'Loaded audio file with length: {len(audio) / 1000:.3f} seconds')

    logging.info('Splitting on silence')
    segments = split_on_silence(
        audio,
        min_silence_len=175,
        silence_thresh=-35
    )

    logging.info(f'Found {len(segments)} segments')
    if not segments:
        logging.warning('No segments found for splitting')
        return segment_counter

    for segment in segments:
        logging.info(f'Processing segment with original length: {len(segment) / 1000:.3f} seconds')

        # Pad segments shorter than 1 second with silence
        if len(segment) < 1000:
            segment += AudioSegment.silent(duration=1000 - len(segment))
            logging.info(f'Padded segment to length: {len(segment) / 1000:.3f} seconds')

        # Split segments longer than 3.7 seconds
        while len(segment) > 3700:
            segment_part1, segment = split_at_quietest_point(segment)
            segment_path = os.path.join(output_folder, f'segment_{segment_counter}.wav')
            logging.info(f'Saving segment {segment_counter} to {segment_path} with length {len(segment_part1) / 1000:.3f} seconds')
            segment_part1.export(segment_path, format="wav")
            segment_counter += 1

        # Save final part of the segment
        if 1000 <= len(segment) <= 3700:
            segment_path = os.path.join(output_folder, f'segment_{segment_counter}.wav')
            logging.info(f'Saving segment {segment_counter} to {segment_path} with length {len(segment) / 1000:.3f} seconds')
            segment.export(segment_path, format="wav")
            segment_counter += 1

    return segment_counter

def main():
    logging.info('Starting split process')
    input_directory = os.path.join(os.getcwd(), "temp", "whisper_output")
    original_folder_name = os.path.basename(os.path.normpath(input_directory))
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder_name = f"{original_folder_name}_{current_time}"
    output_directory = os.path.join(os.getcwd(), "outputs", output_folder_name)
    os.makedirs(output_directory, exist_ok=True)

    # Find all audio files in the input directory recursively
    audio_files = [os.path.join(root, file) for root, dirs, files in os.walk(input_directory) for file in files if
                   file.endswith(('.wav', '.flac', '.mp3'))]

    logging.info(f'Found {len(audio_files)} audio files')

    segment_counter = 1
    for audio_file in audio_files:
        segment_counter = split_audio(audio_file, output_directory, segment_counter)

    logging.info('Split process completed')

if __name__ == "__main__":
    main()