import subprocess
import wave
import os
import json
import vosk
import re
import time

# Set ALSA device (Update as needed, e.g., "plughw:1,0")
ALSA_DEVICE = "plughw:1,0"

# Path to Vosk model
VOSK_MODEL_PATH = "vosk_model"

# Multi-word wake phrase (lowercase for consistency)
WAKE_PHRASES = ["hey jarvis", "hello assistant"]  # Add variations if needed

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
                print("🔊 Sound detected! Checking for wake phrase...")
                process.kill()  # Stop ALSA listening
                if recognize_wake_phrase():
                    print("🎙 Wake phrase detected! Starting speech-to-text mode...")
                    listen_for_speech()
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)  # Restart listening

def recognize_wake_phrase():
    """ Uses Vosk to transcribe speech and check for a wake phrase """
    model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Record temporary speech audio using ALSA
    temp_wav = "wake_phrase.wav"
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
                
                print(f"📝 Recognized: {transcript}")

                # Check for an exact wake phrase match
                if any(re.search(rf"\b{re.escape(phrase)}\b", transcript) for phrase in WAKE_PHRASES):
                    return True  # Wake phrase detected

    return False  # No wake phrase detected

def listen_for_speech():
    """ Starts continuous speech-to-text transcription until silence is detected """
    model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    temp_wav = "speech_output.wav"
    os.system(f"arecord -D {ALSA_DEVICE} -f S16_LE -r 16000 -c 1 -d 10 {temp_wav}")

    with wave.open(temp_wav, "rb") as wf:
        last_audio_time = time.time()
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcript = result.get("text", "").strip()
                
                if transcript:
                    print(f"📝 Transcribed: {transcript}")
                    last_audio_time = time.time()  # Reset silence timer

            # Stop if silence for 3+ seconds
            if time.time() - last_audio_time > 3:
                print("⏹ No speech detected, returning to wake word mode.")
                break

if __name__ == "__main__":
    detect_sound()
