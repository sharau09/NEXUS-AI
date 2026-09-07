import pandas as pd

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==========================================
# DATA PATHS
# ==========================================

anomaly_path = (
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


correlation_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "incident_correlation_results.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

anomaly_df = pd.read_csv(
    anomaly_path
)


logs_df = pd.read_csv(
    logs_path
)


correlation_df = pd.read_csv(
    correlation_path
)


print("All incident knowledge loaded successfully!")


# ==========================================
# CREATE KNOWLEDGE DOCUMENTS
# ==========================================

documents = []


# Incident documents
for _, row in anomaly_df.iterrows():

    document = (
        f"System incident. "
        f"Timestamp: {row.get('timestamp', 'unknown')}. "
        f"CPU usage: {row.get('cpu_usage', 'unknown')}. "
        f"Memory usage: {row.get('memory_usage', 'unknown')}. "
        f"API latency: {row.get('api_latency', 'unknown')}. "
        f"Error rate: {row.get('error_rate', 'unknown')}. "
        f"Severity: {row.get('severity', 'unknown')}. "
        f"Root cause: {row.get('root_cause', 'unknown')}. "
        f"Incident risk: {row.get('incident_risk', 'unknown')}."
    )

    documents.append(document)


# Log documents
for _, row in logs_df.iterrows():

    document = (
        f"System log. "
        f"Service: {row.get('service', 'unknown')}. "
        f"Level: {row.get('level', 'unknown')}. "
        f"Message: {row.get('message', 'unknown')}."
    )

    documents.append(document)


# Correlation documents
for _, row in correlation_df.iterrows():

    document = (
        f"Incident correlation. "
        f"Timestamp: {row.get('timestamp', 'unknown')}. "
        f"Severity: {row.get('severity', 'unknown')}. "
        f"Root cause: {row.get('root_cause', 'unknown')}. "
        f"Incident risk: {row.get('incident_risk', 'unknown')}. "
        f"Related log count: {row.get('related_log_count', 'unknown')}. "
        f"Related logs: {row.get('sample_related_logs', 'unknown')}."
    )

    documents.append(document)


print(
    "Total knowledge documents:",
    len(documents)
)


# ==========================================
# CREATE VECTOR DATABASE
# ==========================================

vectorizer = TfidfVectorizer(
    stop_words="english"
)


document_vectors = vectorizer.fit_transform(
    documents
)


print(
    "Knowledge base indexed successfully!"
)


# ==========================================
# SEARCH FUNCTION
# ==========================================

def search_incidents(
    question,
    top_k=5
):

    question_vector = vectorizer.transform(
        [question]
    )


    similarity_scores = cosine_similarity(
        question_vector,
        document_vectors
    ).flatten()


    top_indices = similarity_scores.argsort()[
        ::-1
    ][:top_k]


    results = []


    for index in top_indices:

        results.append({

            "document": documents[index],

            "similarity_score": round(
                float(
                    similarity_scores[index]
                ),
                4
            )

        })


    return results


# ==========================================
# TEST COPILOT
# ==========================================

if __name__ == "__main__":

    question = (
        "What is causing critical incidents?"
    )


    results = search_incidents(
        question
    )


    print("\nQUESTION:")

    print(question)


    print("\nTOP RESULTS:\n")


    for result in results:

        print(
            "Similarity:",
            result["similarity_score"]
        )

        print(
            result["document"]
        )

        print("-" * 80)