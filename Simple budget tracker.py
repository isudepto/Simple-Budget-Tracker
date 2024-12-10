import os
from datetime import datetime

def load_budget():
    if not os.path.exists("budget_data.txt"):
        default_data = {"income": 0, "expenses": [], "handed_amount": 0}
        save_budget(default_data)
        return default_data
    else:
        return read_from_file()

def save_budget(data):
    with open("budget_data.txt", "w") as file:
        file.write(f"Income: {data['income']}\n")
        file.write(f"Handed Amount: {data['handed_amount']}\n")
        file.write("Expenses:\n")
        for expense in data["expenses"]:
            file.write(f"{expense['category']},{expense['amount']},{expense['date']},{expense['time']}\n")

def read_from_file():
    data = {"income": 0, "expenses": [], "handed_amount": 0}
    with open("budget_data.txt", "r") as file:
        lines = file.readlines()
        data['income'] = float(lines[0].strip().split(": ")[1])
        data['handed_amount'] = float(lines[1].strip().split(": ")[1])
        for line in lines[3:]:
            category, amount, date, time = line.strip().split(",")
            data["expenses"].append({
                "category": category,
                "amount": float(amount),
                "date": date,
                "time": time
            })
    return data

def get_current_datetime():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d"), current_datetime.strftime("%H:%M:%S")

def add_expense(data):
    print("\n========== ADD EXPENSE ==========")
    total_expenses = sum(expense["amount"] for expense in data["expenses"])
    if total_expenses >= data["income"]:
        print(f"Warning: Current expenses ({total_expenses:.2f}) exceed or match your income ({data['income']:.2f}). Cannot add more expenses.")
        return
    category = input("Enter the category of the expense: ").strip()
    try:
        amount = float(input("Enter the amount: ").strip())
        if amount < 0:
            print("Amount cannot be negative. Try again.\n")
            return
        if total_expenses + amount > data["income"]:
            print(f"Error: Adding this expense would exceed your income.")
            return
        expense_date, expense_time = get_current_datetime()
        data["expenses"].append({
            "category": category,
            "amount": amount,
            "date": expense_date,
            "time": expense_time
        })
        data["handed_amount"] += amount
        print(f"Added Expense: {category}, {amount:.2f} on {expense_date} at {expense_time}")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def add_income(data):
    print("\n========== ADD INCOME ==========")
    try:
        income = float(input("Enter the amount of income: ").strip())
        if income < 0:
            print("Income cannot be negative. Try again.\n")
            return
        data["income"] += income
        income_date, income_time = get_current_datetime()
        update_handed = input("Was this income handed to you directly? (yes/no): ").strip().lower()
        if update_handed == "yes":
            data["handed_amount"] += income
        print(f"Added Income: {income:.2f} on {income_date} at {income_time}")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def view_budget(data):
    print("\n" + "=" * 40)
    print("           BUDGET OVERVIEW")
    print("=" * 40)
    total_expenses = sum(expense["amount"] for expense in data["expenses"])
    net_remaining = data["income"] - total_expenses

    print(f"{'Total Income:':<25} {data['income']:<15.2f}")
    print(f"{'Total Expenses:':<25} {total_expenses:<15.2f}")
    print(f"{'Net Remaining Budget:':<25} {net_remaining:<15.2f}")
    print(f"{'Handed Amount:':<25} {data['handed_amount']:<15.2f}")
    print()

    print("=" * 40)
    print("               STATEMENT")
    print("=" * 40)
    print(f"{'Category':<20}{'Amount':<15}{'Type':<15}{'Date':<15}{'Time':<15}{'Remaining Balance':<15}")
    print("-" * 95)

    print(f"{'Income':<20}{data['income']:<15.2f}{'Income':<15}{'---':<15}{'---':<15}{data['income']:<15.2f}")
    
    running_balance = data["income"]
    for expense in data["expenses"]:
        running_balance -= expense["amount"]
        print(f"{expense['category']:<20}{expense['amount']:<15.2f}{'Expense':<15}{expense['date']:<15}{expense['time']:<15}{running_balance:<15.2f}")
    
    print("-" * 95)
    print(f"{'Total Expenses:':<20}{total_expenses:<15.2f}{'---':<15}{'---':<15}{'---':<15}{net_remaining:<15.2f}\n")

def menu():
    while True:
        print("\n" + "_" * 50)
        print("_            SIMPLE BUDGET TRACKER            _")
        print("_" * 50)
        print("_ 1. Add Expense                               _")
        print("_ 2. Add Income                                _")
        print("_ 3. View Budget and Statement                 _")
        print("_ 4. Exit                                      _")
        print("_" * 50)
        choice = input("Enter your choice: ").strip()
        data = load_budget()
        if choice == "1":
            add_expense(data)
            save_budget(data)
        elif choice == "2":
            add_income(data)
            save_budget(data)
        elif choice == "3":
            view_budget(data)
        elif choice == "4":
            print("\nThank you for using Simple Budget Tracker. Goodbye!")
            save_budget(data)
            break
        else:
            print("Invalid choice. Try again.\n")

menu()
