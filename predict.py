import joblib

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# CROP INFO (GLOBAL)
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
# PREDICT FUNCTION
# =========================
def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    data = [[N, P, K, temperature, humidity, ph, rainfall]]
    prediction = model.predict(data)
    return prediction[0]

# =========================
# FULL RECOMMENDATION
# =========================
def get_full_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    crop = predict_crop(N, P, K, temperature, humidity, ph, rainfall)

    info = crop_info.get(crop, {
        "fertilizer": "General",
        "water": "Normal"
    })

    return {
        "crop": crop,
        "fertilizer": info["fertilizer"],
        "water": info["water"]
    }

# =========================
# TEST RUN
# =========================
if __name__ == "__main__":
    result = get_full_recommendation(90, 40, 40, 25, 80, 6.5, 200)
    print(result)