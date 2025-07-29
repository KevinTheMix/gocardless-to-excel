#!/usr/bin/env python3

import requests
import sys
from lib.json_io import load_json, save_json

def get_agreement(access_token):
    url = 'https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    agreement_json = {
        'institution_id': 'BELFIUS_GKCCBEBB',
        'max_historical_days': '6666660', # How many 'bookingDate' days far back (max 90)
        'access_valid_for_days': '30',
        'access_scope': ['transactions']
    }

    response = requests.post(url, headers=headers, json=agreement_json)
    return response.json()

def main(tokens_file, agreement_file):
    tokens_json = load_json(tokens_file)
    agreement_json = get_agreement(tokens_json['access'])
    save_json(agreement_json, agreement_file)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: 3.agreement.py <tokens_file> <agreement_file>')
        sys.exit(1)

    tokens_file = sys.argv[1]
    agreement_file = sys.argv[2]
    main(tokens_file, agreement_file)
