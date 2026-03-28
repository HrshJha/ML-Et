from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# INPUT SCHEMA (VALIDATION)
# =========================
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

# =========================
# CROP INFO DATABASE
# =========================
crop_info = {
    "rice": {"fertilizer": "Urea", "water": "High"},
    "wheat": {"fertilizer": "NPK", "water": "Medium"},
    "maize": {"fertilizer": "DAP", "water": "Medium"},
    "jute": {"fertilizer": "Nitrogen-rich", "water": "High"},
    "cotton": {"fertilizer": "Potash", "water": "Medium"},
    "sugarcane": {"fertilizer": "NPK", "water": "High"}
}

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/")
def home():
    return {"message": "AgriMind API Running"}

# =========================
# PREDICTION LOGIC
# =========================
def get_recommendations(data):
    features = [[
        data.N,
        data.P,
        data.K,
        data.temperature,
        data.humidity,
        data.ph,
        data.rainfall
    ]]

    results = []

    try:
        probs = model.predict_proba(features)[0]
        classes = model.classes_

        top_indices = probs.argsort()[-3:][::-1]

        for i in top_indices:
            crop = classes[i]
            info = crop_info.get(crop, {"fertilizer": "General", "water": "Normal"})

            results.append({
                "crop": crop,
                "confidence": round(float(probs[i]) * 100, 2),
                "fertilizer": info["fertilizer"],
                "water": info["water"]
            })

    except Exception as e:
        # fallback instead of crashing
        prediction = model.predict(features)[0]
        info = crop_info.get(prediction, {"fertilizer": "General", "water": "Normal"})

        results.append({
            "crop": prediction,
            "confidence": "N/A",
            "fertilizer": info["fertilizer"],
            "water": info["water"]
        })

    return results

# =========================
# MAIN API ENDPOINT
# =========================
@app.post("/predict")
def predict_crop(input_data: CropInput):

    # Basic validation
    if not (0 <= input_data.ph <= 14):
        raise HTTPException(status_code=400, detail="Invalid pH value")

    if input_data.N < 0 or input_data.P < 0 or input_data.K < 0:
        raise HTTPException(status_code=400, detail="NPK values must be non-negative")

    recommendations = get_recommendations(input_data)

    explanation = (
        f"Based on temperature ({input_data.temperature}°C), "
        f"humidity ({input_data.humidity}%), soil nutrients (NPK), "
        f"and rainfall ({input_data.rainfall} mm)."
    )

    return {
        "recommendations": recommendations,
        "explanation": explanation
    }