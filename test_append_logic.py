# Run via python test_append_logic.py

import pandas as pd
from openpyxl import Workbook
import os
from step7_excel import append
import step7_excel

# Create dummy Excel file
excel_file = 'test_transactions.xlsx'
wb = Workbook()
ws = wb.active
ws.title = 'Compte'
ws.append(['Transaction ID', 'Mois', 'Date V/R']) # Header
ws.append(['A', 'Jan', '2023-01-01'])
ws.append(['B', 'Jan', '2023-01-02'])
wb.save(excel_file)

# Create DataFrame with mixed new and old transactions
data = {
    'Transaction ID': ['A', 'C', 'B', 'D'],
    'Date V/R': ['2023-01-01', '2023-01-03', '2023-01-02', '2023-01-04'],
    'Débiteur': ['Deb A', 'Deb C', 'Deb B', 'Deb D'],
    'Compte D': ['1', '3', '2', '4'],
    'Créditeur': ['Cred A', 'Cred C', 'Cred B', 'Cred D'],
    'Compte C': ['1', '3', '2', '4'],
    'Quoi': ['Info A', 'Info C', 'Info B', 'Info D'],
    'Communication': ['Comm A', 'Comm C', 'Comm B', 'Comm D'],
    'Montant': [10.0, 30.0, 20.0, 40.0],
    'Sommaire': ['Somm A', 'Somm C', 'Somm B', 'Somm D']
}
df = pd.DataFrame(data)

# Run append
print("Running append...")
append(excel_file, 'Compte', df)

# Check results
wb = pd.read_excel(excel_file, sheet_name='Compte')
print("\nResulting Excel IDs:")
print(wb['Transaction ID'].tolist())

expected_ids = ['A', 'B', 'C', 'D']
actual_ids = wb['Transaction ID'].tolist()

if set(actual_ids) == set(expected_ids) and len(actual_ids) == 4:
    print("\nSUCCESS: All transactions present and no duplicates.")
else:
    print("\nFAILURE: IDs do not match expectations.")

# Clean up
try:
    os.remove(excel_file)
except:
    pass
