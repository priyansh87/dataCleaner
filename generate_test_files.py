import pandas as pd
import os

def create_test_files():
    # 1. Create Input CSV
    input_data = {
        "raw_description": [
            "John Doe purchased a MacBook Pro for $2500 on 2024-01-15. He was happy.",
            "Sarah Connor returned a T-800 Exoskeleton valued at $500000. Reason: Defective.",
            "Bruce Wayne bought a Grappling Hook for $500. It's for spelunking."
        ],
        "transaction_id": ["TX1001", "TX1002", "TX1003"]
    }
    df_input = pd.DataFrame(input_data)
    df_input.to_csv("test_input.csv", index=False)
    print("Created test_input.csv")

    # 2. Create Reference Excel (Schema)
    # The app expects headers to be the fields
    schema_data = {
        "customer_name": [],
        "product_item": [],
        "amount": [],
        "transaction_date": [],
        "sentiment": []
    }
    df_schema = pd.DataFrame(schema_data)
    df_schema.to_excel("test_reference.xlsx", index=False)
    print("Created test_reference.xlsx")

if __name__ == "__main__":
    create_test_files()
