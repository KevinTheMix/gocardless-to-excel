#!/usr/bin/env python3

import os
import requests
import sys
from lib.json_io import load_json, save_json
from datetime import datetime, timedelta

def get_file_creation_time(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def is_token_valid(created_at, expires_in):
    return datetime.now() < created_at + timedelta(seconds=expires_in)

def post(url, json):
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'} 
    response = requests.post(url, headers=headers, json=json)
    response.raise_for_status()
    return response.json()
def get_tokens(secret_json):
    return post('https://bankaccountdata.gocardless.com/api/v2/token/new/', secret_json)
def get_access_token(refresh_token):
    return post('https://bankaccountdata.gocardless.com/api/v2/token/refresh/', { 'refresh': refresh_token })

def main(secret_file, tokens_file):
    if os.path.exists(tokens_file):
        tokens_json = load_json(tokens_file)
        file_time = get_file_creation_time(tokens_file)

        if is_token_valid(file_time, tokens_json['access_expires']):
            print("Access token is still valid. Skipping API call.")
            return

        elif is_token_valid(file_time, tokens_json['refresh_expires']):
            print("Access token is expired. Refreshing now~")
            try:
                at = get_access_token(tokens_json['refresh'])
                tokens_json['access'] = at['access']
                tokens_json['access_expires'] = at['access_expires']
                save_json(tokens_json, tokens_file)
                return
            except requests.HTTPError as e:
                print(f"Failed to refresh token: {e}")
    
    print("Fetching new access token...")
    secret_json = load_json(secret_file)
    tokens_json = get_tokens(secret_json)
    save_json(tokens_json, tokens_file)

# Runs this code only if the script is executed directly (not imported)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tokens.py <secret_file> <tokens_file>")
        sys.exit(1)

    secret_file = sys.argv[1]
    tokens_file = sys.argv[2]
    main(secret_file, tokens_file)
