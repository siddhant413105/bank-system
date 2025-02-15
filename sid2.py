import tkinter as tk
from tkinter import messagebox

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(f"Deposited {amount}. New balance is {self.balance}.")
            print(f"Deposited {amount}. New balance is {self.balance}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
            self.history.append(f"Withdrew {amount}. New balance is {self.balance}.")
            print(f"Withdrew {amount}. New balance is {self.balance}.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.history

class Transaction:
    def __init__(self, transaction_id, from_account, to_account, amount):
        self.transaction_id = transaction_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def execute(self):
        try:
            self.from_account.withdraw(self.amount)
            self.to_account.deposit(self.amount)
            self.from_account.history.append(f"Transferred {self.amount} to {self.to_account.account_number}.")
            self.to_account.history.append(f"Received {self.amount} from {self.from_account.account_number}.")
            print(f"Transaction {self.transaction_id} executed successfully.")
        except InsufficientFundsError as e:
            print(f"Transaction {self.transaction_id} failed: {e}")

class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set the geometry to full screen
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.accounts = {}

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the Bank Management System", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self.root, text="Continue", command=self.show_services, bg="lightblue", font=("Helvetica", 16)).pack(pady=20)

    def show_services(self):
        self.clear_screen()
        self.create_tabs()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_tabs(self):
        self.tab_frame = tk.Frame(self.root)
        self.tab_frame.pack(side=tk.TOP, fill=tk.X, pady=20)

        tab_container = tk.Frame(self.tab_frame)
        tab_container.pack(expand=True)

        tk.Button(tab_container, text="Create Account", command=self.show_create_account, bg="lightblue").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(tab_container, text="Transaction", command=self.show_transaction, bg="lightgreen").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(tab_container, text="Account Operations", command=self.show_account_operations, bg="lightyellow").pack(side=tk.LEFT, padx=5, pady=5)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def show_create_account(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Account Number").grid(row=0, column=0)
        tk.Label(self.content_frame, text="Account Holder").grid(row=1, column=0)
        tk.Label(self.content_frame, text="Initial Balance").grid(row=2, column=0)

        self.account_number_entry = tk.Entry(self.content_frame)
        self.account_holder_entry = tk.Entry(self.content_frame)
        self.initial_balance_entry = tk.Entry(self.content_frame)

        self.account_number_entry.grid(row=0, column=1)
        self.account_holder_entry.grid(row=1, column=1)
        self.initial_balance_entry.grid(row=2, column=1)

        tk.Button(self.content_frame, text="Create Account", command=self.create_account, bg="lightblue").grid(row=3, column=0, columnspan=2)

    def show_transaction(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="From Account").grid(row=0, column=0)
        tk.Label(self.content_frame, text="To Account").grid(row=1, column=0)
        tk.Label(self.content_frame, text="Amount").grid(row=2, column=0)

        self.from_account_entry = tk.Entry(self.content_frame)
        self.to_account_entry = tk.Entry(self.content_frame)
        self.amount_entry = tk.Entry(self.content_frame)

        self.from_account_entry.grid(row=0, column=1)
        self.to_account_entry.grid(row=1, column=1)
        self.amount_entry.grid(row=2, column=1)

        tk.Button(self.content_frame, text="Execute Transaction", command=self.execute_transaction, bg="lightgreen").grid(row=3, column=0, columnspan=2)

    def show_account_operations(self):
        self.clear_content_frame()
        tk.Label(self.content_frame, text="Account Number").grid(row=0, column=0)
        tk.Label(self.content_frame, text="Amount").grid(row=1, column=0)

        self.operation_account_entry = tk.Entry(self.content_frame)
        self.operation_amount_entry = tk.Entry(self.content_frame)

        self.operation_account_entry.grid(row=0, column=1)
        self.operation_amount_entry.grid(row=1, column=1)

        tk.Button(self.content_frame, text="Deposit", command=self.deposit, bg="lightyellow").grid(row=2, column=0)
        tk.Button(self.content_frame, text="Withdraw", command=self.withdraw, bg="lightcoral").grid(row=2, column=1)
        tk.Button(self.content_frame, text="View History", command=self.view_history, bg="lightgray").grid(row=3, column=0, columnspan=2)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_account(self):
        account_number = self.account_number_entry.get()
        account_holder = self.account_holder_entry.get()
        initial_balance = float(self.initial_balance_entry.get())

        if account_number and account_holder:
            self.accounts[account_number] = Account(account_number, account_holder, initial_balance)
            messagebox.showinfo("Success", f"Account {account_number} created for {account_holder} with balance {initial_balance}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def execute_transaction(self):
        from_account_number = self.from_account_entry.get()
        to_account_number = self.to_account_entry.get()
        amount = float(self.amount_entry.get())

        if from_account_number in self.accounts and to_account_number in self.accounts:
            from_account = self.accounts[from_account_number]
            to_account = self.accounts[to_account_number]

            transaction = Transaction("T001", from_account, to_account, amount)
            transaction.execute()

            messagebox.showinfo("Success", f"Transaction executed. New balance of {from_account_number}: {from_account.get_balance()}, {to_account_number}: {to_account.get_balance()}")
        else:
            messagebox.showerror("Error", "Invalid account number(s)")

    def deposit(self):
        account_number = self.operation_account_entry.get()
        amount = float(self.operation_amount_entry.get())

        if account_number in self.accounts:
            account = self.accounts[account_number]
            account.deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount}. New balance is {account.get_balance()}")
        else:
            messagebox.showerror("Error", "Invalid account number")

    def withdraw(self):
        account_number = self.operation_account_entry.get()
        amount = float(self.operation_amount_entry.get())

        if account_number in self.accounts:
            account = self.accounts[account_number]
            try:
                account.withdraw(amount)
                messagebox.showinfo("Success", f"Withdrew {amount}. New balance is {account.get_balance()}")
            except InsufficientFundsError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid account number")

    def view_history(self):
        account_number = self.operation_account_entry.get()

        if account_number in self.accounts:
            account = self.accounts[account_number]
            history = account.get_history()
            history_str = "\n".join(history)
            messagebox.showinfo("Account History", history_str)
        else:
            messagebox.showerror("Error", "Invalid account number")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()