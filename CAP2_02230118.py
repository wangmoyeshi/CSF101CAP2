import random
import string
import os

class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                print(f"Withdrew ${amount}. New balance: ${self.balance}")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def check_balance(self):
        print(f"Current balance: ${self.balance}")

    def to_string(self):
        return f"{self.account_number},{self.password},{self.account_type},{self.balance}"
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, 'Business', balance)
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, 'Personal', balance)
class FileHandler:
    def __init__(self, filename='accounts.txt'):
        self.filename = filename

    def load_accounts(self):
        accounts = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(',')
                    balance = float(balance)
                    if account_type == 'Business':
                        accounts[account_number] = BusinessAccount(account_number, password, balance)
                    elif account_type == 'Personal':
                        accounts[account_number] = PersonalAccount(account_number, password, balance)
        return accounts

    def save_accounts(self, accounts):
        with open(self.filename, 'w') as file:
            for account in accounts.values():
                file.write(account.to_string() + '\n')
class Bank:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.accounts = self.file_handler.load_accounts()

    def create_account(self, account_type):
        account_number = self.generate_account_number()
        password = self.generate_password()
        if account_type == 'Business':
            account = BusinessAccount(account_number, password)
        elif account_type == 'Personal':
            account = PersonalAccount(account_number, password)
        else:
            print("Invalid account type.")
            return
        self.accounts[account_number] = account
        self.file_handler.save_accounts(self.accounts)
        print(f"Account created. Account Number: {account_number}, Password: {password}")

    def generate_account_number(self):
        return ''.join(random.choices(string.digits, k=10))

    def generate_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def login(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.password == password:
            print("Login successful.")
            return account
        else:
            print("Invalid account number or password.")
            return None

    def delete_account(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.password == password:
            del self.accounts[account_number]
            self.file_handler.save_accounts(self.accounts)
            print("Account deleted successfully.")
        else:
            print("Invalid account number or password.")

    def transfer_money(self, from_account_number, to_account_number, amount):
        from_account = self.accounts.get(from_account_number)
        to_account = self.accounts.get(to_account_number)
        if from_account and to_account:
            if from_account.balance >= amount:
                from_account.withdraw(amount)
                to_account.deposit(amount)
                self.file_handler.save_accounts(self.accounts)
                print(f"Transferred ${amount} from {from_account_number} to {to_account_number}")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid account number(s).")
def main():
    file_handler = FileHandler()
    bank = Bank(file_handler)
    
    while True:
        print("\nBanking System")
        print("1. Open Account")
        print("2. Login")
        print("3. Delete Account")
        print("4. Transfer Money")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            account_type = input("Enter account type (Business/Personal): ")
            bank.create_account(account_type)
        elif choice == '2':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.login(account_number, password)
            if account:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == '1':
                        account.check_balance()
                    elif sub_choice == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        bank.file_handler.save_accounts(bank.accounts)
                    elif sub_choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        bank.file_handler.save_accounts(bank.accounts)
                    elif sub_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            bank.delete_account(account_number, password)
        elif choice == '4':
            from_account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            from_account = bank.login(from_account_number, password)
            if from_account:
                to_account_number = input("Enter recipient's account number: ")
                amount = float(input("Enter amount to transfer: "))
                bank.transfer_money(from_account_number, to_account_number, amount)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
