import os
os.environ["MPLCONFIGDIR"] = os.getcwd()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json(
    "data/sample_logs/datasets/training_logs.jsonl",
    lines=True
)

attack_counts = df["attack_type"].value_counts()

plt.figure()
attack_counts.plot(kind="bar")
plt.title("Attack Type Distribution")
plt.xlabel("Attack Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
