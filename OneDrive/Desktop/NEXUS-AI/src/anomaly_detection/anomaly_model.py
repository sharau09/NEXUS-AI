import pandas as pd
from sklearn.ensemble import IsolationForest

# Load system monitoring data
df = pd.read_csv(
    "data/raw/system_metrics.csv"
)

print("Dataset loaded successfully!")
print("Total records:", len(df))


# Select the important monitoring features
features = [
    "cpu_usage",
    "memory_usage",
    "api_latency",
    "error_rate"
]

X = df[features]


# Create the AI anomaly detection model
model = IsolationForest(
    contamination=0.02,
    random_state=42
)


# Train the model and detect anomalies
predictions = model.fit_predict(X)


# Isolation Forest gives:
# 1 = Normal
# -1 = Anomaly

df["anomaly"] = predictions


# Convert values:
# 0 = Normal
# 1 = Anomaly

df["anomaly"] = df["anomaly"].map({
    1: 0,
    -1: 1
})


# Count anomalies
anomaly_count = df["anomaly"].sum()

print("\nAnomalies detected:", anomaly_count)


# Save results
df.to_csv(
    "data/processed/anomaly_results.csv",
    index=False
)


print("\nAnomaly detection completed!")
print(
    "Results saved to data/processed/anomaly_results.csv"
)


# Show detected anomalies
print("\nSample detected anomalies:")

print(
    df[df["anomaly"] == 1]
    .head()
)