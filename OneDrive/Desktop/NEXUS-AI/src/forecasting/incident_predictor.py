import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import joblib


# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Data path
data_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "anomaly_results.csv"
)


# Model path
model_path = (
    BASE_DIR /
    "models" /
    "incident_prediction_model.pkl"
)


# Load data
df = pd.read_csv(data_path)

print("Dataset loaded successfully!")
print("Total records:", len(df))


# Features used for prediction
features = [
    "cpu_usage",
    "memory_usage",
    "api_latency",
    "error_rate"
]


X = df[features]

# Target
y = df["anomaly"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create ML model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# Train model
model.fit(
    X_train,
    y_train
)


# Predictions
predictions = model.predict(X_test)


# Print results
print("\nModel Performance:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)


# Save model
joblib.dump(
    model,
    model_path
)


print(
    "\nIncident prediction model saved successfully!"
)


# Predict probability for all records
probabilities = model.predict_proba(X)[:, 1]


df["incident_risk_score"] = (
    probabilities * 100
).round(2)


# Convert score into risk level
def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    else:
        return "LOW"


df["incident_risk"] = df[
    "incident_risk_score"
].apply(get_risk_level)


# Save updated dataset
df.to_csv(
    data_path,
    index=False
)


print("\nRisk prediction completed!")

print("\nRisk Summary:")

print(
    df["incident_risk"]
    .value_counts()
)