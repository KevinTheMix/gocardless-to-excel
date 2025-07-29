#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

def get_tokens(secret_file, tokens_file):
    print('Fetching (access & refresh) tokens…')
    if subprocess.run(['python3', '1.tokens.py', secret_file, tokens_file]).returncode != 0:
       print('Fetching tokens failed!\n')
       exit(1)

def get_banks(tokens_file, banks_file): 
    print('Fetching banks list…')
    if subprocess.run(['python3', '2.banks.py', tokens_file, banks_file]).returncode != 0:
        print('Fetching banks list failed!\n')
        exit(2)

def get_agreement(tokens_file, agreement_file):
    print('Fetching end user agreement…')
    if subprocess.run(['python3', '3.agreement.py', tokens_file, agreement_file]).returncode != 0:
        print('Fetching end user agreement failed!\n')
        exit(3)

def get_link(tokens_file, agreement_file, link_file):
    print('Linking account…')
    if subprocess.run(['python3', '4.link.py', tokens_file, agreement_file, link_file]).returncode != 0:
        print('Linking account failed!\n')
        exit(4)
    return input('Paste the authorization code from the URL: ')

def get_accounts(tokens_file, accounts_file, auth_code):
    print('Fetching accounts information…')
    if subprocess.run(['python3', '5.accounts.py', tokens_file, accounts_file, auth_code]).returncode != 0:
        print('Fetching accounts information failed!\n')
        exit(5)

def get_transactions(tokens_file, accounts_file, transactions_file):
    print('Fetching transactions…')
    if subprocess.run(['python3', '6.transactions.py', tokens_file, accounts_file, transactions_file]).returncode != 0:
        print('Fetching transactions failed!\n')
        exit(6)

def append(transactions_file, excel_file):
    print('Appending transactions to Excel file…')
    if subprocess.run(['python3', 'excel.py', transactions_file, excel_file]).returncode != 0:
        print('Appending transactions to Excel file failed!\n')
        exit(7)

def main(secret_file, tokens_file, banks_file, agreement_file, link_file, accounts_file, transactions_file, excel_file):
    get_tokens(secret_file, tokens_file)
    get_banks(tokens_file, banks_file)
    get_agreement(tokens_file, agreement_file)
    auth_code = get_link(tokens_file, agreement_file, link_file)
    get_accounts(tokens_file, accounts_file, auth_code)
    get_transactions(tokens_file, accounts_file, transactions_file)
    append(transactions_file, excel_file)
    print('All finished!\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: main.py <secret_file> <excel_file>')
        sys.exit(0)

    secret_file = sys.argv[1]
    folder =  Path(secret_file).parent
    tokens_file = folder / 'tokens.json'
    banks_file = folder / 'banks.json'
    agreement_file = folder / 'agreement.json'
    link_file = folder / 'link.json'
    accounts_file = folder / 'io/accounts.json'
    transactions_file = folder / 'io/transactions.json'
    excel_file = sys.argv[2]

    main(secret_file, tokens_file, banks_file, agreement_file, link_file, accounts_file, transactions_file, excel_file)

