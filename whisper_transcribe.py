import whisper

def transcribe_audio(audio_file):
    model = whisper.load_model("turbo")  # Change model size as needed: tiny, base, small, medium, large
    result = model.transcribe(audio_file)
    return result["text"]

if __name__ == "__main__":
    audio_path = "recording_1738943586.wav"  # Replace with your actual file path
    print(transcribe_audio(audio_path))

