#!/usr/bin/env python3

from pathlib import Path
import step1_tokens
import step2_banks
import step3_agreement
import step4_link
import step4_requisition
import step5_accounts
import step6_transactions
import step7_excel
import sys

def get_tokens(secret_file, tokens_file):
    print('Fetching (access & refresh) tokens…')
    try: step1_tokens.main(secret_file, tokens_file)
    except Exception as e:
        print(f'Error fetching tokens: {e}')
        sys.exit(1)

def get_banks(tokens_file, banks_file): 
    print('Fetching banks list…')
    try: step2_banks.main(tokens_file, banks_file)
    except Exception as e:
        print(f'Error fetching banks list: {e}')
        sys.exit(2)

def get_agreement(tokens_file, agreement_file):
    print('Fetching end user agreement…')
    try: step3_agreement.main(tokens_file, agreement_file)
    except Exception as e:
        print(f'Error fetching end user agreement: {e}')
        sys.exit(3)

def get_link(tokens_file, agreement_file, port, link_file):
    print('Linking account…')
    try: step4_link.main(tokens_file, agreement_file, port, link_file)
    except Exception as e:
        print(f'Error linking account: {e}')
        sys.exit(4)
def get_requisition(port, requisition_file):
    print('Starting local server to receive the "ref" code…')
    try:
        step4_requisition.main(port, requisition_file)
        print('Local server started. Please complete the authentication in your browser.')
    except Exception as e:
        print(f'Error starting local server: {e}')
        sys.exit(4)

def get_accounts(tokens_file, accounts_file, requisition_file):
    print('Fetching accounts information…')
    try: step5_accounts.main(tokens_file, accounts_file, requisition_file)
    except Exception as e:
        print(f'Error fetching accounts information: {e}')
        sys.exit(5)

def get_transactions(tokens_file, accounts_file, transactions_file):
    print('Fetching transactions…')
    try:
        step6_transactions.main(tokens_file, accounts_file, transactions_file)
    except Exception as e:
        print(f'Error fetching transactions: {e}')
        sys.exit(6)

def append(transactions_file, excel_file, sheet_name):
    print('Appending transactions to Excel file…')
    try:
        step7_excel.main(transactions_file, excel_file, sheet_name)
    except Exception as e:
        print(f'Error appending transactions to Excel file: {e}')
        sys.exit(7)

def main():
    if full_mode == '1':
        get_tokens(secret_file, tokens_file)
        get_banks(tokens_file, banks_file)
        get_agreement(tokens_file, agreement_file)
        get_link(tokens_file, agreement_file, port, link_file)
        # requisition_id = input('Paste the "ref" code from the URL: ')
        # return requisition_id.strip()
        get_requisition(port, requisition_file)
        get_accounts(tokens_file, accounts_file, requisition_file)
        get_transactions(tokens_file, accounts_file, transactions_file)
        pass
    append(transactions_file, excel_file, 'Compte')
    print('All finished!\n')

if __name__ == '__main__':
    if len(sys.argv) != 4 or sys.argv[3] not in ['0', '1']:
        # Eg io/gau.json 'C:\Python\gocardless\io\2025. Comptes.xlsx' 1
        print('Usage: main.py <secret_file> <excel_file> <full_mode> (0: excel only, 1: full mode)')
        sys.exit(0)

    secret_file = sys.argv[1]    
    folder =  Path(secret_file).parent
    tokens_file = folder / 'tokens.json'
    banks_file = folder / 'banks.json'
    agreement_file = folder / 'agreement.json'
    port = 8080
    link_file = folder / 'link.json'
    requisition_file = folder / 'requisition.json'
    accounts_file = folder / 'accounts.json'
    transactions_file = folder / 'transactions.json'
    excel_file = sys.argv[2]
    full_mode = sys.argv[3]

    # main(secret_file, tokens_file, banks_file, agreement_file, link_file, accounts_file, transactions_file, excel_file)
    main()
