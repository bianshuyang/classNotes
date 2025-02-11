import subprocess
import time

def record_audio(output_file, duration=15):
    raw_output_file = output_file.replace(".wav", "_raw.wav")
    
    record_command = [
        "rec", "-q", "-b", "16", "-c", "1", "-r", "44100", "-t", "wav", raw_output_file, "trim", "0", str(duration)
    ]
    
    ffmpeg_command = [
        "ffmpeg", "-i", raw_output_file, "-ar", "16000", "-ac", "1", output_file, "-y"
    ]
    
    try:
        subprocess.run(record_command, check=True)
        print(f"Raw recorded audio saved to {raw_output_file}")
        
        subprocess.run(ffmpeg_command, check=True)
        print(f"Converted audio saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
    except FileNotFoundError:
        print("Error: 'sox' or 'ffmpeg' not found. Install via 'brew install sox ffmpeg'")

if __name__ == "__main__":
    timestamp = int(time.time())
    record_audio(f"recording_{timestamp}.wav")