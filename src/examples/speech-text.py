import vosk
import pyaudio
import json

# Load Vosk Model
model = vosk.Model("vosk_models/vosk-model")

# Setup Microphone Input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

rec = vosk.KaldiRecognizer(model, 16000)

print("Listening for speech...")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("You said:", result.get("text", ""))
except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
