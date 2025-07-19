# Kreditz Financial Dashboard

This project ingests banking data, categorizes transactions, detects anomalies, and displays monthly summaries via a Flask dashboard.

## Features
- Data ingestion from JSON
- Transaction categorization
- Anomaly detection
- Monthly report in a web dashboard

## Setup
```bash
pip install -r requirements.txt
python ingest.py kreditz-demo-bank-data.json sqlite:///finance.db
python app.py
```