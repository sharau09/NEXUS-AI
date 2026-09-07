import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

input_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "anomaly_results.csv"
)


df = pd.read_csv(input_path)


def calculate_severity(row):

    # Normal records
    if row["anomaly"] == 0:
        return "NORMAL"

    # Critical incidents
    if (
        row["cpu_usage"] >= 90
        or row["memory_usage"] >= 90
        or row["api_latency"] >= 600
        or row["error_rate"] >= 10
    ):
        return "CRITICAL"

    # High severity incidents
    elif (
        row["cpu_usage"] >= 80
        or row["memory_usage"] >= 80
        or row["api_latency"] >= 400
        or row["error_rate"] >= 7
    ):
        return "HIGH"

    # Low severity incidents
    else:
        return "LOW"


# Apply severity classification
df["severity"] = df.apply(
    calculate_severity,
    axis=1
)


# Save updated results
df.to_csv(
    input_path,
    index=False
)


print("Incident severity classification completed!")

print("\nSeverity Summary:")

print(
    df["severity"].value_counts()
)