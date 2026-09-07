import json
import time
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INCIDENT_FILE = (
    BASE_DIR
    / "data"
    / "incidents"
    / "auto_incidents.json"
)

ALERT_DIR = (
    BASE_DIR
    / "data"
    / "alerts"
)

ALERT_FILE = (
    ALERT_DIR
    / "alerts.json"
)


# ==========================================
# LOAD ALERTS
# ==========================================

def load_alerts():

    if not ALERT_FILE.exists():
        return []

    try:

        with open(
            ALERT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


# ==========================================
# SAVE ALERTS
# ==========================================

def save_alerts(alerts):

    ALERT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        ALERT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            alerts,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==========================================
# CREATE ALERT
# ==========================================

def create_alert(incident):

    return {

        "alert_id": (
            "ALT-"
            + datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        ),

        "incident_id": incident[
            "incident_id"
        ],

        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "severity": incident[
            "severity"
        ],

        "incident_type": incident[
            "incident_type"
        ],

        "root_cause": incident[
            "possible_root_cause"
        ],

        "message": (
            f"{incident['severity']} alert: "
            f"{incident['incident_type']}"
        ),

        "status": "ACTIVE",

        "acknowledged": False

    }


# ==========================================
# CHECK NEW INCIDENTS
# ==========================================

def process_incidents():

    incidents = []

    if INCIDENT_FILE.exists():

        try:

            with open(
                INCIDENT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                incidents = json.load(file)

        except (
            json.JSONDecodeError,
            OSError
        ):

            incidents = []


    alerts = load_alerts()

    existing_incident_ids = {
        alert["incident_id"]
        for alert in alerts
    }


    for incident in incidents:

        # Only create alerts for HIGH/CRITICAL
        if incident["severity"] not in [
            "HIGH",
            "CRITICAL"
        ]:

            continue


        incident_id = incident[
            "incident_id"
        ]


        # Prevent duplicate alerts
        if incident_id in existing_incident_ids:

            continue


        alert = create_alert(
            incident
        )

        alerts.append(
            alert
        )

        print("\n" + "=" * 60)

        print("🔔 NEW ALERT")

        print(
            f"Alert ID: {alert['alert_id']}"
        )

        print(
            f"Severity: {alert['severity']}"
        )

        print(
            f"Incident: {alert['incident_type']}"
        )

        print(
            f"Message: {alert['message']}"
        )

        print("=" * 60)


    save_alerts(alerts)


# ==========================================
# CONTINUOUS ALERT MONITOR
# ==========================================

def start_alert_monitor():

    print("=" * 60)

    print(
        "🔔 NEXUS AI ALERT ENGINE STARTED"
    )

    print("=" * 60)


    while True:

        process_incidents()

        time.sleep(3)


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    start_alert_monitor()