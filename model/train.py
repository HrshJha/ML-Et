import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("Crop_recommendation.csv")

# =========================
# FEATURES & LABEL
# =========================
X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = df["label"]

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)

# =========================
# TRAIN
# =========================
model.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "model.pkl")
print("Model saved successfully")