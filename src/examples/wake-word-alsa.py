# uses ALSA to detect sound, if sound detected, then
# records 3 seconds of audio.  Once recorded, it uses
# vosk to recognize wake words.  Can support multiple.
#
# Setup:
#   pip install vosk pyaudio numpy subprocess

import subprocess
import wave
import os
import json
import vosk
import re

# Set ALSA device (Update as needed, e.g., "plughw:1,0")
ALSA_DEVICE = "plughw:1,0"

# Path to Vosk model
VOSK_MODEL_PATH = "vosk_model"

# Multi-word wake phrase (lowercase for consistency)
WAKE_PHRASES = ["hey jarvis", "hello assistant", "d r 0 1 d", "dr01d", "kalani"]  # Add variations if needed

def detect_sound():
    """ Uses ALSA (arecord) to detect sound levels and trigger speech recognition """
    command = f"arecord -D {ALSA_DEVICE} -f S16_LE -r 16000 -c 1 -t raw"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    print("🎤 Listening for sound...")

    while True:
        data = process.stdout.read(2)  # Read 16-bit sample
        if data:
            sample_value = int.from_bytes(data, byteorder="little", signed=True)
            
            if abs(sample_value) > 500:  # Adjust sensitivity
                print("🔊 Sound detected! Starting speech recognition...")
                process.kill()  # Stop ALSA listening
                recognize_speech()
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)  # Restart listening

def recognize_speech():
    """ Uses Vosk to transcribe speech and check for a wake phrase """
    model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Record temporary speech audio using ALSA
    temp_wav = "temp_speech.wav"
    os.system(f"arecord -D {ALSA_DEVICE} -f S16_LE -r 16000 -c 1 -d 3 {temp_wav}")

    # Open recorded audio and pass it to Vosk
    with wave.open(temp_wav, "rb") as wf:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcript = result.get("text", "").strip().lower()
                
                print(f"Recognized: {transcript}")

                # Check for an exact wake phrase match
                if any(re.search(rf"\b{re.escape(phrase)}\b", transcript) for phrase in WAKE_PHRASES):
                    print(f"Wake phrase detected: '{transcript}'")
                    trigger_action()
                    break

def trigger_action():
    """ Function to run when wake word is detected """
    print("🚀 Running custom action...")
    os.system("echo 'Wake phrase detected!' > wake_log.txt")

if __name__ == "__main__":
    detect_sound()
