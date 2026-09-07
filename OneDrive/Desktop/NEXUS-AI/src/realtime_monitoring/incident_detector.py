import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

REALTIME_FILE = (
    BASE_DIR /
    "data" /
    "realtime" /
    "live_metrics.csv"
)

INCIDENT_DIR = (
    BASE_DIR /
    "data" /
    "incidents"
)

INCIDENT_FILE = (
    INCIDENT_DIR /
    "auto_incidents.json"
)


def detect_incident(metrics):

    incidents = []

    if metrics["cpu_usage"] >= 90:

        incidents.append(
            {
                "type": "HIGH CPU USAGE",
                "severity": "CRITICAL",
                "root_cause": "Possible CPU resource exhaustion"
            }
        )

    if metrics["memory_usage"] >= 90:

        incidents.append(
            {
                "type": "HIGH MEMORY USAGE",
                "severity": "CRITICAL",
                "root_cause": "Possible memory leak or memory exhaustion"
            }
        )

    if metrics["api_latency"] >= 1000:

        incidents.append(
            {
                "type": "HIGH API LATENCY",
                "severity": "CRITICAL",
                "root_cause": "Possible database, network, or service bottleneck"
            }
        )

    if metrics["error_rate"] >= 20:

        incidents.append(
            {
                "type": "HIGH ERROR RATE",
                "severity": "CRITICAL",
                "root_cause": "Possible application or service failure"
            }
        )

    # High severity conditions
    if (
        metrics["cpu_usage"] >= 75
        and metrics["cpu_usage"] < 90
    ):

        incidents.append(
            {
                "type": "HIGH CPU USAGE",
                "severity": "HIGH",
                "root_cause": "Increasing CPU pressure"
            }
        )

    if (
        metrics["memory_usage"] >= 75
        and metrics["memory_usage"] < 90
    ):

        incidents.append(
            {
                "type": "HIGH MEMORY USAGE",
                "severity": "HIGH",
                "root_cause": "Increasing memory pressure"
            }
        )

    if (
        metrics["api_latency"] >= 700
        and metrics["api_latency"] < 1000
    ):

        incidents.append(
            {
                "type": "HIGH API LATENCY",
                "severity": "HIGH",
                "root_cause": "Possible performance bottleneck"
            }
        )

    if (
        metrics["error_rate"] >= 10
        and metrics["error_rate"] < 20
    ):

        incidents.append(
            {
                "type": "HIGH ERROR RATE",
                "severity": "HIGH",
                "root_cause": "Increasing application errors"
            }
        )

    return incidents


def load_incidents():

    if not INCIDENT_FILE.exists():

        return []

    try:

        with open(
            INCIDENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_incidents(incidents):

    INCIDENT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        INCIDENT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            incidents,
            file,
            indent=4,
            ensure_ascii=False
        )


def create_incident(metric_data, incident):

    return {
        "incident_id": (
            "INC-" +
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        ),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "incident_type": incident["type"],
        "severity": incident["severity"],
        "possible_root_cause": incident[
            "root_cause"
        ],
        "cpu_usage": float(
            metric_data["cpu_usage"]
        ),
        "memory_usage": float(
            metric_data["memory_usage"]
        ),
        "api_latency": float(
            metric_data["api_latency"]
        ),
        "error_rate": float(
            metric_data["error_rate"]
        ),
        "status": "OPEN"
    }


def monitor_incidents():

    print("=" * 60)
    print("🚨 NEXUS AI AUTOMATIC INCIDENT DETECTOR STARTED")
    print("=" * 60)

    INCIDENT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    processed_rows = 0

    while True:

        if not REALTIME_FILE.exists():

            print(
                "Waiting for real-time metrics..."
            )

            time.sleep(3)

            continue

        try:

            df = pd.read_csv(
                REALTIME_FILE
            )

        except Exception:

            time.sleep(2)

            continue

        if len(df) <= processed_rows:

            time.sleep(2)

            continue

        new_rows = df.iloc[
            processed_rows:
        ]

        saved_incidents = load_incidents()

        for _, row in new_rows.iterrows():

            detected = detect_incident(
                row
            )

            for incident in detected:

                new_incident = create_incident(
                    row,
                    incident
                )

                saved_incidents.append(
                    new_incident
                )

                print(
                    f"\n🚨 INCIDENT DETECTED"
                )

                print(
                    f"ID: {new_incident['incident_id']}"
                )

                print(
                    f"TYPE: "
                    f"{new_incident['incident_type']}"
                )

                print(
                    f"SEVERITY: "
                    f"{new_incident['severity']}"
                )

                print(
                    f"ROOT CAUSE: "
                    f"{new_incident['possible_root_cause']}"
                )

        save_incidents(
            saved_incidents
        )

        processed_rows = len(df)

        time.sleep(2)


if __name__ == "__main__":

    monitor_incidents()