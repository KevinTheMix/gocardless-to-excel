#!/usr/bin/env python3

import requests
import sys
from lib.json_io import load_json, save_json

def get_transactions_json(access_token, account_id):
    url = f'https://bankaccountdata.gocardless.com/api/v2/accounts/{account_id}/transactions/'
    headers = { 'accept': 'application/json', 'Authorization': f'Bearer {access_token}' }
    response = requests.get(url, headers=headers)
    #print('Fetched transactions data')
    return response.json()

def main(tokens_file, transactions_file):
    tokens_json = load_json(tokens_file)
    accounts_json = load_json(accounts_file)
    transactions_json = get_transactions_json(tokens_json['access'], accounts_json['accounts'][0])
    save_json(transactions_json, transactions_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: 6.transactions.py <tokens_file> <accounts_file> <transactions_file>")
        sys.exit(1)
    tokens_file = sys.argv[1]
    accounts_file = sys.argv[2]
    transactions_file = sys.argv[3]
    main(tokens_file, transactions_file)
