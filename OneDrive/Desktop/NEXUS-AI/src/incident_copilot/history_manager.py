import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

HISTORY_DIR = (
    BASE_DIR /
    "data" /
    "history"
)

HISTORY_FILE = (
    HISTORY_DIR /
    "investigation_history.json"
)


def save_investigation(
    question,
    answer,
    evidence
):

    # Create history directory if needed
    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create investigation record
    investigation = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "question": question,
        "answer": answer,
        "evidence_count": len(evidence)
    }

    # Load existing history
    if HISTORY_FILE.exists():

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except (
            json.JSONDecodeError,
            OSError
        ):

            history = []

    else:

        history = []

    # Add new investigation
    history.append(
        investigation
    )

    # Save history
    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )

    return investigation


def load_history():

    if not HISTORY_FILE.exists():

        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []

def clear_history():

    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=4
        )