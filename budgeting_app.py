from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type, date=None):
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.strptime(date, '%Y-%m-%d') if date else datetime.now()

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of ${self.amount:.2f} on {self.date.strftime('%Y-%m-%d')}"

class Budget:
    def __init__(self):
        self.transactions = []
        self.savings = 0
        self.savings_interest_rate = 0.05  # Default interest rate of 5%

    def add_transaction(self, amount, transaction_type, date=None):
        transaction = Transaction(amount, transaction_type, date)
        self.transactions.append(transaction)
        if transaction_type == 'salary':
            self.savings += amount  # Adds salary to savings

    def calculate_balance(self):
        balance = sum(t.amount if t.transaction_type == 'salary' else -t.amount for t in self.transactions)
        return balance

    def add_to_savings(self, amount):
        self.savings += amount

    def calculate_savings_interest(self, months):
        return self.savings * ((1 + self.savings_interest_rate) ** months - 1)

    def project_future_savings(self, monthly_contribution, months):
        future_savings = self.savings
        for month in range(months):
            future_savings = future_savings * (1 + self.savings_interest_rate) + monthly_contribution
        return future_savings

    def __str__(self):
        transactions_str = '\n'.join(str(transaction) for transaction in self.transactions)
        return f"Transactions:\n{transactions_str}\nCurrent Balance: ${self.calculate_balance():.2f}\nSavings: ${self.savings:.2f}"

def main():
    budget = Budget()
    while True:
        action = input("Choose action (Salary 's', Bill 'b', Transaction 't', Add to Savings 'a', Project Savings 'p', Exit 'e'): ").lower()
        if action == 'e':
            break

        if action in ['s', 'b', 't']:
            amount = float(input("Enter amount: "))
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            budget.add_transaction(amount, action, date_input)

        elif action == 'a':
            amount = float(input("Enter amount to add to savings: "))
            budget.add_to_savings(amount)

        elif action == 'p':
            months = int(input("Enter number of months for projection: "))
            monthly_contribution = float(input("Enter monthly contribution to savings: "))
            projected_savings = budget.project_future_savings(monthly_contribution, months)
            print(f"Projected savings after {months} months: ${projected_savings:.2f}")

        print(budget)

if __name__ == "__main__":
    main()