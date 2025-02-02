from datetime import datetime, timedelta

class Refrigerator:
    def __init__(self):
        self.inventory = {}  # Stores item data
        self.history = []  # Stores purchase and consumption history

    def insert(self, name, quantity, unit, expiry_date=None):
        """
        Adds an item to the refrigerator.
        """
        if name in self.inventory:
            self.inventory[name]['quantity'] += quantity
        else:
            self.inventory[name] = {'quantity': quantity, 'unit': unit, 'expiry_date': expiry_date}

        self.history.append(f"Inserted {quantity} {unit} of {name} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{name} added successfully.")

    def consume(self, name, quantity):
        """
        Consumes an item from the refrigerator.
        """
        if name in self.inventory and self.inventory[name]['quantity'] >= quantity:
            self.inventory[name]['quantity'] -= quantity
            self.history.append(f"Consumed {quantity} {self.inventory[name]['unit']} of {name} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{quantity} {self.inventory[name]['unit']} of {name} consumed.")
        else:
            print("Insufficient quantity or item not found.")

    def status(self):
        """
        Displays the current inventory.
        """
        if not self.inventory:
            print("The refrigerator is empty.")
        else:
            print("Current Inventory:")
            for item, details in self.inventory.items():
                print(f"{item}: {details['quantity']} {details['unit']} (Expires: {details['expiry_date']})")

    def check_expiry(self):
        """
        Checks for items that are about to expire or have expired.
        """
        today = datetime.today().date()
        for item, details in list(self.inventory.items()):
            expiry_date = details['expiry_date']
            if expiry_date:
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
                if expiry_date < today:
                    print(f"{item} has expired! Removing from inventory.")
                    del self.inventory[item]
                elif expiry_date <= today + timedelta(days=2):
                    print(f"Warning: {item} is about to expire on {expiry_date}!")

    def shopping_list(self):
        """
        Suggests a shopping list based on past consumption.
        """
        suggested_items = {}
        for record in self.history:
            if "Consumed" in record:
                parts = record.split()
                quantity = float(parts[1])
                name = parts[3]
                if name in suggested_items:
                    suggested_items[name] += quantity
                else:
                    suggested_items[name] = quantity

        print("Suggested Shopping List:")
        for item, quantity in suggested_items.items():
            print(f"{item}: {quantity} (based on past usage)")

# User interaction
fridge = Refrigerator()
while True:
    print("\n1. Insert Item\n2. Consume Item\n3. Show Status\n4. Check Expiry\n5. Shopping List\n6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter item name: ")
        quantity = float(input("Enter quantity: "))
        unit = input("Enter unit (liters, grams, etc.): ")
        expiry_date = input("Enter expiry date (YYYY-MM-DD) or press Enter to skip: ")
        expiry_date = expiry_date if expiry_date else None
        fridge.insert(name, quantity, unit, expiry_date)
    elif choice == "2":
        name = input("Enter item name to consume: ")
        quantity = float(input("Enter quantity to consume: "))
        fridge.consume(name, quantity)
    elif choice == "3":
        fridge.status()
    elif choice == "4":
        fridge.check_expiry()
    elif choice == "5":
        fridge.shopping_list()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")



# 2 : Evaluate Expression 

import operator

def precedence(op):
    """Returns precedence of the operator."""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    if op == '(':  # Lowest precedence for opening parenthesis
        return 0
    return -1

def apply_operation(a, b, op):
    """Applies the operation on two operands."""
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv  # Supporting floating-point division
    }
    return operations[op](a, b)

def evaluate(expression):
    """Evaluates a mathematical expression considering precedence, associativity, and parentheses."""
    values = []  # Stack to store values
    ops = []  # Stack to store operators
    i = 0

    while i < len(expression):
        if expression[i].isdigit() or (expression[i] == '-' and (i == 0 or expression[i-1] in "(+-*/")):
            val = 0
            negative = False
            if expression[i] == '-':
                negative = True
                i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                val = val * 10 + int(expression[i]) if expression[i] != '.' else val + 0.1
                i += 1
            if negative:
                val = -val
            values.append(val)
            i -= 1
        elif expression[i] == '(':
            ops.append(expression[i])
        elif expression[i] == ')':
            while ops and ops[-1] != '(':
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                values.append(apply_operation(a, b, op))
            ops.pop()  # Remove '('
        elif expression[i] in '+-*/':
            while ops and precedence(ops[-1]) >= precedence(expression[i]):
                b = values.pop()
                a = values.pop()
                op = ops.pop()
                values.append(apply_operation(a, b, op))
            ops.append(expression[i])
        i += 1

    while ops:
        b = values.pop()
        a = values.pop()
        op = ops.pop()
        values.append(apply_operation(a, b, op))

    return values[0]

# Taking user input
expression = input("Enter mathematical expression: ").replace(" ", "")
print("Output:", evaluate(expression))
