#!/usr/bin/env python3

import requests
import subprocess
import sys
from lib.json_io import load_json, save_json

def get_link(access_token, port, agreement_id):
    url = 'https://bankaccountdata.gocardless.com/api/v2/requisitions/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    link_json = {
        'redirect': f'http://localhost:{port}',
        'institution_id': 'BELFIUS_GKCCBEBB',
        'agreement': agreement_id
    }
    
    response = requests.post(url, headers=headers, json=link_json)
    return response.json()

def open_link(url):
    # Lets explorer run the link (browser will open it)
    print('Opening browser for bank authentication')
    subprocess.run(['explorer.exe', url])

def main(tokens_file, agreement_file, port, link_file):
    access_token = load_json(tokens_file).get('access')
    agreement_id = load_json(agreement_file).get('id')
    link_json = get_link(access_token, port, agreement_id)
    save_json(link_json, link_file)
    open_link(link_json['link'])

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: 4.link.py <tokens_file> <agreement_file> <port> <link_file>')
        sys.exit(1)

    tokens_file = sys.argv[1]
    agreement_file = sys.argv[2]
    port = sys.argv[3]
    link_file = sys.argv[4]
    main(tokens_file, agreement_file, port, link_file)
