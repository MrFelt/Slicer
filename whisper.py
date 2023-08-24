import os
import logging
import torch
import soundfile as sf
from faster_whisper import WhisperModel
from glob import glob

logging.basicConfig(level=logging.INFO)

# Check for CUDA device
if torch.cuda.is_available():
    device = "cuda"
    logging.info(f"CUDA device found: {torch.cuda.get_device_name()}")
else:
    response = input("No CUDA device found, would you like to run CPU inference? (Y/N): ").strip().lower()
    if response == 'y':
        device = "cpu"
        logging.info("Using CPU for inference.")
    else:
        logging.info("Exiting the script.")
        exit(0)


def process_audio(audio_path, output_folder):
    model_name = "large-v2"  # Define the model name
    mtypes = {'cpu': 'int8', 'cuda': 'float16'}

    logging.info(f"Processing audio file {audio_path}")
    logging.info(f"Using device: {device}")

    # Initialize Whisper model using the model name
    logging.info(f"Loading Whisper model {model_name}")
    whisper_model = WhisperModel(model_name, device=device, compute_type=mtypes[device])

    # Transcribe the audio to get segments
    logging.info("Transcribing audio to get segments")
    segments, _ = whisper_model.transcribe(audio_path, beam_size=1, word_timestamps=True)

    # Read the audio file
    logging.info("Reading audio file")
    audio, sample_rate = sf.read(audio_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through segments and create audio files
    logging.info("Creating audio segments")
    for i, segment in enumerate(segments):
        start_time = int(segment.start * sample_rate)  # Accessing attributes directly
        end_time = int(segment.end * sample_rate)
        segment_audio = audio[start_time:end_time]
        segment_path = os.path.join(output_folder, f"segment_{i}.wav")
        sf.write(segment_path, segment_audio, sample_rate)
        logging.info(f"Exported segment {i} to {segment_path}")

    # Clear GPU memory
    logging.info("Clearing GPU memory")
    del whisper_model
    torch.cuda.empty_cache()


def main(input_directory=None):
    if input_directory is None:
        input_directory = input("Please enter the input directory: ")

    logging.info(f"Input directory: {input_directory}")

    # Create output directory inside input directory
    output_directory = os.path.join(input_directory, "output_segments")
    os.makedirs(output_directory, exist_ok=True)

    # Find all audio files in the input directory (.wav, .flac, .mp3)
    audio_files = []
    for ext in ['*.wav', '*.flac', '*.mp3']:
        audio_files.extend(glob(os.path.join(input_directory, ext)))

    logging.info(f"Found {len(audio_files)} audio files")

    # Process each audio file
    for audio_file in audio_files:
        process_audio(audio_file, output_directory)


if __name__ == "__main__":
    main()
