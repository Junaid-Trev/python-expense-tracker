from __future__ import print_function

try:
    input = raw_input
except NameError:
    pass

import datetime

DATE_FMT = "%Y-%m-%d"
FILE_NAME = "expenses.txt"

def parse_line(line):
    line = line.strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split(",")]
    if len(parts) == 2:
        catergory, amount_text = parts
        date_text = "N/A"
    else:
        category = parts[0]
        amount_text = parts[1] if len(parts) > 1 else "0"
        date_text = parts[2] if len(parts) > 2 else "N/A"
    try:
        amount = float(amount_text)
    except:
        return None
    return {"category": category, "amount": amount, "date": date_text}

def get_total_expenses():
    try:
        total = 0.0
        with open(FILE_NAME, "r") as f:
            for line in f:
                item = parse_line(line)
                if not item:
                    continue
                total += item["amount"]
        return total
    except (IOError, OSError):
        return 0.0


def prompt_date():
    while True:
        date_in = input("Enter date (YYYY-MM-DD) or press Enter for today :").strip()
        if not date_in:
            return datetime.date.today().strftime(DATE_FMT)
        try:
            dt = datetime.datetime.strptime(date_in, DATE_FMT)
            return dt.strftime(DATE_FMT)
        except:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-07-21)")

def add_expense():
    category = input("Enter category: ")
    while not category:
        category = input("Please enter a category: ").strip()

    #validate numeric amount
    while True:
        amt = input("Enter amount (e.g. 12.50): ").strip()
        try:
            amount = float(amt)
            break
        except:
            print("Invalid amount. Use digits only, e.g. 20 or 15.50")

    date_text = prompt_date()

    try:
        with open(FILE_NAME, "a") as f:
            f.write("{},{},{}\n".format(category.strip(), "{:.2f}".format(amount), date_text))
    except (IOError, OSError):
        print("Could not write to {}. Check folder permissions.".format(FILE_NAME))
        return

    #Real-time total
    total = get_total_expenses()
    print("Expenses saved! Your new total is: R{:.2f}\n".format(total))

def view_expenses():
    try:
        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
    except (IOError, OSError):
        print("\nNo expenses found. Please add some first.\n")
        return

    if not lines:
        print("\nNo expenses found. Please add some first.\n")
        return


    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 2:
            continue
        category = parts[0]
        try:
            amount = float(parts[1])
        except:
            amount = 0.0
        date_text = parts[2] if len(parts) > 2 else "N/A"
        items.append({"category": category, "amount": amount, "date": date_text})

    if not items:
        print("\nNo expenses found. Please add some first.\n")
        return

    print("\n--- Your Saved Expenses ---")
    print("{:<12} | {:<12} | {:>10}".format("Date", "Category", "Amount (R)" ))
    print("-" * 42)
    total = 0.0
    for it in items:
        print("{:<12} | {:<12} | {:>10.2f}".format(it["date"], it["category"], it["amount"]))
        total += it["amount"]
    print("-" * 42)
    print("Total: R{:.2f}\n".format(total))

def main():
    while True:
        print("Expense Tracker")
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Thank you for using our App! Goodbye")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()







