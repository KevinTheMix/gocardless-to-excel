#!/usr/bin/env python3

import requests
import sys
from lib.json_io import load_json, save_json

def get_accounts(access_token, requisition_id):
    url = f'https://bankaccountdata.gocardless.com/api/v2/requisitions/{requisition_id}/'
    headers = { 'accept': 'application/json', 'Authorization': f'Bearer {access_token}' }
    response = requests.get(url, headers=headers)
    return response.json()

def main(tokens_file, accounts_file, requisition_id):
    tokens_json = load_json(tokens_file)
    accounts_json = get_accounts(tokens_json['access'], requisition_id)
    save_json(accounts_json, accounts_file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: 5.accounts.py <tokens_file> <accounts_file> <<requisition_id>")
        sys.exit(1)

    tokens_file = sys.argv[1]
    accounts_file = sys.argv[2]
    requisition_id = sys.argv[3]
    main(tokens_file, accounts_file, requisition_id)
