# Uses Vosk
# Setup:
#   sudo apt update && sudo apt upgrade -y
#   sudo apt install python3-pip portaudio19-dev ffmpeg -y
#   pip3 install vosk pyaudio
#
# Install models:
#   mkdir -p ~/vosk_models && cd ~/vosk_models
#   slecect either of:
#      40MB: wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
#      8MB: wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
#   unzip vosk-model-small-en-us-0.15.zip
#   mv vosk-model-small-en-us-0.15 vosk-model

import vosk
import json
import pyaudio

# Load the Vosk model (download a small model for Raspberry Pi)
model = vosk.Model("vosk_models/vosk-model-small-en-us-0.15")

# Create a Vosk recognizer (16kHz sample rate)
rec = vosk.KaldiRecognizer(model, 16000)

# Initialize microphone stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

wake_word = "jarvis"  # Change this to your desired wake word
print("Listening for wake word...")

while True:
    data = stream.read(4000, exception_on_overflow=False)

    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        recognized_text = result["text"].lower()
        
        if wake_word in recognized_text:
            print(f"Wake word '{wake_word}' detected! Activating assistant...")
            # Call your assistant function here
            break  # Stop listening after wake word is detected
