REQUIRED_FIELDS = [
    "id",
    "type",
    "message",
    "severity",
    "timestamp"
]

VALID_SEVERITIES = {
    "low",
    "medium",
    "high",
    "critical"
}


def validate_alert(alert):
    for field in REQUIRED_FIELDS:
        if field not in alert:
            return False

    severity = alert["severity"].lower()

    if severity not in VALID_SEVERITIES:
        return False

    if not alert["message"]:
        return False

    return True


def validate_alerts(alerts):
    valid_alerts = []
    invalid_alerts = []

    for alert in alerts:
        if validate_alert(alert):
            valid_alerts.append(alert)
        else:
            invalid_alerts.append(alert)

    return valid_alerts, invalid_alerts