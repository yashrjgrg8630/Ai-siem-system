import json

log_file = "data/sample_logs/datasets/training_logs.jsonl"

target_attack = "ddos"   # yaha jo check karna ho wo likho

count = 0

with open(log_file, "r") as f:
    for line in f:
        log = json.loads(line)
        if log.get("attack_type") == target_attack:
            count += 1

print(f"Total '{target_attack}' logs found:", count)
