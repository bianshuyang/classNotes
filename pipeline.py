import time
import threading
from queue import Queue
from record_audio import record_audio
print('importing whisper...')
import whisper
print('whisper importing success!')
model = whisper.load_model("turbo") 
print('model loading complete! Service ready')
def transcribe_audio(audio_file): # Change model size as needed: tiny, base, small, medium, large
    result = model.transcribe(audio_file)
    return result["text"]
from gemini_api import generate_mcq
import logging
from queue import Empty

import os

# 队列设置
audio_queue = Queue()  # 存放待转写的音频文件
transcript_queue = Queue()  # 存放待生成MCQ的文本
batch_queue = Queue()  # 存放每5个合并后的文本批次

# 线程池大小
TRANSCRIBE_WORKERS = 1  # 保持为1以保证顺序
GENERATE_WORKERS = 1    # Gemini API的并发线程数

logging.basicConfig(filename='transcript.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')
def mock_record_audio(output_file, duration=15):
    """模拟录音文件生成"""
    import shutil
    dummy_audio = "mock.wav"
    shutil.copy(dummy_audio, output_file)


def record_audio_loop_test(interval=15, max_files=10):
    """模拟录音循环（测试用）"""
    buffer_index = 0
    while buffer_index < max_files:
        audio_file = f"audio_{buffer_index}_{int(time.time())}.wav"
        try:
            mock_record_audio(audio_file, duration=interval)
            audio_queue.put(audio_file)
            buffer_index += 1
            time.sleep(interval)
        except Exception as e:
            print(f"Mock recording failed: {e}")
            time.sleep(1)

def transcribe_worker():
    """转写工作线程"""
    while True:
        audio_file = audio_queue.get()
        if audio_file is None:
            break
        try:
            print(f'Starting transcription for {audio_file}')
            transcript = transcribe_audio(audio_file)
            logging.info(f"Audio File: {audio_file}\nTranscript: {transcript}\n{'-'*50}")
            transcript_queue.put((audio_file, transcript))
        except Exception as e:
            print(f"Error transcribing {audio_file}: {e}")
        finally:
            audio_queue.task_done()


def record_audio_loop_produce(max_duration=30):
    """Record until either `max_duration` passes or user indicates stop."""
    start_time = time.time()
    buffer_index = 0

    while True:
        elapsed = time.time() - start_time
        if elapsed >= max_duration:
            print("Reached max recording duration. Stopping recording.")
            break
        
        # Alternatively, you can also check a global or threading.Event to allow user to press Enter to stop
        # e.g. if user_stop_event.is_set(): break

        audio_file = f"audio_{buffer_index}_{int(time.time())}.wav"
        try:
            record_audio(audio_file, duration=3)  # or however long each chunk is
            audio_queue.put(audio_file)
            buffer_index += 1
        except Exception as e:
            print(f"Recording failed: {e}")
            time.sleep(1)
    
    print("Recording thread exiting. No more audio will be produced.")
    # Here we do NOT put None into audio_queue yet if we want the pipeline to keep processing
    # We'll put None only when we do a final shutdown.
'''
def record_audio_loop_produce():
    print('recording starts!')
    interval = 3
    """录音循环线程，持续生成音频文件"""
    buffer_index = 0
    while True:
        audio_file = f"audio_{buffer_index}_{int(time.time())}.wav"  # 唯一文件名
        try:
            # 阻塞式录音（假设record_audio支持duration参数）
            record_audio(audio_file, duration=interval)
            #mock_record_audio(audio_file, duration=interval)
            audio_queue.put(audio_file)
            buffer_index += 1
        except Exception as e:
            print(f"Recording failed: {e}")
            time.sleep(1)  # 防止错误循环
'''
def batch_worker():
    """Strictly wait until 5 transcripts or a stop signal arrives."""
    buffer = []
    while True:
        item = transcript_queue.get()  # No timeout => blocks until item is available
        if item is None:
            # Stop signal
            if buffer:
                # Flush any leftover items (optional)
                combined = ' '.join([t for _, t in buffer])
                files = [af for af, _ in buffer]
                batch_queue.put((combined, files))
            # Tell generate_workers to stop as well
            for _ in range(GENERATE_WORKERS):
                batch_queue.put(None)
            transcript_queue.task_done()
            break

        buffer.append(item)
        transcript_queue.task_done()

        # If we have 5 items, flush them as one batch.
        if len(buffer) == 5:
            combined = ' '.join([t for _, t in buffer])
            files = [af for af, _ in buffer]
            batch_queue.put((combined, files))
            buffer = []


def generate_worker():
    """生成工作线程（修改后处理批次）"""
    while True:
        batch = batch_queue.get()
        if batch is None:
            break
        combined_transcript, audio_files = batch
        try:
            print("*"*30)
            print(combined_transcript)
            summary = generate_mcq(combined_transcript)
            print(f"\n--- Batch Summary ({len(audio_files)} files) ---\n{summary}")
        except Exception as e:
            print(f"Error generating MCQ: {e}")
        finally:
            for af in audio_files:
                if os.path.exists(af):
                    os.remove(af)
            batch_queue.task_done()

def start_pipeline():
    # 初始化线程池
    transcribe_threads = []
    for _ in range(TRANSCRIBE_WORKERS):
        t = threading.Thread(target=transcribe_worker, daemon=True)
        t.start()
        transcribe_threads.append(t)

    # 启动批次处理线程
    batch_thread = threading.Thread(target=batch_worker, daemon=True)
    batch_thread.start()

    # 启动生成线程池
    generate_threads = []
    for _ in range(GENERATE_WORKERS):
        t = threading.Thread(target=generate_worker, daemon=True)
        t.start()
        generate_threads.append(t)

    # 启动模拟录音线程
    record_thread = threading.Thread(
        target=record_audio_loop_produce, 
        args=(30,),  # e.g. 1.5 hours = 5400 seconds
        daemon=False  
    )
    record_thread.start()
    return record_thread, transcribe_threads, batch_thread, generate_threads
    
def main():
    record_thread, transcribe_threads, batch_thread, generate_threads = start_pipeline()

    # Wait for the recording thread to finish (it will finish after max_duration or user stops)
    record_thread.join()
    print("Recording has stopped. Now let's wait for the queue to empty or do a final shutdown...")

    # If you want to keep the pipeline running until all current items are processed:
    # 1) Wait until the audio_queue is empty:
    audio_queue.join()
    
    # 2) Now tell transcribers no more new audio
    for _ in range(TRANSCRIBE_WORKERS):
        audio_queue.put(None)
    for t in transcribe_threads:
        t.join()
    
    # 3) Wait until transcripts are fully processed
    transcript_queue.join()
    # Then push None so batch_worker can flush or finish
    transcript_queue.put(None)
    batch_thread.join()
    
    # 4) Wait until all batches are generated
    batch_queue.join()
    for _ in range(GENERATE_WORKERS):
        batch_queue.put(None)
    for t in generate_threads:
        t.join()

    print("All done. Exiting gracefully.")


if __name__ == "__main__":
    main()