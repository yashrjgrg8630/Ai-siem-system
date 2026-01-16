import time
import joblib
import pandas as pd

from backend.data.log_parser import LogParser
from data.sample_logs.datasets.log_generator import SecurityLogGenerator

# Load trained threat classifier
threat_classifier = joblib.load("models/saved_models/threat_classifier.pkl")

model = threat_classifier.model
label_encoder = threat_classifier.label_encoder
feature_columns = threat_classifier.feature_columns

parser = LogParser()
generator = SecurityLogGenerator()

print("\n=== Real-Time Threat Detection Started ===\n")

while True:
    # Generate one log
    log = generator.generate_log()
    df = pd.DataFrame([log])

    # Feature extraction
    df = parser.extract_features(df)

    # Ensure feature consistency
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    X = df[feature_columns]

    # Predict threat
    prediction = model.predict(X)[0]
    threat = label_encoder.inverse_transform([prediction])[0]

    # Alert logic
    if threat.lower() == "ddos":
        print("[CRITICAL ALERT] DDoS attack detected!")
    else:
        print(f"[INFO] Detected activity: {threat}")

    time.sleep(3)
