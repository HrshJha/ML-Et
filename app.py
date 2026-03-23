from fastapi import FastAPI
import joblib

# =========================
# INIT APP
# =========================
app = FastAPI()

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# CROP INFO
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
# ROOT CHECK
# =========================
@app.get("/")
def home():
    return {"message": "API is running"}

# =========================
# PREDICTION API
# =========================
@app.post("/predict")
def predict(data: dict):
    values = [[
        data["N"],
        data["P"],
        data["K"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"]
    ]]

    crop = model.predict(values)[0]

    info = crop_info.get(crop, {
        "fertilizer": "General",
        "water": "Normal"
    })

    return {
        "crop": crop,
        "fertilizer": info["fertilizer"],
        "water": info["water"]
    }