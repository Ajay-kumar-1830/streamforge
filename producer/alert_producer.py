import json
import random
from datetime import datetime


SEVERITIES = ["low", "medium", "high", "critical"]

ALERT_TYPES = [
    "temperature",
    "security",
    "system",
    "network"
]


def generate_alert(alert_id):
    severity = random.choice(SEVERITIES)
    alert_type = random.choice(ALERT_TYPES)

    messages = {
        "temperature": "Temperature threshold exceeded",
        "security": "Unauthorized access detected",
        "system": "System health check completed",
        "network": "Network activity detected"
    }

    return {
        "id": alert_id,
        "type": alert_type,
        "message": messages[alert_type],
        "severity": severity,
        "timestamp": datetime.now().isoformat()
    }


def generate_alerts(count=5):
    return [generate_alert(i) for i in range(1, count + 1)]


def save_alerts(alerts):
    with open("generated_alerts.json", "w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=4)


if __name__ == "__main__":
    alerts = generate_alerts(5)
    save_alerts(alerts)

    print("=== STREAMFORGE ALERT PRODUCER ===")
    print(f"Generated {len(alerts)} alerts")
    print("Saved to generated_alerts.json")