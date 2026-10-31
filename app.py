from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import requests

app = Flask(__name__)

# Real, public UCI New-Thyroid dataset mirror.
# 215 records, 5 clinical test measurements, 3 documented classes.
DATA_URL = "https://raw.githubusercontent.com/mikeizbicki/datasets/master/csv/uci/new-thyroid.data"
COLUMNS = ["class", "t3_resin", "total_thyroxin", "total_triiodothyronine",
           "basal_tsh", "max_tsh_difference"]
FEATURES = COLUMNS[1:]
CLASS_NAMES = {1: "Normal thyroid pattern", 2: "Hyperthyroid pattern", 3: "Hypothyroid pattern"}

def load_real_dataset():
    response = requests.get(DATA_URL, timeout=25)
    response.raise_for_status()
    data = pd.read_csv(StringIO(response.text), header=None, names=COLUMNS)
    data = data.apply(pd.to_numeric, errors="coerce").dropna()
    data = data[data["class"].isin(CLASS_NAMES)]
    if len(data) < 100:
        raise RuntimeError("The downloaded dataset did not pass the integrity check.")
    return data

try:
    df = load_real_dataset()
    X = df[FEATURES]
    y = df["class"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=300, class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = round(accuracy_score(y_test, y_pred) * 100, 1)
    cm = confusion_matrix(y_test, y_pred, labels=[1, 2, 3]).tolist()
    report = classification_report(
        y_test, y_pred, labels=[1, 2, 3],
        target_names=[CLASS_NAMES[i] for i in [1, 2, 3]],
        output_dict=True, zero_division=0
    )
    dataset_error = None
except Exception as exc:
    df = None
    model = None
    accuracy = None
    cm = []
    report = {}
    dataset_error = str(exc)

@app.route("/")
def home():
    if dataset_error:
        return render_template("index.html", accuracy=None, dataset_error=True,
                               total=0, counts={})
    counts = {CLASS_NAMES[int(k)]: int(v) for k, v in df["class"].value_counts().sort_index().items()}
    return render_template("index.html", accuracy=accuracy, dataset_error=False,
                           total=len(df), counts=counts)

@app.route("/predict", methods=["POST"])
def predict():
    if dataset_error or model is None:
        return jsonify({"error": "Real UCI dataset could not be loaded. Check your internet connection and restart the app."}), 503
    try:
        payload = request.get_json(force=True)
        values = [float(payload[key]) for key in FEATURES]
        if not all(np.isfinite(values)):
            raise ValueError()
        row = pd.DataFrame([values], columns=FEATURES)
        prediction = int(model.predict(row)[0])
        probabilities = model.predict_proba(row)[0]
        scores = {
            CLASS_NAMES[int(label)]: round(float(prob) * 100, 1)
            for label, prob in zip(model.classes_, probabilities)
        }
        return jsonify({
            "prediction": CLASS_NAMES[prediction],
            "confidence": round(float(max(probabilities)) * 100, 1),
            "scores": scores,
            "note": "Model output from a small historical public dataset. Not a diagnosis."
        })
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Please enter valid numeric values in all five fields."}), 400

@app.route("/api/stats")
def stats():
    if dataset_error or model is None:
        return jsonify({"error": "Dataset unavailable"}), 503
    return jsonify({
        "total_records": int(len(df)),
        "train_records": int(len(X_train)),
        "test_records": int(len(X_test)),
        "accuracy": accuracy,
        "confusion_matrix": cm,
        "class_counts": {CLASS_NAMES[int(k)]: int(v) for k, v in df["class"].value_counts().sort_index().items()},
        "classification_report": report
    })

if __name__ == "__main__":
    app.run(debug=True)
