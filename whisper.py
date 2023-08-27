import os
import logging
import torch
import soundfile as sf
from faster_whisper import WhisperModel
from glob import glob
from datetime import datetime

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

current_time_log = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = os.path.join(log_directory, f'whisper_log_{current_time_log}.txt')

logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Check for CUDA device
device = "cuda" if torch.cuda.is_available() else "cpu"

if device == "cuda":
    logging.info(f"CUDA device found: {torch.cuda.get_device_name()}")
else:
    response = input("No CUDA device found. Continue with CPU? (Y/N): ").strip().lower()
    if response != 'y':
        logging.info("Exiting.")
        exit(0)

def process_audio(audio_path, output_folder):
    model_name = "large-v2"
    mtypes = {'cpu': 'int8', 'cuda': 'float16'}

    logging.info(f"Processing {audio_path} on {device}")
    whisper_model = WhisperModel(model_name, device=device, compute_type=mtypes[device])

    segments, _ = whisper_model.transcribe(
        audio_path,
        vad_filter=True,
        vad_parameters=dict(
            threshold=0.90,
            min_silence_duration_ms=80,
            min_speech_duration_ms=1000,
            speech_pad_ms=10,
            window_size_samples=512
        ),
        beam_size=5
    )

    audio, sample_rate = sf.read(audio_path)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file_name = os.path.basename(audio_path)
    audio_file_base_name, _ = os.path.splitext(audio_file_name)
    unique_output_folder = os.path.join(output_folder, f"{audio_file_base_name}_{current_time}")
    os.makedirs(unique_output_folder, exist_ok=True)

    for i, segment in enumerate(segments):
        start_time = int(segment.start * sample_rate)
        end_time = int(segment.end * sample_rate)
        segment_audio = audio[start_time:end_time]
        segment_path = os.path.join(unique_output_folder, f"segment_{i}.wav")
        sf.write(segment_path, segment_audio, sample_rate, subtype='PCM_32')  # 32-bit WAV
        logging.info(f"Exported segment {i} to {segment_path}")

    del whisper_model
    torch.cuda.empty_cache()

def main():
    input_directory = os.path.join(os.getcwd(), "temp", "resample")
    if not os.path.exists(input_directory) or not os.listdir(input_directory):
        input_directory = input("Please enter the input directory: ")

    output_directory = os.path.join(os.getcwd(), "temp", "whisper_output")
    os.makedirs(output_directory, exist_ok=True)

    audio_files = []
    for ext in ['*.wav', '*.flac', '*.mp3']:
        audio_files.extend(glob(os.path.join(input_directory, ext)))

    logging.info(f"Found {len(audio_files)} audio files")

    for audio_file in audio_files:
        process_audio(audio_file, output_directory)

if __name__ == "__main__":
    main()
