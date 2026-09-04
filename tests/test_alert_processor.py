import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_alert_data_exists():
    file_path = BASE_DIR / "alerts.json"
    assert file_path.exists()


def test_processed_alerts_exist():
    file_path = BASE_DIR / "processed_alerts.json"
    assert file_path.exists()


def test_processed_alert_count():
    file_path = BASE_DIR / "processed_alerts.json"

    with open(file_path, "r", encoding="utf-8") as file:
        alerts = json.load(file)

    assert len(alerts) == 3


def test_critical_alert_action():
    file_path = BASE_DIR / "processed_alerts.json"

    with open(file_path, "r", encoding="utf-8") as file:
        alerts = json.load(file)

    critical_alert = next(
        alert for alert in alerts
        if alert["severity"] == "critical"
    )

    assert critical_alert["action"] == "IMMEDIATE ACTION REQUIRED"