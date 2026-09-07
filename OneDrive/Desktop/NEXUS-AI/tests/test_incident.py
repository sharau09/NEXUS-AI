def test_incident_structure():
    incident = {
        "incident_id": "INC-001",
        "severity": "HIGH",
        "incident_type": "HIGH CPU USAGE"
    }

    assert "incident_id" in incident
    assert "severity" in incident
    assert incident["severity"] in [
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]