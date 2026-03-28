import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import whisper
import shutil
import re

# =========================
# INIT APP
# =========================
app = FastAPI()

# ✅ CORS (IMPORTANT)
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
print("ML Model loaded")

whisper_model = whisper.load_model("tiny")
print("Whisper loaded")

# =========================
# CROP INFO
# =========================
crop_info = {
    "rice": {"fertilizer": "Urea", "water": "High"},
    "wheat": {"fertilizer": "NPK", "water": "Medium"},
    "maize": {"fertilizer": "DAP", "water": "Medium"},
    "jute": {"fertilizer": "Nitrogen-rich", "water": "High"},
    "cotton": {"fertilizer": "Potash", "water": "Medium"},
    "sugarcane": {"fertilizer": "NPK", "water": "High"},
    "coffee": {"fertilizer": "NPK", "water": "Medium"},
    "banana": {"fertilizer": "Potash", "water": "High"},
    "watermelon": {"fertilizer": "DAP", "water": "Medium"},
    "muskmelon": {"fertilizer": "DAP", "water": "Medium"},
}

# =========================
# SMART PARSER
# =========================
def extract_values(text):
    text = text.lower()

    def find(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else 0

    return {
        "N": find(r"(?:n|nitrogen)\s*(\d+)"),
        "P": find(r"(?:p|phosphorus)\s*(\d+)"),
        "K": find(r"(?:k|potassium)\s*(\d+)"),
        "temperature": find(r"(?:temperature|temp)\s*(\d+)"),
        "humidity": find(r"(?:humidity)\s*(\d+)"),
        "ph": find(r"(?:ph)\s*(\d+\.?\d*)"),
        "rainfall": find(r"(?:rain|rainfall)\s*(\d+)")
    }

# =========================
# ROOT
# =========================
@app.get("/")
def home():
    return {"message": "API is running"}

# =========================
# TEXT PREDICT
# =========================
@app.post("/predict")
def predict(data: dict):
    try:
        values = [[
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])
        ]]

        probs = model.predict_proba(values)[0]
        classes = model.classes_

        top = probs.argsort()[::-1][:3]

        result = []
        for i in top:
            crop = str(classes[i]).lower()
            info = crop_info.get(crop, {"fertilizer": "General", "water": "Normal"})

            result.append({
                "crop": crop,
                "confidence": round(float(probs[i]) * 100, 2),
                "fertilizer": info["fertilizer"],
                "water": info["water"]
            })

        return {"recommendations": result}

    except Exception as e:
        return {"error": str(e)}

# =========================
# AUDIO PREDICT
# =========================
@app.post("/predict-audio")
def predict_audio(file: UploadFile = File(...)):
    try:
        path = "temp.webm"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = whisper_model.transcribe(path)["text"].lower()

        data = extract_values(text)

        values = [[
            data["N"], data["P"], data["K"],
            data["temperature"], data["humidity"],
            data["ph"], data["rainfall"]
        ]]

        probs = model.predict_proba(values)[0]
        classes = model.classes_

        top = probs.argsort()[::-1][:3]

        result = []
        for i in top:
            crop = str(classes[i]).lower()
            info = crop_info.get(crop, {"fertilizer": "General", "water": "Normal"})

            result.append({
                "crop": crop,
                "confidence": round(float(probs[i]) * 100, 2),
                "fertilizer": info["fertilizer"],
                "water": info["water"]
            })

        return {
            "text": text,
            "data": data,
            "recommendations": result
        }

    except Exception as e:
        return {"error": str(e)}