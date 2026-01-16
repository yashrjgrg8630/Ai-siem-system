import time
import json
import os

LOG_FILE = "data/sample_logs/datasets/training_logs.jsonl"

FILTER_ATTACK = None  
# Examples:
# FILTER_ATTACK = "ddos"
# FILTER_ATTACK = "port_scan"
# FILTER_ATTACK = "brute_force"


def follow(file):
    """Generator function that yields new lines as they are written"""
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(1)
            continue
        yield line


def main():
    print("\n=== REAL-TIME LOG VIEWER STARTED ===\n")

    if not os.path.exists(LOG_FILE):
        print("Log file not found!")
        return

    with open(LOG_FILE, "r") as f:
        log_lines = follow(f)

        for line in log_lines:
            try:
                log = json.loads(line)

                attack_type = log.get("attack_type", "unknown")

                # Filter logic
                if FILTER_ATTACK and attack_type != FILTER_ATTACK:
                    continue

                print(
                    f"[LOG] Time: {log.get('timestamp')} | "
                    f"Attack: {attack_type} | "
                    f"Source IP: {log.get('source_ip')}"
                )

            except json.JSONDecodeError:
                continue


if __name__ == "__main__":
    main()
