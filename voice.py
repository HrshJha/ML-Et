import whisper
import requests
from gtts import gTTS
import sounddevice as sd
from scipy.io.wavfile import write
import os

# =========================
# RECORD AUDIO
# =========================
def record_audio(filename="input.wav", duration=5, fs=44100):
    print("Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print("Recording done")

# =========================
# SPEECH → TEXT
# =========================
def speech_to_text(file="input.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]

# =========================
# CALL YOUR API
# =========================
def call_api():
    url = "http://127.0.0.1:8000/predict"

    data = {
        "N": 90,
        "P": 40,
        "K": 40,
        "temperature": 25,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200
    }

    response = requests.post(url, json=data)
    return response.json()

# =========================
# TEXT → SPEECH
# =========================
def speak(text, lang="hi"):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("afplay output.mp3")  # Mac

# =========================
# MAIN FLOW
# =========================
if __name__ == "__main__":
    # Step 1: record
    record_audio()

    # Step 2: speech → text
    text = speech_to_text()
    print("You said:", text)

    # Step 3: call API
    result = call_api()
    print("API Result:", result)
    crop_hindi = {
    "rice": "chawal",
    "wheat": "gehu",
    "maize": "makka",
    "jute": "jute",
    "cotton": "kapas",
    "sugarcane": "ganna"
}

    # Step 4: convert to Hindi voice
crop_name = crop_hindi.get(result["crop"], result["crop"])

response_text = (
    f"Aapko {crop_name} ugaana chahiye. "
    f"{result['fertilizer']} fertilizer use karein. "
    f"{result['water']} paani dein."
)
    # Step 5: speak
speak(response_text)