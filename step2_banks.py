#!/usr/bin/env python3

import requests
import sys
from lib.json_io import load_json, save_json

def get_banks_json(access_token):
    url = 'https://bankaccountdata.gocardless.com/api/v2/institutions/?country=be'
    headers = { 'accept': 'application/json', 'Authorization': f'Bearer {access_token}' }
    response = requests.get(url, headers=headers)
    #print('Fetched banks data')
    return response.json()

def main(tokens_file, banks_file):
    tokens_json = load_json(tokens_file)
    banks_json = get_banks_json(tokens_json['access'])
    save_json(banks_json, banks_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: 2.banks.py <tokens_file> <banks_file>")
        sys.exit(1)
    tokens_file = sys.argv[1]
    banks_file = sys.argv[2]
    main(tokens_file, banks_file)
