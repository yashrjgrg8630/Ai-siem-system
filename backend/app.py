from flask import Flask, jsonify, render_template
import threading
import time
import json
from pathlib import Path
import subprocess
import sys

app = Flask(__name__)

LOG_FILE = Path("data/sample_logs/datasets/training_logs.jsonl")

# -------------------------
# Background log generator
# -------------------------
def auto_log_generator():
    generator_path = Path("data/sample_logs/datasets/log_generator.py")
    subprocess.Popen([sys.executable, str(generator_path)])

# -------------------------
# Routes
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    logs = []
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass
    return jsonify(logs[-100:])  # last 100 logs only

# -------------------------
# Start background thread
# -------------------------
def start_background_tasks():
    t = threading.Thread(target=auto_log_generator, daemon=True)
    t.start()

# -------------------------
if __name__ == "__main__":
    start_background_tasks()
    app.run(debug=True)
