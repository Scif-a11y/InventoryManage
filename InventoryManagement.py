import json
from pathlib import Path
import time

inventory = {}
data = {}
cart = {}
name = input("Enter Your Name: ")
password = input("Enter password: ")
file_dir = Path("userData")
file_dir.mkdir(exist_ok=True)
file_path = file_dir / f"{name}.json"
file_path_data = file_dir / f"{name}data.json"
if file_path.exists():
    with open(file_path, 'r') as f:
        inventory = json.load(f)
        if inventory[name] != password:
            print("Invalid Password")
            exit()
else:
    with open(file_path, 'w') as f:
        inventory[name.lower()] = password
        json.dump(inventory, f, indent=4)

if file_path_data.exists():
    with open(file_path_data, 'r') as f:
        data = json.load(f)
else:
    with open(file_path_data, 'w') as f:
        json.dump(data, f, indent=4)

def add():
    count = 1
    while True:
        item = input(f"Enter item {count} to be added (or type 'exit' or 'e' to return): ")
        if item.lower() in ["e", "exit"]:
            print("Returning to main menu.")
            break
        try:
            amt = int(input("Enter amount in numbers (in kg, dozens, etc.): "))
            price = float(input("Enter price of item: "))
            if item in inventory:
                inventory[item]['amount'] += amt
            else:
                inventory[item] = {'amount': amt, 'price': price}
        except ValueError:
            print("Invalid input. Please enter numeric values for amount and price.")
            continue
        count += 1

def viewInventory():
    if len(inventory) == 0:
        print("Inventory Empty!")
        add()
        return
    count = 1
    for item, details in inventory.items():
        # print(name)
        if item == name:
            print("running")
            continue
        print(f"Item {count}: {item}\t|\tAmount: {details['amount']}\t|\tPrice(in inr): {details['price']}")
        count += 1

def inventorycheck():
    viewInventory()
    for item, details in inventory.items():
        if isinstance(details, dict) and 'amount' in details:
            if details['amount'] == 0:
                print(f"Low Inventory for {item}")
def sell_items():
    while True:
        inventorycheck()
        item = input("What item do you want to sell, or enter 'e' or 'exit' to return: ")
        if item.lower() in ["e", "exit"]:
            break
        if item in inventory:
            try:
                amt = int(input("Amount to be sold: "))
                if amt > inventory[item]['amount']:
                    print("Amount exceeds availability.")
                    continue

                if item in cart:
                    cart[item]['amount'] += amt
                else:
                    cart[item] = {'amount': amt, 'price': inventory[item]['price']}
                inventory[item]['amount'] -= amt
                print(f"Added {amt} of {item} to the cart.")

                checkout_decision = input("Do you want to checkout? (yes/no): ").strip().lower()
                if checkout_decision in ["yes", "y"]:
                    checkout()
                    break

            except ValueError:
                print("Invalid amount. Please enter a number.")
        else:
            print("Item not in inventory.")

def view_cart():
    if not cart:
        print("Cart is empty!")
        return
    print("Your Cart:")
    total_cost = 0
    for item, details in cart.items():
        print(f"{item}: {details['amount']} @ {details['price']} INR each")
        total_cost += details['amount'] * details['price']
    print(f"Total Cost: {total_cost} INR")

def checkout():
    if not cart:
        print("Cart is empty. Please add items to the cart before checking out.")
        return

    view_cart()
    total_cost = sum(details['amount'] * details['price'] for details in cart.values())

    while True:
        try:
            change = float(input(f"\nEnter amount given by user: "))
            if change < total_cost:
                print("Not enough money provided. Please enter a valid amount.")
            else:
                print(f"Change: {change - total_cost:.2f} INR")
                break
        except ValueError:
            print("Invalid amount entered. Please enter a numeric value.")

    for item, details in cart.items():
        inventory[item]['amount'] -= details['amount']
        if item in data:
            data[item]['amount'] += details['amount']
        else:
            local_time = time.localtime()
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            data[item] = {'amount': details['amount'], 'price': details['price'], 'time': formatted_time}

    cart.clear()
    print("Checkout successful! Thank you for your purchase.")

def view_data_sorted(sort_by="name"):
    if not data:
        print("No sales data to show.")
        return
    print("Sales Data:")
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1]['amount'], reverse=True))
    sorted_data = data
    for item, details in sorted_data.items():
        print(f"Item: {item}\t|\tAmount Sold: {details['amount']}\t|\tPrice: {details['price']} INR")

def main():
    while True:
        local_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        print("\n1. Add Items\t\t\t\t\t\t\t\t\t| Time:", formatted_time, "|")
        print("2. Selling Accounts Window (Add to Cart and Checkout)")
        print("3. View Inventory")
        print("4. View Sorted Sales Data")
        print("5. End Program")
        try:
            inp = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if inp == 1:
            add()
        elif inp == 2:
            sell_items()
        elif inp == 3:
            viewInventory()
        elif inp == 4:
            view_data_sorted('amount')
        elif inp == 5:
            print("Exiting.....")
            break
        else:
            print("Invalid option. Try again.")
    with open(file_path, 'w') as f:
        json.dump(inventory, f, indent=4)
    with open(file_path_data, 'w') as f:
        json.dump(data, f, indent=4)
main()
