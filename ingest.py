import json
import pandas as pd
from sqlalchemy import create_engine

def ingest_json_to_db(json_file, db_url):
    with open(json_file, 'r') as f:
        data = json.load(f)

    accounts = pd.json_normalize(data, 'accounts')
    transactions = pd.json_normalize(data, record_path=['accounts', 'transactions'], meta=['accountId'])

    engine = create_engine(db_url)
    accounts.to_sql('accounts', engine, if_exists='replace', index=False)
    transactions.to_sql('transactions', engine, if_exists='replace', index=False)

    print("Data ingested successfully.")