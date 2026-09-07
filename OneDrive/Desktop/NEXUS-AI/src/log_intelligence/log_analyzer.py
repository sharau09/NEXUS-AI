import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


BASE_DIR = Path(__file__).resolve().parent.parent.parent


input_path = (
    BASE_DIR /
    "data" /
    "raw" /
    "system_logs.csv"
)


output_path = (
    BASE_DIR /
    "data" /
    "processed" /
    "log_analysis_results.csv"
)


# Load logs
df = pd.read_csv(input_path)


print("Logs loaded successfully!")

print("Total logs:", len(df))


# Convert log messages into numerical vectors
vectorizer = TfidfVectorizer(
    stop_words="english"
)


X = vectorizer.fit_transform(
    df["message"]
)


print(
    "Text converted into vectors successfully!"
)


# Create clustering model
kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)


# Cluster similar logs
df["log_cluster"] = kmeans.fit_predict(X)


# Save results
df.to_csv(
    output_path,
    index=False
)


print(
    "Log clustering completed successfully!"
)


print("\nCluster Summary:")

print(
    df["log_cluster"]
    .value_counts()
)


print("\nExample Logs:")

print(
    df[
        [
            "level",
            "service",
            "message",
            "log_cluster"
        ]
    ].head(20)
)