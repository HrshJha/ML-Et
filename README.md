# 🌱 Crop Recommendation System (ML Project)

## Overview

This project is a Machine Learning-based crop recommendation system that suggests the most suitable crop based on soil and environmental conditions.

It takes input parameters such as:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* Temperature
* Humidity
* pH value
* Rainfall

And predicts the best crop to grow.

---

## Features

* Machine Learning model trained on agricultural dataset
* Real-time prediction API (backend)
* Simple web interface (frontend)
* Optional voice input support (Whisper-based)
* Modular structure (ML / Backend / Frontend separated)

---

## Project Structure

```
crop-recommendation/
│
├── backend/              # API + logic
├── frontend/             # UI
├── model/                # ML model + training
```

---

## Tech Stack

### Machine Learning

* Python
* Scikit-learn
* Pandas
* NumPy

### Backend

* Flask / FastAPI (depending on your implementation)

### Frontend

* HTML
* CSS

### Optional

* OpenAI Whisper / Speech Recognition

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/your-username/crop-recommendation.git
cd crop-recommendation
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows
```

---

### 3. Install Dependencies

```
pip install -r backend/requirements.txt
```

---

## Running the Project

### Step 1: Start Backend

```
cd backend
python app.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

### Step 2: Open Frontend

Open:

```
frontend/index.html
```

in your browser

---

## Model Training

To retrain the model:

```
cd model
python train.py
```

Dataset used:

* Crop_recommendation.csv
* Custom city dataset

---

## Input Parameters

| Parameter   | Description        |
| ----------- | ------------------ |
| N           | Nitrogen content   |
| P           | Phosphorus content |
| K           | Potassium content  |
| Temperature | In Celsius         |
| Humidity    | Percentage         |
| pH          | Soil pH value      |
| Rainfall    | mm                 |

---

## Output

The model predicts:

```
Recommended Crop Name
```

---

## Example

Input:

```
N = 90
P = 42
K = 43
Temperature = 20.8
Humidity = 82
pH = 6.5
Rainfall = 202
```

Output:

```
Rice
```

---

## Future Improvements

* Better UI (React or Tailwind)
* API deployment (Render / AWS)
* Mobile integration
* Real-time weather API integration
* Model optimization

---

## Author

Harsh Kumar Jha

---

## License

MIT License
