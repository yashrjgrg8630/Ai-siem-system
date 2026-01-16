import json
import pandas as pd
from typing import List, Dict
import re

class LogParser:
    def __init__(self):
        self.supported_formats = ['json', 'syslog', 'csv']
    
    def parse_json_logs(self, file_path: str) -> pd.DataFrame:
        """Parse JSON formatted logs"""
        logs = []
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return pd.DataFrame(logs)
    
    def parse_syslog(self, log_line: str) -> Dict:
        """Parse standard syslog format"""
        # Example: Jan 15 10:30:45 server sshd[1234]: Failed password for user from 192.168.1.100
        pattern = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+?)(\[\d+\])?:\s+(.*)'
        match = re.match(pattern, log_line)
        
        if match:
            return {
                'timestamp': match.group(1),
                'host': match.group(2),
                'process': match.group(3),
                'message': match.group(5)
            }
        return {}
    
    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract features for ML model"""
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        return df