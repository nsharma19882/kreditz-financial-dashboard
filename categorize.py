def categorize_transactions(df):
    def categorize(description):
        if "salary" in description.lower():
            return "Income"
        elif "transfer" in description.lower():
            return "Internal Transfer"
        else:
            return "Expense"

    df['category'] = df['description'].apply(categorize)
    return df