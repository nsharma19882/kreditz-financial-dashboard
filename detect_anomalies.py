def detect_anomalies(df, threshold=10000):
    df['is_anomaly'] = df['amount'].abs() > threshold
    df['is_duplicate'] = df.duplicated(subset=['date', 'amount', 'description'], keep=False)
    return df

# File: app.py
from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine
from categorize import categorize_transactions
from detect_anomalies import detect_anomalies

app = Flask(__name__)
engine = create_engine('sqlite:///finance.db')

@app.route('/')
def report():
    transactions = pd.read_sql("SELECT * FROM transactions", engine)
    transactions = categorize_transactions(transactions)
    transactions = detect_anomalies(transactions)

    transactions['month'] = pd.to_datetime(transactions['date']).dt.to_period('M')
    report_data = transactions.groupby(['accountId', 'month', 'category']).agg(
        total_amount=pd.NamedAgg(column='amount', aggfunc='sum'),
        count=pd.NamedAgg(column='amount', aggfunc='count'),
        anomalies=pd.NamedAgg(column='is_anomaly', aggfunc='sum')
    ).reset_index()

    return render_template('report.html', tables=report_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)