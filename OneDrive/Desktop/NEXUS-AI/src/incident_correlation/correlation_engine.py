import pandas as pd
from pathlib import Path


# Find main project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Input files
metrics_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "anomaly_results.csv"
)

logs_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "log_analysis_results.csv"
)


# Output file
output_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "incident_correlation_results.csv"
)


# Load datasets
metrics_df = pd.read_csv(metrics_path)
logs_df = pd.read_csv(logs_path)


print("Datasets loaded successfully!")

print("Metrics records:", len(metrics_df))
print("Log records:", len(logs_df))


# Get anomaly incidents
incidents = metrics_df[
    metrics_df["anomaly"] == 1
].copy()


print("Detected incidents:", len(incidents))


def find_related_logs(root_cause, logs):

    root_cause = str(root_cause).lower()

    # Database/API related incidents
    if (
        "database" in root_cause
        or "api latency" in root_cause
    ):

        keywords = [
            "database",
            "timeout",
            "api"
        ]

    # CPU related incidents
    elif "cpu" in root_cause:

        keywords = [
            "cpu",
            "resource"
        ]

    # Memory related incidents
    elif "memory" in root_cause:

        keywords = [
            "memory"
        ]

    # Error/application incidents
    elif "error" in root_cause or "application" in root_cause:

        keywords = [
            "failed",
            "error",
            "unavailable"
        ]

    else:

        keywords = [
            "error",
            "warning"
        ]


    # Search matching log messages
    related_logs = logs[
        logs["message"]
        .str.lower()
        .str.contains(
            "|".join(keywords),
            na=False
        )
    ]

    return related_logs


# Store correlation results
results = []


for _, incident in incidents.iterrows():

    related_logs = find_related_logs(
        incident["root_cause"],
        logs_df
    )


    # Get top matching logs
    matching_logs = related_logs.head(3)


    # Create incident record
    results.append({

        "timestamp": incident["timestamp"],

        "severity": incident["severity"],

        "root_cause": incident["root_cause"],

        "incident_risk": incident["incident_risk"],

        "related_log_count": len(related_logs),

        "sample_related_logs": " | ".join(
            matching_logs["message"]
            .astype(str)
            .tolist()
        )

    })


# Create result dataframe
results_df = pd.DataFrame(results)


# Save results
results_df.to_csv(
    output_path,
    index=False
)


print("\nIncident correlation completed successfully!")

print(
    "\nCorrelation results saved to:"
)

print(output_path)


print("\nFirst 10 results:")

print(
    results_df.head(10)
)