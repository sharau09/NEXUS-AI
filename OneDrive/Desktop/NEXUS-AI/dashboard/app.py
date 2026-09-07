import streamlit as st
import pandas as pd
import sys
import time
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.incident_copilot.llm_copilot import investigate_incident



 
from src.incident_copilot.history_manager import (
    load_history,
    clear_history
)


history = load_history()
if st.button("🗑️ Clear Investigation History"):

    clear_history()

    st.success(
        "Investigation history cleared successfully!"
    )

    st.rerun()
   
# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🚀",
    layout="wide"
)


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# LOAD MAIN DATA
# ==========================================

data_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "anomaly_results.csv"
)

df = pd.read_csv(data_path)


# ==========================================
# TITLE
# ==========================================

st.title("🚀 NEXUS AI")

st.subheader(
    "Autonomous AI Operations Intelligence Platform"
)


# ==========================================
# BASIC STATISTICS
# ==========================================

anomalies = df[
    df["anomaly"] == 1
]

total_records = len(df)

anomaly_count = len(anomalies)

normal_count = total_records - anomaly_count


anomaly_percentage = round(
    (anomaly_count / total_records) * 100,
    2
)


# ==========================================
# METRIC CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Records",
    total_records
)


col2.metric(
    "Normal Records",
    normal_count
)


col3.metric(
    "Anomalies Detected ⚠️",
    anomaly_count
)


col4.metric(
    "Anomaly Percentage",
    f"{anomaly_percentage}%"
)


st.divider()


# ==========================================
# SEVERITY DISTRIBUTION
# ==========================================

st.subheader(
    "🚨 Incident Severity Distribution"
)


severity_counts = (
    df["severity"]
    .value_counts()
)


st.bar_chart(
    severity_counts
)


# ==========================================
# API LATENCY
# ==========================================

st.subheader(
    "📊 API Latency Monitoring"
)


st.line_chart(
    df["api_latency"]
)


# ==========================================
# CPU USAGE
# ==========================================

st.subheader(
    "🖥️ CPU Usage"
)


st.line_chart(
    df["cpu_usage"]
)


# ==========================================
# MEMORY USAGE
# ==========================================

st.subheader(
    "💾 Memory Usage"
)


st.line_chart(
    df["memory_usage"]
)


# ==========================================
# ERROR RATE
# ==========================================

st.subheader(
    "⚠️ Error Rate"
)


st.line_chart(
    df["error_rate"]
)


st.divider()


# ==========================================
# AI DETECTED ANOMALIES
# ==========================================

st.subheader(
    "🚨 AI Detected Anomalies"
)


st.dataframe(
    anomalies.head(50),
    use_container_width=True
)


st.divider()


# ==========================================
# ROOT CAUSE ANALYSIS
# ==========================================

st.subheader(
    "🧠 AI Root Cause Analysis"
)


root_cause_counts = (
    anomalies["root_cause"]
    .value_counts()
)


st.bar_chart(
    root_cause_counts
)


st.divider()


# ==========================================
# INCIDENT RISK PREDICTION
# ==========================================

st.subheader(
    "🔮 AI Incident Risk Prediction"
)


risk_counts = (
    df["incident_risk"]
    .value_counts()
)


st.bar_chart(
    risk_counts
)


st.subheader(
    "⚠️ High Risk Incidents"
)


high_risk = df[
    df["incident_risk"] == "HIGH"
]


st.dataframe(
    high_risk.head(20),
    use_container_width=True
)


st.divider()


# ==========================================
# AI INCIDENT CORRELATION
# ==========================================

st.subheader(
    "🔗 AI Incident Correlation"
)


correlation_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "incident_correlation_results.csv"
)


# Check if correlation file exists
if correlation_path.exists():

    correlation_df = pd.read_csv(
        correlation_path
    )


    col1, col2 = st.columns(2)


    col1.metric(
        "Correlated Incidents",
        len(correlation_df)
    )


    col2.metric(
        "Related Logs",
        int(
            correlation_df[
                "related_log_count"
            ].sum()
        )
    )


    st.subheader(
        "🔍 Correlated Incident Investigation"
    )


    st.dataframe(
        correlation_df.head(50),
        use_container_width=True
    )


else:

    st.warning(
        "Incident correlation results not found. "
        "Please run correlation_engine.py first."
    )

st.divider()

st.subheader("🤖 NEXUS AI Incident Copilot")

question = st.text_input(
    "Ask NEXUS AI about your incidents:",
    placeholder="Example: What is causing critical incidents?"
)


if question:

    from src.incident_copilot.copilot_engine import (
        search_incidents
    )


    results = search_incidents(
        question
    )


    st.subheader("🔍 AI Investigation Results")


    for result in results:

        st.write(
            f"**Relevance Score:** "
            f"{result['similarity_score']}"
        )

        st.info(
            result["document"]
        )


st.divider()

st.header("🤖 NEXUS AI Incident Copilot")

st.write(
    "Ask NEXUS AI to investigate system incidents "
    "using your incident knowledge base."
)

question = st.text_area(
    "Describe the incident or ask a question:",
    placeholder=(
        "Example: Why is API latency increasing "
        "and what should engineers investigate?"
    ),
    height=120
)


if st.button(
    "🔍 Investigate Incident",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "⚠️ Please enter an incident question."
        )

    else:

        with st.spinner(
            "🧠 NEXUS AI is searching evidence and investigating..."
        ):

            try:

                result = investigate_incident(
                    question.strip()
                )

                st.success(
                    "✅ Investigation completed successfully!"
                )

                # Investigation Report
                st.subheader(
                    "📋 AI Investigation Report"
                )

                st.markdown(
                    result["answer"]
                )

                # Evidence section
                with st.expander(
                    "🔍 View Evidence Used"
                ):

                    evidence_results = result.get(
                        "evidence",
                        []
                    )

                    if evidence_results:

                        for i, item in enumerate(
                            evidence_results,
                            start=1
                        ):

                            st.markdown(
                                f"### Evidence {i}"
                            )

                            st.write(
                                item.get(
                                    "document",
                                    "No evidence available."
                                )
                            )

                            st.divider()

                    else:

                        st.warning(
                            "No evidence was found."
                        )

            except Exception as e:

                st.error(
                    f"❌ Investigation failed: {str(e)}"
                )

st.divider()

st.header("📜 Investigation History")

history = load_history()

if history:

    for item in reversed(history):

        title = (
            f"🕒 {item['timestamp']} — "
            f"{item['question'][:60]}"
        )

        with st.expander(title):

            st.subheader("❓ Question")

            st.write(
                item["question"]
            )

            st.subheader(
                "🤖 AI Investigation"
            )

            st.markdown(
                item["answer"]
            )

            st.caption(
                f"Evidence Used: "
                f"{item['evidence_count']}"
            )

else:

    st.info(
        "No investigation history yet."
    )

st.divider()

st.header("📡 Real-Time System Monitoring")

REALTIME_FILE = (
    BASE_DIR /
    "data" /
    "realtime" /
    "live_metrics.csv"
)


if REALTIME_FILE.exists():

    realtime_df = pd.read_csv(
        REALTIME_FILE
    )

    if not realtime_df.empty:

        latest = realtime_df.iloc[-1]

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "🖥️ CPU",
            f"{latest['cpu_usage']}%"
        )

        col2.metric(
            "💾 Memory",
            f"{latest['memory_usage']}%"
        )

        col3.metric(
            "⚡ API Latency",
            f"{latest['api_latency']} ms"
        )

        col4.metric(
            "⚠️ Error Rate",
            f"{latest['error_rate']}%"
        )

        col5.metric(
            "🚨 Severity",
            latest["severity"]
        )

        st.subheader(
            "📈 Live CPU Usage"
        )

        st.line_chart(
            realtime_df.tail(50).set_index(
                "timestamp"
            )["cpu_usage"]
        )

        st.subheader(
            "📈 Live API Latency"
        )

        st.line_chart(
            realtime_df.tail(50).set_index(
                "timestamp"
            )["api_latency"]
        )

        st.subheader(
            "📈 Live Error Rate"
        )

        st.line_chart(
            realtime_df.tail(50).set_index(
                "timestamp"
            )["error_rate"]
        )

else:

    st.warning(
        "⚠️ Real-time monitoring is not running yet."
    )

    st.info(
        "Run this command in another terminal:\n\n"
        "python -m src.realtime_monitoring.metrics_generator"
    )

import json


st.divider()

st.header("🚨 Automatic Incident Detection")

INCIDENT_FILE = (
    BASE_DIR /
    "data" /
    "incidents" /
    "auto_incidents.json"
)


if INCIDENT_FILE.exists():

    try:

        with open(
            INCIDENT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            incidents = json.load(file)


        if incidents:

            open_incidents = [
                incident
                for incident in incidents
                if incident["status"] == "OPEN"
            ]


            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🚨 Total Incidents",
                len(incidents)
            )

            col2.metric(
                "🔴 Open Incidents",
                len(open_incidents)
            )

            critical_count = sum(
                1
                for incident in incidents
                if incident["severity"] == "CRITICAL"
            )

            col3.metric(
                "🔥 Critical Incidents",
                critical_count
            )


            st.subheader(
                "🚨 Latest Detected Incidents"
            )

            incidents_df = pd.DataFrame(
                list(
                    reversed(incidents)
                )
            )

            st.dataframe(
                incidents_df,
                use_container_width=True
            )

        else:

            st.info(
                "No incidents detected yet."
            )

    except Exception as e:

        st.error(
            f"Could not load incidents: {e}"
        )

else:

    st.warning(
        "Incident detector is not running yet."
    )

st.divider()

st.header("🔔 NEXUS AI Smart Alerts")

ALERT_FILE = (
    BASE_DIR
    / "data"
    / "alerts"
    / "alerts.json"
)


if ALERT_FILE.exists():

    try:

        with open(
            ALERT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            alerts = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        alerts = []


    if alerts:

        active_alerts = [
            alert
            for alert in alerts
            if alert["status"] == "ACTIVE"
            and not alert["acknowledged"]
        ]


        critical_alerts = [
            alert
            for alert in active_alerts
            if alert["severity"] == "CRITICAL"
        ]


        high_alerts = [
            alert
            for alert in active_alerts
            if alert["severity"] == "HIGH"
        ]


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "🔔 Active Alerts",
            len(active_alerts)
        )


        col2.metric(
            "🔥 Critical",
            len(critical_alerts)
        )


        col3.metric(
            "⚠️ High",
            len(high_alerts)
        )


        st.subheader(
            "🚨 Active Alerts"
        )


        if active_alerts:

            for alert in reversed(
                active_alerts
            ):

                if alert["severity"] == "CRITICAL":

                    st.error(
                        f"🔥 CRITICAL: "
                        f"{alert['message']}\n\n"
                        f"Root Cause: "
                        f"{alert['root_cause']}"
                    )

                else:

                    st.warning(
                        f"⚠️ HIGH: "
                        f"{alert['message']}\n\n"
                        f"Root Cause: "
                        f"{alert['root_cause']}"
                    )

                st.caption(
                    f"Alert ID: {alert['alert_id']} | "
                    f"Time: {alert['timestamp']}"
                )

        else:

            st.success(
                "✅ No active alerts."
            )


        st.subheader(
            "📋 Alert History"
        )


        alerts_df = pd.DataFrame(
            list(reversed(alerts))
        )


        st.dataframe(
            alerts_df,
            use_container_width=True
        )


    else:

        st.success(
            "✅ No alerts generated yet."
        )

else:

    st.info(
        "🔔 Alert engine has not generated alerts yet."
    )