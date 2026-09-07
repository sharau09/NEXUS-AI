import pandas as pd
from pathlib import Path


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

input_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "anomaly_results.csv"
)


# Load processed data
df = pd.read_csv(input_path)


def find_root_cause(row):

    # Normal system
    if row["anomaly"] == 0:
        return "No Incident"

    # Database / API performance issue
    if row["api_latency"] >= 600:
        return "High API Latency / Database Performance Issue"

    # CPU overload
    elif row["cpu_usage"] >= 85:
        return "High CPU Usage / Compute Resource Overload"

    # Memory problem
    elif row["memory_usage"] >= 85:
        return "High Memory Usage / Possible Memory Leak"

    # Error issue
    elif row["error_rate"] >= 8:
        return "High Error Rate / Application Failure"

    # Unknown anomaly
    else:
        return "Unknown System Anomaly"


# Apply root cause analysis
df["root_cause"] = df.apply(
    find_root_cause,
    axis=1
)


# Save updated data
df.to_csv(
    input_path,
    index=False
)


print("Root Cause Analysis Completed!")

print("\nRoot Cause Summary:")

print(
    df["root_cause"].value_counts()
)