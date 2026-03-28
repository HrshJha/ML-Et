import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import whisper
import shutil
import re
import pyttsx3

# =========================
# INIT
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODELS
# =========================
model = joblib.load("model.pkl")
whisper_model = whisper.load_model("tiny.en")

# =========================
# TEXT TO SPEECH
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# =========================
# PARSER
# =========================
def extract_values(text):
    text = text.lower()

    def find(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else 0

    return {
        "N": find(r"(?:n|nitrogen)[^\d]*(\d+)"),
        "P": find(r"(?:p|phosphorus)[^\d]*(\d+)"),
        "K": find(r"(?:k|potassium)[^\d]*(\d+)"),
        "temperature": find(r"(?:temperature|temp)[^\d]*(\d+)"),
        "humidity": find(r"(?:humidity)[^\d]*(\d+)"),
        "ph": find(r"(?:ph)[^\d]*(\d+\.?\d*)"),
        "rainfall": find(r"(?:rainfall|rain)[^\d]*(\d+)")
    }

# =========================
# API
# =========================
@app.post("/predict-audio")
def predict_audio(file: UploadFile = File(...)):
    try:
        path = "temp.webm"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = whisper_model.transcribe(path, fp16=False)
        text = result["text"]

        data = extract_values(text)

        values = [[
            data["N"], data["P"], data["K"],
            data["temperature"], data["humidity"],
            data["ph"], data["rainfall"]
        ]]

        probs = model.predict_proba(values)[0]
        classes = model.classes_

        top = probs.argsort()[::-1][:3]

        recommendations = []

        for i in top:
            crop = str(classes[i]).lower()
            recommendations.append({
                "crop": crop,
                "confidence": round(float(probs[i]) * 100, 2)
            })

        # 🔊 BACKEND VOICE (FINAL FIX)
        top_crop = recommendations[0]["crop"]
        confidence = recommendations[0]["confidence"]

        message = f"{top_crop} is best with {confidence} percent confidence"
        speak(message)

        return {
            "text": text,
            "data": data,
            "recommendations": recommendations
        }

    except Exception as e:
        return {"error": str(e)}