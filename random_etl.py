import pandas as pd
import json
from datetime import datetime
import s3fs
import requests

def run_customer_etl():

    response = requests.get('https://retoolapi.dev/i39UqK/data')
    data = response.json()
    if response.status_code == 200:
        print('scuccess')
    else:
        print("Error:", response.status_code)

    customer_list = []
    for res in data:
        customer = {
            "customerId": res["id"],  # Use dictionary key access
            "customer": res["names"],
            "payment": res["paid"],
            "address": res["location"],
            "pending": res["pending_amount"],
            "last_day_to_pay": res["last_date_to_pay"],
            "payment_type": res["Payment_Type"]  # Ensure case matches JSON
        }
        customer_list.append(customer)

    df = pd.DataFrame(customer_list)

    df.to_csv('s3://prayag-airflow/customers.csv')