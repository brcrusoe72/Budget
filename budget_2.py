import json
from datetime import datetime, timedelta

class Transaction:
    def __init__(self, type, amount, description, date, term):
        self.type = type.capitalize()
        self.amount = round(float(amount), 2)
        self.description = description.capitalize()
        self.date = date
        self.term = term.capitalize()

    def __str__(self):
        return f"{self.date}: {self.type}: {self.amount:.2f} - {self.description} ({self.term})"

    @staticmethod
    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class TransactionManager:
    def __init__(self):
        self.short_term_transactions = []
        self.long_term_transactions = []

    def add_transaction(self, transaction):
        if transaction.term == 'Short-term':
            self.short_term_transactions.append(transaction)
        else:  # Long-term
            self.long_term_transactions.append(transaction)

    def edit_transactions(self, description, term):
        term = term.lower()
        transactions = self.short_term_transactions if term == 'short-term' else self.long_term_transactions
        matched_transactions = [t for t in transactions if t.description.lower() == description.lower()]

        for transaction in matched_transactions:
            print(f"Editing Transaction: {transaction}")
            new_type = input(f"Enter new type (Income/Expense) [{transaction.type}]: ") or transaction.type
            new_amount = get_valid_amount()  # Utilize the existing function for amount validation
            new_description = input(f"Enter new description [{transaction.description}]: ") or transaction.description
            new_date = get_valid_date(f"Enter new date (YYYY-MM-DD) [{transaction.date}]: ") or transaction.date

            transaction.type = new_type.capitalize()
            transaction.amount = round(float(new_amount), 2)
            transaction.description = new_description.capitalize()
            transaction.date = new_date
        
        self.save_transactions()  # Save the updated transactions

    def list_transactions_by_term(self, term):
        term = term.lower()
        transactions = self.short_term_transactions if term == 'short-term' else self.long_term_transactions
        for transaction in transactions:
            print(transaction)

    def calculate_summary(self, term_transactions):
        income = sum(t.amount for t in term_transactions if t.type == 'Income')
        expense = sum(t.amount for t in term_transactions if t.type == 'Expense')
        balance = income - expense
        return income, expense, balance

    def show_summary(self, term_transactions):
        income, expense, balance = self.calculate_summary(term_transactions)
        print(f"Total Income: {income:.2f}, Total Expense: {expense:.2f}, Balance: {balance:.2f}")

    def show_visual_summary(self, term_transactions):
        income, expense, _ = self.calculate_summary(term_transactions)
        max_amount = max(income, expense, 1)
        income_bar = '|' * int((income / max_amount) * 50)
        expense_bar = '|' * int((expense / max_amount) * 50)
        print(f"Visual Summary:\nIncome  : {income_bar} ({income})\nExpense : {expense_bar} ({expense})")

    def save_transactions(self):
        with open('short_term_transactions.json', 'w') as f:
            json.dump([t.__dict__ for t in self.short_term_transactions], f)
        with open('long_term_transactions.json', 'w') as f:
            json.dump([t.__dict__ for t in self.long_term_transactions], f)

    def load_transactions(self):
        try:
            with open('short_term_transactions.json', 'r') as f:
                self.short_term_transactions = [Transaction(**t) for t in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Short-term transactions file not found or is empty.")

        try:
            with open('long_term_transactions.json', 'r') as f:
                self.long_term_transactions = [Transaction(**t) for t in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Long-term transactions file not found or is empty.")

def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        if Transaction.is_valid_date(date_input):
            return date_input
        else:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            return round(amount, 2)
        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")

def get_transaction_details():
    type = input("Enter type (Income/Expense): ")
    amount = get_valid_amount()
    description = input("Enter description: ")
    date = get_valid_date("Enter date (YYYY-MM-DD): ")
    term = input("Enter term (short-term/long-term): ")
    return type, amount, description, date, term

def main():
    manager = TransactionManager()
    manager.load_transactions()

    while True:
        print("\n1: Add Income/Expense 2: Add Recurring Transaction 3: List Transactions 4: Summary 5: Visual Summary 6: Edit Transaction 7: Exit")
        choice = input("Choose an action: ")

        if choice == '1':
            type, amount, description, date, term = get_transaction_details()
            transaction = Transaction(type, amount, description, date, term)
            manager.add_transaction(transaction)
            manager.save_transactions()

        elif choice == '2':
            type, amount, description, start_date, term = get_transaction_details()
            frequency = input("Enter frequency (weekly/monthly): ")
            end_date = get_valid_date("Enter end date (YYYY-MM-DD): ")

            current_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

            while current_date <= end_date_obj:
                transaction = Transaction(type, amount, description, current_date.strftime('%Y-%m-%d'), term)
                manager.add_transaction(transaction)
                if frequency == 'monthly':
                    current_date += timedelta(days=30)  # Approximation for monthly
                elif frequency == 'weekly':
                    current_date += timedelta(weeks=1)
            manager.save_transactions()
           

        elif choice == '3':
            term = input("Enter term to list (short-term/long-term): ")
            manager.list_transactions_by_term(term)

        elif choice in ['4', '5']:
            term = input("Choose the type of summary (short-term/long-term): ")
            term_transactions = manager.short_term_transactions if term.lower() == 'short-term' else manager.long_term_transactions
            manager.show_summary(term_transactions)
            if choice == '5':
                manager.show_visual_summary(term_transactions)

        elif choice == '6':
            # Logic for editing transactions
            description = input("Enter the description of the transaction to edit: ")
            term = input("Enter the term (short-term/long-term): ")
            manager.edit_transactions(description, term)

        elif choice == '7':
            break

    print("Exiting the application.")

# Additional function definitions, such as get_transaction_details, needed here


if __name__ == "__main__":
    main()