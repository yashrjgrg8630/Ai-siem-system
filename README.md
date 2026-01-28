🔐 AI-Driven SIEM System
Overview

An AI-driven Security Information and Event Management (SIEM) system that continuously analyzes system logs to detect cyber attacks, classify threats using machine learning, and assess their severity in near real time, helping security teams identify and respond to incidents efficiently.

Features

Real-time log generation to simulate continuous system activity

Detection of cyber attacks such as:

DDoS attacks

Port scanning

Brute-force login attempts

Machine-learning-based attack classification

Automated severity scoring (Low, Medium, High)

Interactive web dashboard for live monitoring

Advanced filtering and search by IP address and attack type

Security analytics including attack timelines and top threat sources

Simulated email alerts for high-severity incidents

Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS, JavaScript

Machine Learning: Scikit-learn

Visualization: Chart.js

Version Control: Git, GitHub

How It Works

The system continuously generates and ingests log data simulating real network events.

Logs are analyzed by rule-based detection and machine learning models to identify and classify attacks.

Detected threats are assigned a severity score and displayed on a real-time dashboard, with alerts triggered for critical events.

Results / Output

Successful identification of multiple attack types from simulated logs

Accurate classification of malicious vs normal activity

Clear visualization of attack trends and threat sources

Real-time alerts for high-risk security incidents, simulating SOC behavior

How to Run
Prerequisites

Python 3.8 or above

Git

Steps
git clone https://github.com/yashrjgrg8630/Ai-siem-system.git
cd Ai-siem-system
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py


After starting the application, open your browser and access the web dashboard to view live logs, detected attacks, analytics, and alerts.
