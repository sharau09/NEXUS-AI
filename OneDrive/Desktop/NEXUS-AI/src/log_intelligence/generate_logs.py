import pandas as pd
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

output_path = (
    BASE_DIR /
    "data" /
    "raw" /
    "system_logs.csv"
)


random.seed(42)


log_templates = [

    "ERROR Database connection timeout",

    "ERROR Database connection failed",

    "ERROR Database query timeout",

    "ERROR API request timeout",

    "WARNING API response slow",

    "WARNING High CPU usage detected",

    "WARNING High memory usage detected",

    "ERROR Payment service failed",

    "ERROR Authentication service unavailable",

    "ERROR Redis connection failed",

    "WARNING Disk usage high",

    "INFO User login successful",

    "INFO API request completed",

    "INFO Payment processed successfully",

    "INFO System health check completed"
]


services = [

    "payment-service",

    "user-service",

    "order-service",

    "database-service",

    "api-gateway",

    "authentication-service"
]


levels = [

    "INFO",

    "WARNING",

    "ERROR"
]


logs = []


for i in range(1000):

    message = random.choice(log_templates)

    service = random.choice(services)

    level = message.split()[0]

    logs.append({

        "timestamp": pd.Timestamp(
            "2026-01-01"
        ) + pd.Timedelta(
            minutes=i
        ),

        "service": service,

        "level": level,

        "message": message

    })


df = pd.DataFrame(logs)


df.to_csv(
    output_path,
    index=False
)


print("System logs generated successfully!")

print("Total logs:", len(df))

print("\nFirst 5 logs:")

print(df.head())