import sys
from pathlib import Path
import json

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from producer.alert_producer import generate_alerts
from stream_processor.alert_validator import validate_alerts
from stream_processor.alert_processor import process_alerts
from metrics.alert_metrics import calculate_metrics


def run_pipeline(count=5):
    print("\n=== STREAMFORGE PIPELINE ===\n")

    # Step 1: Generate alerts
    alerts = generate_alerts(count)

    print(f"1. Generated alerts: {len(alerts)}")

    # Step 2: Validate alerts
    valid_alerts, invalid_alerts = validate_alerts(alerts)

    print(f"2. Valid alerts: {len(valid_alerts)}")
    print(f"   Invalid alerts: {len(invalid_alerts)}")

    # Step 3: Process valid alerts
    processed_alerts = process_alerts(valid_alerts)

    print(f"3. Processed alerts: {len(processed_alerts)}")

    # Step 4: Calculate metrics
    metrics = calculate_metrics(processed_alerts)

    print("\n=== METRICS ===")
    print(f"Total: {metrics['total']}")
    print(f"Critical: {metrics['critical']}")
    print(f"High: {metrics['high']}")
    print(f"Medium: {metrics['medium']}")
    print(f"Low: {metrics['low']}")

    # Step 5: Save pipeline results
    output_file = BASE_DIR / "pipeline_results.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            {
                "alerts": processed_alerts,
                "metrics": metrics
            },
            file,
            indent=4
        )

    print("\nPipeline completed successfully!")
    print("Results saved to: pipeline_results.json")


if __name__ == "__main__":
    run_pipeline(5)