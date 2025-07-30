# filepath: c:\Python\gocardless\main_gui.py
#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, filedialog
from pathlib import Path
import logging
import step1_tokens
import step2_banks
import step3_agreement
import step4_link
import step5_accounts
import step6_transactions
import step7_excel
import threading
import sys

class TextRedirector:
    def __init__(self, log_func):
        self.log_func = log_func

    def write(self, s):
        if s.strip():
            self.log_func(s.rstrip())

    def flush(self):
        pass

class GoCardlessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GoCardless to Excel Automation")
        self.geometry("500x400")
        self.resizable(False, False)

        # Redirect stdout and stderr
        sys.stdout = TextRedirector(self.log)
        sys.stderr = TextRedirector(self.log)

        self.textbox = scrolledtext.ScrolledText(self, state='disabled', wrap='word', height=15, width=80)
        self.textbox.pack(padx=10, pady=10, fill='both', expand=True)

        self.frame = tk.Frame(self)
        self.frame.pack(pady=5)

        tk.Label(self.frame, text="Secret File:").grid(row=0, column=0, sticky='e')
        self.secret_entry = tk.Entry(self.frame, width=40)
        self.secret_entry.grid(row=0, column=1, padx=5)
        tk.Button(self.frame, text="Browse", command=self.browse_secret).grid(row=0, column=2)

        tk.Label(self.frame, text="Excel File:").grid(row=1, column=0, sticky='e')
        self.excel_entry = tk.Entry(self.frame, width=40)
        self.excel_entry.grid(row=1, column=1, padx=5)
        tk.Button(self.frame, text="Browse", command=self.browse_excel).grid(row=1, column=2)

        self.full_mode_var = tk.IntVar(value=1)
        tk.Checkbutton(self.frame, text="Full Mode (uncheck for Excel only)", variable=self.full_mode_var).grid(row=2, column=1, sticky='w')

        self.start_button = tk.Button(self, text="Start", command=self.start_process)
        self.start_button.pack(pady=5)

    def browse_secret(self):
        file = filedialog.askopenfilename(title="Select Secret File", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if file:
            self.secret_entry.delete(0, tk.END)
            self.secret_entry.insert(0, file)

    def browse_excel(self):
        file = filedialog.askopenfilename(title="Select Excel File", defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
        if file:
            self.excel_entry.delete(0, tk.END)
            self.excel_entry.insert(0, file)

    def log(self, message):
        self.textbox.config(state='normal')
        self.textbox.insert(tk.END, message + '\n')
        self.textbox.see(tk.END)
        self.textbox.config(state='disabled')
        self.update_idletasks()

    def ask_auth_code(self):
        # Schedule the dialog on the main thread and wait for the result
        self.auth_code = None
        def get_code():
            self.auth_code = simpledialog.askstring("Authorization Code", "Paste the authorization code from the URL:", parent=self)
            self.waiting_for_auth = False
        self.waiting_for_auth = True
        self.after(0, get_code)
        # Wait for the dialog to close
        while self.waiting_for_auth:
            self.update()
        return self.auth_code

    def start_process(self):
        self.start_button.config(state='disabled')
        threading.Thread(target=self.run_main, daemon=True).start()

    def run_main(self):
        secret_file = self.secret_entry.get()
        excel_file = self.excel_entry.get()
        full_mode = str(self.full_mode_var.get())

        if not secret_file or not excel_file:
            messagebox.showerror("Error", "Please select both Secret and Excel files.")
            self.start_button.config(state='normal')
            return

        folder = Path(secret_file).parent
        tokens_file = folder / 'tokens.json'
        banks_file = folder / 'banks.json'
        agreement_file = folder / 'agreement.json'
        link_file = folder / 'link.json'
        accounts_file = folder / 'accounts.json'
        transactions_file = folder / 'transactions.json'

        try:
            if full_mode == '1':
                if not self.get_tokens(secret_file, tokens_file): return
                if not self.get_banks(tokens_file, banks_file): return
                if not self.get_agreement(tokens_file, agreement_file): return
                if not self.get_link(tokens_file, agreement_file, link_file): return
                auth_code = self.ask_auth_code()
                if auth_code is None:
                    self.log("Authorization code entry cancelled.")
                    self.start_button.config(state='normal')
                    return
                if not self.get_accounts(tokens_file, accounts_file, auth_code): return
                if not self.get_transactions(tokens_file, accounts_file, transactions_file): return
            if not self.append(transactions_file, excel_file): return
            self.log('All finished!\n')
            messagebox.showinfo("Done", "All finished!")
        finally:
            self.start_button.config(state='normal')

    def get_tokens(self, secret_file, tokens_file):
        self.log('Fetching (access & refresh) tokens…')
        try:
            step1_tokens.main(secret_file, tokens_file)
            return True
        except Exception as e:
            self.log(f'Error fetching tokens: {e}')
            return False

    def get_banks(self, tokens_file, banks_file):
        self.log('Fetching banks list…')
        try:
            step2_banks.main(tokens_file, banks_file)
            return True
        except Exception as e:
            self.log(f'Error fetching banks list: {e}')
            return False

    def get_agreement(self, tokens_file, agreement_file):
        self.log('Fetching end user agreement…')
        try:
            step3_agreement.main(tokens_file, agreement_file)
            return True
        except Exception as e:
            self.log(f'Error fetching end user agreement: {e}')
            return False

    def get_link(self, tokens_file, agreement_file, link_file):
        self.log('Linking account…')
        try:
            step4_link.main(tokens_file, agreement_file, link_file)
            return True
        except Exception as e:
            self.log(f'Error linking account: {e}')
            return False

    def get_accounts(self, tokens_file, accounts_file, auth_code):
        self.log('Fetching accounts information…')
        try:
            step5_accounts.main(tokens_file, accounts_file, auth_code)
            return True
        except Exception as e:
            self.log(f'Error fetching accounts information: {e}')
            return False

    def get_transactions(self, tokens_file, accounts_file, transactions_file):
        self.log('Fetching transactions…')
        try:
            step6_transactions.main(tokens_file, accounts_file, transactions_file)
            return True
        except Exception as e:
            self.log(f'Error fetching transactions: {e}')
            return False

    def append(self, transactions_file, excel_file):
        self.log('Appending transactions to Excel file…')
        try:
            step7_excel.main(transactions_file, excel_file)
            return True
        except Exception as e:
            self.log(f'Error appending transactions to Excel file: {e}')
            return False

if __name__ == '__main__':
    app = GoCardlessGUI()
    app.mainloop()