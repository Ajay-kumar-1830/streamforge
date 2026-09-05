from flask import Flask, jsonify
from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from stream_processor.pipeline import run_pipeline
from state.state_manager import load_state


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "StreamForge",
        "status": "running",
        "message": "Real-time alert processing API"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/alerts")
def get_alerts():
    file_path = BASE_DIR / "pipeline_results.json"

    if not file_path.exists():
        return jsonify({
            "alerts": [],
            "message": "No processed alerts available"
        })

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/metrics")
def get_metrics():
    file_path = BASE_DIR / "pipeline_results.json"

    if not file_path.exists():
        return jsonify({
            "total": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        })

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify(data.get("metrics", {}))


@app.route("/state")
def get_state():
    return jsonify(load_state())


@app.route("/process", methods=["POST"])
def process_alerts():
    run_pipeline(5)

    file_path = BASE_DIR / "pipeline_results.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return jsonify({
        "message": "Pipeline executed successfully",
        "data": data
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )