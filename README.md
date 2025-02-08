# classNotes
I absolutely hate school lectures. This module uses whisper + gemini to summarize the lecture without active attention.
# usage
python3 pipeline.py to start.
# note on GEMINI api
Please apply for an individual API to get started. 
# features
1. Ideally it should be free unless you have multiple people sharing the same GEMINI key. Do note the choice of whisper model. Turbo is excellent in accuracy but without gpu performance is catastrophically slow. 
2. Feature using threads. In short, the producers are i) the recording ii) the transcripts. The consumers are i) the transcript modules that consume produced recordings ii) the ai module that consume produced transcripts. Depending on your computing power you may adjust up the number of workers of transcription module, for non-GPU computer I shall suffice with worker=1.
