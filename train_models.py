import os
import sys
import pickle
import pandas as pd

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Project imports
from backend.data.log_parser import LogParser
from backend.models.anomaly_detector import AnomalyDetector
from backend.models.threat_classifier import ThreatClassifier
from data.sample_logs.datasets.log_generator import SecurityLogGenerator


def main():
    print("\n=== AI-SIEM Training Pipeline Started ===\n")

    # -----------------------------------
    # Step 1: Generate synthetic logs
    # -----------------------------------
    print("Step 1: Generating logs...")
    dataset_dir = "data/sample_logs/datasets"
    os.makedirs(dataset_dir, exist_ok=True)

    log_file = os.path.join(dataset_dir, "training_logs.jsonl")

    generator = SecurityLogGenerator()
    generator.generate_dataset(log_file)

    # -----------------------------------
    # Step 2: Parse logs
    # -----------------------------------
    print("Step 2: Parsing logs...")
    parser = LogParser()
    df = parser.parse_json_logs(log_file)

    if df.empty:
        raise ValueError("Parsed DataFrame is empty")

    # -----------------------------------
    # Step 3: Feature extraction
    # -----------------------------------
    print("Step 3: Extracting features...")
    df = parser.extract_features(df)

    # -----------------------------------
    # Step 4: Prepare training data
    # -----------------------------------
    print("Step 4: Preparing training data...")
    X = df[['hour', 'day_of_week']]

    # Label: normal = 0, attack = 1
    y = df['attack_type'].apply(lambda x: 0 if x == "normal" else 1)

    # -----------------------------------
    # Step 5: Train anomaly detector
    # -----------------------------------
    print("Step 5: Training anomaly detector...")
    anomaly_detector = AnomalyDetector()
    anomaly_detector.train(X)

    # -----------------------------------
    # Step 6: Train threat classifier (✅ FIXED)
    # -----------------------------------
    print("Step 6: Training threat classifier...")

    df['label'] = df['attack_type']   # ✅ REQUIRED LINE

    threat_classifier = ThreatClassifier()
    threat_classifier.train(df)       # ✅ PASS ONLY df

    # -----------------------------------
    # Step 7: Save models
    # -----------------------------------
    print("Step 7: Saving models...")
    model_dir = "models/saved_models"
    os.makedirs(model_dir, exist_ok=True)

    with open(os.path.join(model_dir, "anomaly_detector.pkl"), "wb") as f:
        pickle.dump(anomaly_detector, f)

    with open(os.path.join(model_dir, "threat_classifier.pkl"), "wb") as f:
        pickle.dump(threat_classifier, f)

    print("\n✅ Training completed successfully!")


if __name__ == "__main__":
    main()
