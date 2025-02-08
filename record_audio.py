import subprocess
import time

def record_audio(output_file, duration=15):
    command = [
        "rec",  # sox 的录音命令
        "-q",    # 静默模式
        "-b", "16",  # 16-bit 深度
        "-c", "2",   # 双声道
        "-r", "44100",  # 采样率
        "-t", "wav",    # 输出格式
        output_file,
        "trim", "0", str(duration)  # 录制时长
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Recorded audio saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error recording audio: {e}")
    except FileNotFoundError:
        print("Error: 'sox' not found. Install via 'brew install sox'")

if __name__ == "__main__":
    timestamp = int(time.time())
    record_audio(f"recording_{timestamp}.wav")