import subprocess

def transcribe_audio(audio_file):
    resampled_audio_file = audio_file.replace(".wav", "_16k.wav")
    
    ffmpeg_command = [
        "ffmpeg", "-i", audio_file, "-ar", "16000", "-ac", "1", resampled_audio_file, "-y"
    ]
    
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"Audio resampled to 16kHz: {resampled_audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error resampling audio: {e}")
    
    command = [
    "whisper.cpp/build/bin/whisper-cli",
    resampled_audio_file,
    "--model", "whisper.cpp/models/ggml-large-v3-turbo.bin"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    #print(result)
    return result.stdout

if __name__ == "__main__":
    audio_path = "/train/audio.wav"
    #print('ok')
    print(transcribe_audio(audio_path))
