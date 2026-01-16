import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.alert_threshold = 0.8
        self.alerts = []
    
    def create_alert(self, threat_data: dict):
        """Create security alert"""
        alert = {
            'id': len(self.alerts) + 1,
            'timestamp': datetime.now().isoformat(),
            'threat_type': threat_data['threat_type'],
            'confidence': threat_data['confidence'],
            'source_ip': threat_data.get('source_ip', 'unknown'),
            'severity': threat_data['severity'],
            'status': 'NEW'
        }
        self.alerts.append(alert)
        
        if threat_data['confidence'] > self.alert_threshold:
            self.send_notification(alert)
        
        return alert
    
    def send_notification(self, alert: dict):
        """Send alert notification"""
        print(f"🚨 ALERT: {alert['threat_type']} detected from {alert['source_ip']}")
        print(f"   Severity: {alert['severity']} | Confidence: {alert['confidence']:.2%}")
        # Add email/Slack notification here