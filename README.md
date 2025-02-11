# classNotes
This module uses whisper.cpp + gemini free tier API to summarize the lecture without active attention.
# usage
python3 pipeline.py to start.
# note on GEMINI api
Please apply for an individual API to get started. Put it as a txt as specified in gemini_api.py.
# note on whisper
whisper on Mac M1 is too slow, changing to whisper.cpp for better native metal config.
You need to make and build own whisper.cpp program following appropriate GitHub packages.
Replace whiserp_transcribe.py with correct absolute path (or if you decide to clone the entire thing here)
# features
1. Ideally it should be free unless you have multiple people sharing the same GEMINI key. Do note the choice of whisper model. Turbo is excellent in accuracy but without gpu performance is catastrophically slow. 
2. Feature using threads. In short, the producers are i) the recording ii) the transcripts. The consumers are i) the transcript modules that consume produced recordings ii) the ai module that consume produced transcripts. Depending on your computing power you may adjust up the number of workers of transcription module, for non-GPU computer I shall suffice with worker=1 with appreciable speed and in a semi-real-time transcription.
3. Enter new line to stop recording. Old program assumes a constant minutes of recording.
# drawbacks
Now the recordings are retained as is. Future script may involve auto-cloud-upload.
