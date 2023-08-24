import sys
import whisper


def process_audio(audio_path):
    model = whisper.load_model("models/whisper_medium.safetensors")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    recognized_text = result.text

    return detected_language, recognized_text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python whisper.py <audio_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    language, recognized_text = process_audio(audio_path)

    print(f"Detected language: {language}")
    print(f"Recognized text: {recognized_text}")