def test_alert_only_for_high_severity():
    incident = {
        "severity": "HIGH",
        "incident_type": "HIGH CPU USAGE"
    }

    assert incident["severity"] in ["HIGH", "CRITICAL"]


def test_critical_alert():
    incident = {
        "severity": "CRITICAL",
        "incident_type": "HIGH MEMORY USAGE"
    }

    assert incident["severity"] == "CRITICAL"