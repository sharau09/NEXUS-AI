import random
import time
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = (
    BASE_DIR /
    "data" /
    "realtime"
)

METRICS_FILE = (
    DATA_DIR /
    "live_metrics.csv"
)


def generate_metrics():

    cpu_usage = round(
        random.uniform(20, 95),
        2
    )

    memory_usage = round(
        random.uniform(30, 95),
        2
    )

    api_latency = round(
        random.uniform(80, 1200),
        2
    )

    error_rate = round(
        random.uniform(0, 25),
        2
    )

    database_latency = round(
        random.uniform(10, 800),
        2
    )

    return {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "api_latency": api_latency,
        "error_rate": error_rate,
        "database_latency": database_latency
    }


def classify_severity(metrics):

    if (
        metrics["cpu_usage"] > 90
        or metrics["memory_usage"] > 90
        or metrics["api_latency"] > 1000
        or metrics["error_rate"] > 20
    ):

        return "CRITICAL"

    elif (
        metrics["cpu_usage"] > 75
        or metrics["memory_usage"] > 75
        or metrics["api_latency"] > 700
        or metrics["error_rate"] > 10
    ):

        return "HIGH"

    elif (
        metrics["cpu_usage"] > 60
        or metrics["memory_usage"] > 60
        or metrics["api_latency"] > 400
        or metrics["error_rate"] > 5
    ):

        return "MEDIUM"

    return "LOW"


def start_monitoring():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 60)
    print("🚀 NEXUS AI REAL-TIME MONITORING STARTED")
    print("=" * 60)

    while True:

        metrics = generate_metrics()

        metrics["severity"] = (
            classify_severity(metrics)
        )

        new_row = pd.DataFrame(
            [metrics]
        )

        # Create file if it doesn't exist
        if not METRICS_FILE.exists():

            new_row.to_csv(
                METRICS_FILE,
                index=False
            )

        else:

            new_row.to_csv(
                METRICS_FILE,
                mode="a",
                header=False,
                index=False
            )

        print(
            f"[{metrics['timestamp']}] "
            f"CPU: {metrics['cpu_usage']}% | "
            f"Memory: {metrics['memory_usage']}% | "
            f"Latency: {metrics['api_latency']}ms | "
            f"Errors: {metrics['error_rate']}% | "
            f"Severity: {metrics['severity']}"
        )

        time.sleep(3)


if __name__ == "__main__":

    start_monitoring()