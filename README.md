# 🌾 AgriMind — Voice-Based Crop Recommendation System

> Built with intent, frustration, iteration, and persistence.
> Not a tutorial copy. Not a template project.
> A system that actually works end-to-end.

---

## 🚀 What is AgriMind?

AgriMind is a **voice-driven AI + ML system** that takes spoken agricultural inputs (NPK, temperature, humidity, pH, rainfall) and returns:

* 🌱 Crop recommendations
* 📊 Confidence scores
* 🔊 Voice output (system speaks result)

---

## 🧠 What it actually does

**Pipeline:**

```
🎤 Voice Input → Whisper (Speech-to-Text)
              → Regex Parser (extract values)
              → ML Model (RandomForest)
              → JSON Output + Voice Output
```

---

## 🔥 Why this exists

Most crop recommendation systems:

* require manual input ❌
* are not accessible to farmers ❌
* are not interactive ❌

AgriMind solves:

* Voice-based input ✔
* Fast ML prediction ✔
* Real-time feedback ✔

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* scikit-learn
* joblib
* Whisper (`openai-whisper`)
* pyttsx3 (Text-to-Speech)

### Frontend

* HTML
* CSS
* JavaScript (MediaRecorder API)

---

## 📦 Installation

### 1. Clone repo

```bash
git clone <your-repo-link>
cd AgriMind
```

---

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib openai-whisper pyttsx3 python-multipart
```

---

### 4. (Mac fix for Whisper SSL issue)

```bash
/Applications/Python\ 3.14/Install\ Certificates.command
```

---

## ▶️ Running the Project

### Terminal 1 (Backend)

```bash
uvicorn app:app --reload
```

---

### Terminal 2 (Frontend)

```bash
python -m http.server 5500
```

---

### Open in browser:

```
http://localhost:5500
```

---

## 🎯 How to Use

1. Click **Start**
2. Speak (≤ 4 seconds):

   ```
   nitrogen 90 phosphorus 40 potassium 40 temperature 25 humidity 80 ph 6.5 rainfall 200
   ```
3. Click **Stop**
4. Get:

   * JSON output
   * 🔊 Voice output (system speaks result)

---

## ⚠️ Real Problems We Faced

This was not smooth. Here’s what actually went wrong:

---

### ❌ 1. Environment Chaos

* `(venv) (base)` conflict
* packages installing in wrong Python
* modules not found

✔ Fix:

* isolate environment
* use only `(venv)`

---

### ❌ 2. Whisper SSL Failure

```
CERTIFICATE_VERIFY_FAILED
```

✔ Fix:

* install certificates
* fallback SSL override

---

### ❌ 3. Audio Format Issues

* `.wav` vs `.webm`
* Whisper not decoding properly

✔ Fix:

* switched to `webm + opus`

---

### ❌ 4. Browser TTS Completely Failed

* Chrome blocking speech
* Brave blocking everything
* async issues

✔ Final decision:
👉 **Removed browser TTS**
👉 Used backend voice (pyttsx3)

---

### ❌ 5. Slow Processing

Cause:

* Whisper on CPU

✔ Fix:

* use `tiny.en`
* limit recording to 4 seconds

---

### ❌ 6. Speech Parsing Errors

Input like:

```
n90p40k40
```

✔ Fix:

* robust regex parser
* supports messy speech

---

## 🧠 What We Learned

* ML is the easiest part
* Real problem = integration
* Audio + browser = unpredictable
* Debugging > coding

---

## 📊 Model Details

* Algorithm: RandomForestClassifier
* Accuracy: ~99% (on dataset)
* Input features:

  * N, P, K
  * Temperature
  * Humidity
  * pH
  * Rainfall

---

## 🎨 UI

* Minimal but clean
* CSS-based modern layout
* Designed for demonstration + portfolio

---

## 🔊 Voice Output

* Implemented via `pyttsx3`
* Runs on backend
* Works independent of browser

---

## 🚧 Future Improvements

* Natural language understanding (no structured input)
* Auto weather API (city-based input)
* Mobile-friendly UI
* Deployment (public access)
* Better UI (cards, charts, visualization)

---

## 💭 What this project really took

Not just code.

* patience when nothing worked
* debugging environment issues
* understanding browser limitations
* fixing things that tutorials never mention

---

## 🧑‍💻 Author

**Harsh Kumar Jha**

Built with:

* intent
* frustration
* iteration
* and consistency

---

## ⚡ Final Note

This is not a perfect system.
It is a **working system**.

And that matters more.

---

## ⭐ If you read this far

You’re not just browsing projects.
You’re trying to understand them.

That already puts you ahead.
