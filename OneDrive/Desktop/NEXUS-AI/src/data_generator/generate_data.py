import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of monitoring records
n = 5000

# Generate normal system monitoring data
data = {
    "timestamp": pd.date_range(
        start="2026-01-01",
        periods=n,
        freq="min"
    ),

    "cpu_usage": np.random.normal(
        loc=50,
        scale=10,
        size=n
    ),

    "memory_usage": np.random.normal(
        loc=60,
        scale=8,
        size=n
    ),

    "api_latency": np.random.normal(
        loc=120,
        scale=20,
        size=n
    ),

    "error_rate": np.random.normal(
        loc=2,
        scale=1,
        size=n
    )
}

# Create DataFrame
df = pd.DataFrame(data)

# Select random rows for anomalies
anomaly_indexes = np.random.choice(
    n,
    100,
    replace=False
)

# Create abnormal system behavior
df.loc[anomaly_indexes, "cpu_usage"] += 40

df.loc[anomaly_indexes, "memory_usage"] += 30

df.loc[anomaly_indexes, "api_latency"] += 500

df.loc[anomaly_indexes, "error_rate"] += 10

# Prevent negative values
df["cpu_usage"] = df["cpu_usage"].clip(0, 100)

df["memory_usage"] = df["memory_usage"].clip(0, 100)

df["api_latency"] = df["api_latency"].clip(lower=0)

df["error_rate"] = df["error_rate"].clip(lower=0)

# Save generated data
df.to_csv(
    "data/raw/system_metrics.csv",
    index=False
)

print("Data generated successfully!")
print(f"Total records: {len(df)}")

print("\nFirst 5 records:")

print(df.head())