import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.feature_columns = []
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare numerical features for anomaly detection"""
        feature_cols = ['bytes_sent', 'bytes_received', 'hour', 
                       'day_of_week', 'port']
        
        # Handle missing columns
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0
        
        self.feature_columns = feature_cols
        X = df[feature_cols].fillna(0)
        return X
    
    def train(self, df: pd.DataFrame):
        """Train the anomaly detection model"""
        X = self.prepare_features(df)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        print("Anomaly detection model trained successfully")
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predict anomalies (-1 for anomaly, 1 for normal)"""
        X = self.prepare_features(df)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        # Get anomaly scores
        scores = self.model.score_samples(X_scaled)
        
        return predictions, scores
    
    def save_model(self, path: str):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }, path)
    
    def load_model(self, path: str):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.scaler = data['scaler']
        self.feature_columns = data['feature_columns']