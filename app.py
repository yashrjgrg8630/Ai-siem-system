from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

LOG_FILE = "data/sample_logs/datasets/training_logs.jsonl"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    logs = []
    with open(LOG_FILE) as f:
        for line in f:
            logs.append(json.loads(line))
    return jsonify(logs[-50:])

if __name__ == "__main__":
    app.run(debug=True)
