import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

class ThreatClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            random_state=42
        )
        self.label_encoder = LabelEncoder()
        self.feature_columns = []
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepare features and labels for classification"""
        feature_cols = ['bytes_sent', 'bytes_received', 'hour', 
                       'day_of_week', 'port']
        
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0
        
        self.feature_columns = feature_cols
        X = df[feature_cols].fillna(0)
        
        if 'label' in df.columns:
            y = self.label_encoder.fit_transform(df['label'])
            return X, y
        return X, None
    
    def train(self, df: pd.DataFrame):
        """Train the threat classification model"""
        X, y = self.prepare_features(df)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        print("\nThreat Classification Report:")
        print(classification_report(
            y_test, y_pred, 
            target_names=self.label_encoder.classes_
        ))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
    
    def predict(self, df: pd.DataFrame) -> tuple:
        """Predict threat types"""
        X, _ = self.prepare_features(df)
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        threat_types = self.label_encoder.inverse_transform(predictions)
        confidence = np.max(probabilities, axis=1)
        
        return threat_types, confidence
    
    def save_model(self, path: str):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_columns': self.feature_columns
        }, path)
    
    def load_model(self, path: str):
        """Load trained model"""
        data = joblib.load(path)
        self.model = data['model']
        self.label_encoder = data['label_encoder']
        self.feature_columns = data['feature_columns']