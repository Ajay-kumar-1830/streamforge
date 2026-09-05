def calculate_metrics(alerts):
    metrics = {
        "total": len(alerts),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for alert in alerts:
        severity = alert.get("severity", "low").lower()

        if severity in metrics:
            metrics[severity] += 1

    return metrics