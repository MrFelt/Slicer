import os
import shutil
import random
import argparse

def randomize_and_move_files(main_folder):
    """Randomize names and move WAV and FLAC files to the main folder."""

    # Find all wav and flac files
    files_to_move = []
    for root, _, files in os.walk(main_folder):
        for file in files:
            if file.endswith(('.wav', '.flac')):
                files_to_move.append(os.path.join(root, file))
    print(f"Found {len(files_to_move)} files.")

    # Generate random names
    random_names = random.sample(range(1, 100000), len(files_to_move))
    print("Generated random names.")

    # Move and rename files to main folder
    for old_path, new_name in zip(files_to_move, random_names):
        extension = os.path.splitext(old_path)[1]
        new_path = os.path.join(main_folder, f"{new_name}{extension}")
        shutil.move(old_path, new_path)
    print("Files moved and renamed.")

if __name__ == '__main__':
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Randomize and move WAV and FLAC files.')
    parser.add_argument('main_folder', type=str, help='Path to the main folder.')
    args = parser.parse_args()

    randomize_and_move_files(args.main_folder)
