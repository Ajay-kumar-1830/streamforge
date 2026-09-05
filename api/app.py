from flask import Flask, jsonify
from pathlib import Path
import json
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from stream_processor.pipeline import run_pipeline
from state.state_manager import load_state


app = Flask(__name__)


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def home():
    return jsonify({
        "project": "StreamForge",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/alerts")
def alerts():
    file_path = BASE_DIR / "pipeline_results.json"

    if not file_path.exists():
        return jsonify({
            "alerts": [],
            "metrics": {}
        })

    with open(file_path, "r", encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.route("/metrics")
def metrics():
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
def state():
    return jsonify(load_state())


@app.route("/process", methods=["POST"])
def process():
    try:
        run_pipeline(5)

        file_path = BASE_DIR / "pipeline_results.json"

        if not file_path.exists():
            return jsonify({
                "success": False,
                "message": "Pipeline did not create results"
            }), 500

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return jsonify({
            "success": True,
            "message": "Pipeline executed successfully",
            "data": data
        })

    except Exception as error:
        print("PIPELINE ERROR:", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )