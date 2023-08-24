import os
import subprocess
import sys
import concurrent.futures


def resample_audio(input_audio):
    try:
        # Using FFmpeg to resample and convert to FLAC format
        command = [
            "ffmpeg", "-i", input_audio, "-ar", "48000", "-ac", "1", "-c:a", "flac",
            "-sample_fmt", "s32", "-b:a", "256k", "-f", "null", "-"
        ]
        subprocess.run(command, check=True)
        print(f"Resampled: {input_audio}")
    except subprocess.CalledProcessError as e:
        print(f"Error resampling {input_audio}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python resample.py <audio_file1> [<audio_file2> ...]")
        return

    input_audio_files = sys.argv[1:]

    cpu_count = os.cpu_count()
    max_workers = int((cpu_count / 2) * 0.4)  # Calculate max_workers based on CPU thread count

    max_workers = max(max_workers, 1)  # Ensure at least 1 worker

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for input_audio in input_audio_files:
            executor.submit(resample_audio, input_audio)


if __name__ == "__main__":
    main()