import whisper
import requests
from gtts import gTTS
import sounddevice as sd
from scipy.io.wavfile import write
import os
import tempfile

# =========================
# CROP HINDI TRANSLATIONS (Devanagari)
# =========================
crop_hindi = {
    "rice":       "धान (चावल)",
    "wheat":      "गेहूँ",
    "maize":      "मक्का",
    "jute":       "जूट",
    "cotton":     "कपास",
    "sugarcane":  "गन्ना",
    "coffee":     "कॉफ़ी",
    "banana":     "केला",
    "mango":      "आम",
    "grapes":     "अंगूर",
    "apple":      "सेब",
    "orange":     "संतरा",
    "papaya":     "पपीता",
    "pomegranate":"अनार",
    "watermelon": "तरबूज",
    "muskmelon":  "खरबूजा",
    "coconut":    "नारियल",
    "chickpea":   "चना",
    "kidneybeans":"राजमा",
    "pigeonpeas": "अरहर दाल",
    "mothbeans":  "मोठ",
    "mungbean":   "मूंग",
    "blackgram":  "उड़द",
    "lentil":     "मसूर",
}

fertilizer_hindi = {
    "Urea":         "यूरिया",
    "NPK":          "एनपीके",
    "DAP":          "डीएपी",
    "Nitrogen-rich":"नाइट्रोजन युक्त खाद",
    "Potash":       "पोटाश",
    "General":      "सामान्य खाद",
}

water_hindi = {
    "High":   "अधिक पानी",
    "Medium": "मध्यम पानी",
    "Low":    "कम पानी",
    "Normal": "सामान्य पानी",
}

# =========================
# RECORD AUDIO
# =========================
def record_audio(filename="input.wav", duration=6, fs=16000):
    print("\n🎙️  बोलिए... (Speak now...)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    write(filename, fs, recording)
    print("✅ रिकॉर्डिंग पूरी हुई।")

# =========================
# SPEECH → TEXT (Whisper auto-detects language)
# =========================
def speech_to_text(file="input.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"].strip()

# =========================
# CALL PREDICTION API
# =========================
def call_api(N, P, K, temperature, humidity, ph, rainfall):
    url = "http://127.0.0.1:8000/predict"
    data = {
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

# =========================
# TEXT → HINDI SPEECH (gTTS)
# =========================
def speak_hindi(text: str):
    print(f"\n🗣️  {text}")
    tts = gTTS(text=text, lang="hi", slow=False)
    tmp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(tmp_file.name)
    os.system(f"afplay '{tmp_file.name}'")   # macOS
    # For Linux: os.system(f"mpg123 '{tmp_file.name}'")
    os.unlink(tmp_file.name)

# =========================
# BUILD HINDI RESPONSE
# =========================
def build_hindi_response(result: dict) -> str:
    crop_raw  = str(result.get("crop", "")).strip().lower()
    fert_raw  = result.get("fertilizer", "General")
    water_raw = result.get("water", "Normal")

    crop_hi  = crop_hindi.get(crop_raw, crop_raw)   # falls back to raw name if missing
    fert_hi  = fertilizer_hindi.get(fert_raw, fert_raw)
    water_hi = water_hindi.get(water_raw, water_raw)

    response = (
        f"नमस्ते किसान भाई! "
        f"आपकी जमीन के लिए {crop_hi} की खेती सबसे अच्छी रहेगी। "
        f"कृपया {fert_hi} का उपयोग करें। "
        f"फसल को {water_hi} की आवश्यकता है। "
        f"आपकी फसल अच्छी हो, शुभकामनाएं!"
    )
    return response

# =========================
# PARSE VOICE COMMAND FOR PARAMS
# (Simple demo: uses fixed default values — extend with NLU as needed)
# =========================
def get_farm_params_from_voice():
    """
    In a full production system, you'd use NLU to extract N/P/K etc.
    from the farmer's speech. For now this uses sensible defaults and
    prints what was heard.
    """
    # Default representative soil values
    return {
        "N": 90,
        "P": 40,
        "K": 40,
        "temperature": 25.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 200.0,
    }

# =========================
# MAIN VOICE LOOP
# =========================
def main():
    speak_hindi(
        "नमस्ते! मैं आपका कृषि सहायक हूँ। "
        "मैं आपको बताऊंगा कि आपकी जमीन पर कौन सी फसल उगाएं। "
        "कृपया बोलने के लिए तैयार रहें।"
    )

    while True:
        print("\n" + "="*50)
        print("क्या आप फसल की सिफारिश लेना चाहते हैं?")
        print("माइक्रोफोन में बोलें: 'हाँ' या 'बंद करो' (quit)")
        print("="*50)

        record_audio(duration=4)
        heard = speech_to_text().lower()
        print(f"📝 आपने कहा: {heard}")

        # Exit words
        if any(w in heard for w in ["बंद", "बाहर", "quit", "exit", "stop", "band"]):
            speak_hindi("ठीक है! धन्यवाद। खुदा हाफिज़।")
            break

        # Proceed to recommendation
        speak_hindi("ठीक है। अभी आपकी जमीन के लिए सुझाव तैयार हो रहा है।")

        params = get_farm_params_from_voice()
        result = call_api(**params)

        if result:
            message = build_hindi_response(result)
            speak_hindi(message)
        else:
            speak_hindi(
                "क्षमा करें, इस समय सेवा उपलब्ध नहीं है। "
                "कृपया बाद में प्रयास करें।"
            )

        speak_hindi("क्या आप फिर से जानकारी लेना चाहते हैं?")

if __name__ == "__main__":
    main()