import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "data/processed/anomaly_results.csv"
)

anomalies = df[df["anomaly"] == 1]


metrics = [
    "cpu_usage",
    "memory_usage",
    "api_latency",
    "error_rate"
]


for metric in metrics:

    plt.figure(figsize=(14, 6))

    plt.plot(
        df.index,
        df[metric],
        label=metric
    )

    plt.scatter(
        anomalies.index,
        anomalies[metric],
        label="Anomaly"
    )

    plt.title(
        f"NEXUS AI - {metric} Monitoring"
    )

    plt.xlabel("Monitoring Record")

    plt.ylabel(metric)

    plt.legend()

    plt.tight_layout()

    plt.show()