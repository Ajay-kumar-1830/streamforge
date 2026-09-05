import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "state" / "pipeline_state.json"


def save_state(metrics, processed_count):
    state = {
        "processed_count": processed_count,
        "metrics": metrics,
        "last_updated": datetime.now().isoformat()
    }

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


def load_state():
    if not STATE_FILE.exists():
        return {
            "processed_count": 0,
            "metrics": {},
            "last_updated": None
        }

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    state = load_state()

    print("=== STREAMFORGE STATE ===")
    print(f"Processed alerts: {state['processed_count']}")
    print(f"Last updated: {state['last_updated']}")