import json
from datetime import datetime

class Expense:
    def __init__(self, amount, category,date, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.budgets = {}

    def add_expense(self, amount, category, description):
        #total_spent = self.total_expenses_by_category(category)
        #amount = amount + total_spent
        #if category in self.budgets:
        #    budget = self.budgets[category]
        #remainingamount =budget-total_spent
        #if amount > budget:
        #   print(f"You have remaining budget for {category} category only {remainingamount}, so cannot add!")
        #else:
        date=datetime.now().strftime('%Y-%m-%d')
        expense = Expense(amount, category,date,description)
        self.expenses.append(expense)
        print(f"Added expense: {amount} in {category} for '{description}'")
    def set_budget(self, category, amount):
        self.budgets[category] = amount
        print(f"Set budget for {category}: {amount}")

    def view_expenses(self, category=None):
        if category:
            filtered_expenses = [exp for exp in self.expenses if exp.category == category]
            print(f"Expenses in category '{category}':")
            for exp in filtered_expenses:
                print(f"- {exp.amount} on {exp.date} for {exp.description}")
        else:
            print("All expenses:")
            for exp in self.expenses:
                print(f"- {exp.amount} in {exp.category} on {exp.date} for {exp.description}")

    def total_expenses_by_category(self, category):
        return sum(exp.amount for exp in self.expenses if exp.category == category)

    def check_budget(self, category):
        total_spent = self.total_expenses_by_category(category)
        if category in self.budgets:
            budget = self.budgets[category]
            print(f"Total spent in {category}: {total_spent}, Budget: {budget}")
            if total_spent > budget:
                print(f"WARNING: You have exceeded the budget for {category}!")
        else:
            print(f"No budget set for {category}")

    def save_to_file(self, filename='expenses.json'):
        data = {
            'expenses': [vars(exp) for exp in self.expenses],
            'budgets': self.budgets
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print(f"Expenses saved to {filename}")

    def load_from_file(self, filename='expenses.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.expenses = [Expense(**exp) for exp in data['expenses']]
                self.budgets = data['budgets']
            print(f"Expenses loaded from {filename}")
        except FileNotFoundError:
            print(f"No data file found. Starting fresh.")


def main_menu():
    tracker = ExpenseTracker()
    tracker.load_from_file()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Set Budget")
        print("4. Check Budget")
        print("5. Save and Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, category, description)
        elif choice == '2':
            category = input("Enter category to filter by (leave empty for all): ")
            tracker.view_expenses(category if category else None)
        elif choice == '3':
            category = input("Enter category: ")
            amount = float(input(f"Enter budget for {category}: "))
            tracker.set_budget(category, amount)
        elif choice == '4':
            category = input("Enter category: ")
            tracker.check_budget(category)
        elif choice == '5':
            tracker.save_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()