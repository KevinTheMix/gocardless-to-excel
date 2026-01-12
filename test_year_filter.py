
import pandas as pd
from openpyxl import Workbook
import os
from step7_excel import append
import step7_excel

# Create dummy Excel file with a year in the name
excel_file = 'transactions_2023.xlsx'
wb = Workbook()
ws = wb.active
ws.title = 'Compte'
ws.append(['Transaction ID', 'Mois', 'Date V/R']) # Header
wb.save(excel_file)

# Create DataFrame with mixed years
data = {
    'Transaction ID': ['A', 'B', 'C'],
    'Date V/R': ['2022-12-31', '2023-01-01', '2024-01-01'],
    'Débiteur': ['Deb A', 'Deb B', 'Deb C'],
    'Compte D': ['1', '2', '3'],
    'Créditeur': ['Cred A', 'Cred B', 'Cred C'],
    'Compte C': ['1', '2', '3'],
    'Quoi': ['Info A', 'Info B', 'Info C'],
    'Communication': ['Comm A', 'Comm B', 'Comm C'],
    'Montant': [10.0, 20.0, 30.0],
    'Sommaire': ['Somm A', 'Somm B', 'Somm C']
}
df = pd.DataFrame(data)
df['Date V/R'] = pd.to_datetime(df['Date V/R']) # Ensure datetime objects

# Run append
print(f"Running append on {excel_file}...")
append(excel_file, 'Compte', df)

# Check results
wb = pd.read_excel(excel_file, sheet_name='Compte')
print("\nResulting Excel IDs:")
print(wb['Transaction ID'].tolist())

expected_ids = ['B'] # Only 2023 transaction
actual_ids = wb['Transaction ID'].tolist()

if set(actual_ids) == set(expected_ids) and len(actual_ids) == 1:
    print("\nSUCCESS: Only 2023 transaction appended.")
else:
    print("\nFAILURE: Incorrect transactions appended.")

# Clean up
try:
    os.remove(excel_file)
except:
    pass
