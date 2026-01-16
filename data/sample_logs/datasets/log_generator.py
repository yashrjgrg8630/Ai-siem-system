import json
import random
import time
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "training_logs.jsonl"

ATTACK_TYPES = ["ddos", "port_scan", "brute_force", "normal"]
PORTS = [22, 80, 443, 8080, 3306]

def generate_log():
    attack = random.choices(
        ATTACK_TYPES,
        weights=[0.4, 0.2, 0.2, 0.2],
        k=1
    )[0]

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": f"192.168.1.{random.randint(1, 254)}",
        "destination_port": random.choice(PORTS),
        "attack_type": attack
    }

def append_log():
    log = generate_log()
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    print("Log generated:", log)

if __name__ == "__main__":
    while True:
        append_log()
        time.sleep(5)
