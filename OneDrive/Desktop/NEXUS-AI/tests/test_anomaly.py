from src.realtime_monitoring.metrics_generator import classify_severity


def test_low_severity():
    metrics = {
        "cpu_usage": 30,
        "memory_usage": 40,
        "api_latency": 100,
        "error_rate": 1
    }

    assert classify_severity(metrics) == "LOW"


def test_critical_cpu():
    metrics = {
        "cpu_usage": 95,
        "memory_usage": 40,
        "api_latency": 100,
        "error_rate": 1
    }

    assert classify_severity(metrics) == "CRITICAL"


def test_high_latency():
    metrics = {
        "cpu_usage": 40,
        "memory_usage": 40,
        "api_latency": 800,
        "error_rate": 2
    }

    assert classify_severity(metrics) == "HIGH"