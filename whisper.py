import sys
import os

def process_audio(audio_path, output_folder):
    import torch
    import soundfile as sf
    from faster_whisper import WhisperModel

    model_path = "models/whisper_medium.safetensors"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    mtypes = {'cpu': 'int8', 'cuda': 'float16'}

    print(f"Processing audio file {audio_path}")

    # Initialize Whisper model
    whisper_model = WhisperModel(model_path, device=device, compute_type=mtypes[device])

    # Transcribe the audio to get segments
    segments, _ = whisper_model.transcribe(audio_path, beam_size=1, word_timestamps=True)

    # Read the audio file
    audio, sample_rate = sf.read(audio_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through segments and create audio files
    for i, segment in enumerate(segments):
        start_time = int(segment['start'] * sample_rate)
        end_time = int(segment['end'] * sample_rate)
        segment_audio = audio[start_time:end_time]
        segment_path = os.path.join(output_folder, f"segment_{i}.wav")
        sf.write(segment_path, segment_audio, sample_rate)
        print(f"Exported segment {i} to {segment_path}")

    # Clear GPU memory
    del whisper_model
    torch.cuda.empty_cache()

def main(input_directory=None):
    from glob import glob

    if input_directory is None:
        input_directory = input("Please enter the input directory: ")

    # Create output directory inside input directory
    output_directory = os.path.join(input_directory, "output_segments")
    os.makedirs(output_directory, exist_ok=True)

    # Find all audio files in the input directory
    audio_files = glob(os.path.join(input_directory, "*.wav"))

    # Process each audio file
    for audio_file in audio_files:
        process_audio(audio_file, output_directory)

if __name__ == "__main__":
    main()
