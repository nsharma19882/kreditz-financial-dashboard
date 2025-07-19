from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine
from categorize import categorize_transactions
from detect_anomalies import detect_anomalies

app = Flask(__name__)

# Replace with your DB URL if needed (e.g., PostgreSQL)
engine = create_engine('sqlite:///finance.db')


@app.route('/')
def monthly_report():
    # Load data from DB
    transactions = pd.read_sql("SELECT * FROM transactions", engine)

    # Apply categorization and anomaly detection
    transactions = categorize_transactions(transactions)
    transactions = detect_anomalies(transactions)

    # Extract month from transaction date
    transactions['month'] = pd.to_datetime(transactions['date']).dt.to_period('M')

    # Generate report data
    report_data = transactions.groupby(['accountId', 'month', 'category']).agg(
        total_amount=pd.NamedAgg(column='amount', aggfunc='sum'),
        count=pd.NamedAgg(column='amount', aggfunc='count'),
        anomalies=pd.NamedAgg(column='is_anomaly', aggfunc='sum')
    ).reset_index()

    return render_template('report.html', tables=report_data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
