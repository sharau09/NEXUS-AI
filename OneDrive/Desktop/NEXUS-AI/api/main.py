from fastapi import FastAPI
from src.incident_copilot.copilot_engine import search_incidents
import pandas as pd

app = FastAPI(
    title="NEXUS AI",
    description="Autonomous AI Operations Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "NEXUS AI is running successfully 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/metrics")
def get_metrics():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    return df.head(20).to_dict(
        orient="records"
    )

@app.get("/anomalies")
def get_anomalies():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    anomalies = df[
        df["anomaly"] == 1
    ]

    return anomalies.to_dict(
        orient="records"
    )

@app.get("/summary")
def get_summary():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    total_records = len(df)

    anomaly_count = int(
        df["anomaly"].sum()
    )

    normal_count = total_records - anomaly_count

    anomaly_percentage = round(
        (anomaly_count / total_records) * 100,
        2
    )

    return {
        "total_records": total_records,
        "normal_records": normal_count,
        "anomalies_detected": anomaly_count,
        "anomaly_percentage": anomaly_percentage
    }

@app.get("/incidents")
def get_incidents():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    incidents = df[
        df["anomaly"] == 1
    ]

    return incidents.to_dict(
        orient="records"
    )

@app.get("/severity-summary")
def severity_summary():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    summary = (
        df["severity"]
        .value_counts()
        .to_dict()
    )

    return summary

@app.get("/root-causes")
def get_root_causes():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    incidents = df[
        df["anomaly"] == 1
    ]

    results = incidents[
        [
            "timestamp",
            "cpu_usage",
            "memory_usage",
            "api_latency",
            "error_rate",
            "severity",
            "root_cause"
        ]
    ]

    return results.to_dict(
        orient="records"
    )

@app.get("/root-cause-summary")
def root_cause_summary():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    incidents = df[
        df["anomaly"] == 1
    ]

    summary = (
        incidents["root_cause"]
        .value_counts()
        .to_dict()
    )

    return summary

@app.get("/incident-risk-summary")
def incident_risk_summary():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    summary = (
        df["incident_risk"]
        .value_counts()
        .to_dict()
    )

    return summary

@app.get("/high-risk-incidents")
def high_risk_incidents():

    df = pd.read_csv(
        "data/processed/anomaly_results.csv"
    )

    high_risk = df[
        df["incident_risk"] == "HIGH"
    ]

    return high_risk.to_dict(
        orient="records"
    )

@app.get("/incident-correlations")
def get_incident_correlations():

    df = pd.read_csv(
        "data/processed/incident_correlation_results.csv"
    )

    return df.head(100).to_dict(
        orient="records"
    )

@app.get("/correlation-summary")
def correlation_summary():

    df = pd.read_csv(
        "data/processed/incident_correlation_results.csv"
    )

    return {

        "total_correlated_incidents": len(df),

        "total_related_logs": int(
            df["related_log_count"].sum()
        ),

        "average_related_logs": round(
            df["related_log_count"].mean(),
            2
        )

    }

@app.get("/copilot")
def incident_copilot(
    question: str
):

    results = search_incidents(
        question
    )

    return {

        "question": question,

        "relevant_evidence": results

    }

