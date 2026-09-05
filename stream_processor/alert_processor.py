import json
from pathlib import Path
from datetime import datetime
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from stream_processor.alert_validator import validate_alerts
from metrics.alert_metrics import calculate_metrics

INPUT_FILE = BASE_DIR / "alerts.json"
OUTPUT_FILE = BASE_DIR / "processed_alerts.json"


def load_alerts():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def process_alerts(alerts):
    processed = []

    for alert in alerts:
        severity = alert.get("severity", "low").lower()

        if severity == "critical":
            action = "IMMEDIATE ACTION REQUIRED"
        elif severity == "high":
            action = "HIGH PRIORITY ALERT"
        elif severity == "medium":
            action = "MONITOR ALERT"
        else:
            action = "NORMAL"

        processed.append({
            **alert,
            "action": action,
            "processed_at": datetime.now().isoformat()
        })

    return processed


def main():
    alerts = load_alerts()

    valid_alerts, invalid_alerts = validate_alerts(alerts)

    processed_alerts = process_alerts(valid_alerts)

    metrics = calculate_metrics(processed_alerts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(processed_alerts, file, indent=4)

    print("\n=== STREAMFORGE ALERT PROCESSOR ===\n")

    for alert in processed_alerts:
        print(
            f"[{alert['severity'].upper()}] "
            f"{alert['type']} → {alert['action']}"
        )

    print("\n=== ALERT METRICS ===")
    print(f"Total: {metrics['total']}")
    print(f"Critical: {metrics['critical']}")
    print(f"High: {metrics['high']}")
    print(f"Medium: {metrics['medium']}")
    print(f"Low: {metrics['low']}")

    print(f"\nInvalid alerts: {len(invalid_alerts)}")
    print("Processed results saved to: processed_alerts.json")


if __name__ == "__main__":
    main()