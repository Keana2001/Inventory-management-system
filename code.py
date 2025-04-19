import csv
from datetime import datetime
import os
import re
import json
import matplotlib.pyplot as plt


def load_inventory(file_path="inventory.csv"):
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


# show products


def show_all_products(file_path="inventory.csv"):
    inventory = load_inventory(file_path)
    print(f"\nShowing {len(inventory)} products:\n")
    for k in inventory:
        print(f"{k['product_id']} | {k['name']} | {k['category']} | R{k['price']} | Qty: {k['quantity']}")


# new product


def add_product(file_path="inventory.csv"):
    print("\nAdd New Product:")
    product_id = input("Enter product ID: ").strip()
    name = input("Enter product name: ").strip().title()

    while True:
        category = input("Enter category: ").strip().title()
        if not category:
            print("Category cannot be empty.")
        elif len(category) > 20:
            print("Category name too long (max 20 characters).")
        elif not re.match(r'^[A-Za-z0-9 ]+$', category):
            print("Category can only contain letters, numbers, and spaces.")
        else:
            break

    inventory = load_inventory(file_path)
    existing_names = {item['name'].strip().lower() for item in inventory}
    if name.lower() in existing_names:
        print(f"Error: A product named '{name}' already exists.")
        return

    try:
        price = float(input("Enter price: ").strip())
    except ValueError:
        print("Invalid input.")
        price = 0.0

    try:
        quantity = int(input("Enter quantity: ").strip())
    except ValueError:
        print("Invalid input.")
        quantity = 0

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_product = {
        "product_id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "last_updated": last_updated
    }

    inventory.append(new_product)

    fieldnames = ["product_id", "name", "category", "price", "quantity", "last_updated"]
    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

    print(f"Product '{name}' added successfully.")

# update products


def update_product(file_path="inventory.csv"):
    inventory = load_inventory(file_path)

    if not inventory:
        print("No inventory data found.")
        return

    product_id = input("Enter the product ID to update: ").strip()

    product = next((pr for pr in inventory if pr["product_id"] == product_id), None)

    if not product:
        print("Product not found.")
        return

    print(f"Current details for {product_id}: {product}")

    name_input = input(f"Enter new name [{product['name']}]: ").strip()
    name = name_input.title() if name_input else product['name']

    while True:
        category_input = input(f"Enter new category [{product['category']}]: ").strip()
        if not category_input:
            category = product['category']
            break
        category_input = category_input.title()
        if len(category_input) > 20:
            print("Category name too long (max 20 characters).")
        elif not re.match(r'^[A-Za-z0-9 ]+$', category_input):
            print("Category can only contain letters, numbers, and spaces.")
        else:
            category = category_input
            break

    try:
        price_input = input(f"Enter new price [{product['price']}]: ").strip()
        price = float(price_input) if price_input else float(product['price'])
    except ValueError:
        print("Invalid price input. Keeping original.")
        price = float(product['price'])

    try:
        quantity_input = input(f"Enter new quantity [{product['quantity']}]: ").strip()
        quantity = int(quantity_input) if quantity_input else int(product['quantity'])
    except ValueError:
        print("Invalid quantity input. Keeping original.")
        quantity = int(product['quantity'])

    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    product["name"] = name
    product["category"] = category
    product["price"] = price
    product["quantity"] = quantity
    product["last_updated"] = last_updated

    print(f"Updated details: {product}")

    fieldnames = ["product_id", "name", "category", "price", "quantity", "last_updated"]
    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory)

    print("Product updated successfully.")


# product search


def search_product(file_path="inventory.csv"):
    find = input("Enter product ID or name: ").strip().lower()

    inventory = load_inventory(file_path)

    product = [
        i for i in inventory if find in i['product_id'].lower() or find in i['name'].lower()
    ]

    if product:
        print(f"\nFound {len(product)} product(s):\n")
        for j in product:
            print(f"{j['product_id']} | {j['name']} | {j['category']} | R{j['price']} | Qty: {j['quantity']}")
    else:
        print("Product does not exist.")


# inventory report

def inventory_report(file_path="inventory.csv"):
    inventory = load_inventory(file_path)

    if not inventory:
        print("Inventory is empty.")
        return

    total_products = len(inventory)
    total_quantity = 0
    total_value = 0.0
    count = {}

    print("\nInventory Report")

    for total in inventory:
        quantity = int(total['quantity'])
        price = float(total['price'])
        category = total['category']

        total_quantity += quantity
        total_value += price * quantity

        if category in count:
            count[category] += 1
        else:
            count[category] = 1

    print(f"\nTotal number of products: {total_products}")
    print(f"Total quantity: {total_quantity}")
    print(f"Total inventory amount: R{total_value:,.2f}")

    print("\nNumber of products by category:")
    for category, count in count.items():
        print(f"  {category}: {count} product(s)")


# export data


def export_data(file_path="inventory.csv", path="inventory.csv"):
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        return

    try:
        with open(file_path, mode='r', newline='') as source_file:
            with open(path, mode='w', newline='') as report_file:
                for line in source_file:
                    report_file.write(line)
        print(f"Successfully exported to '{path}'.")
    except Exception as e:
        print(f"Error in export {e}")

# product sorting


def product_sorting(file_path="inventory.csv"):
    inventory = load_inventory(file_path)

    if not inventory:
        print("No items in inventory.")
        return

    print("\nSort by:")
    print("1. A-Z")
    print("2. Price from low to high")
    print("3. Quantity from low to high")
    choice = input("How would you like to sort it (1-3): ").strip()

    if choice == "1":
        inventory_sort = sorted(inventory, key=lambda x: x['name'].lower())
    elif choice == "2":
        inventory_sort = sorted(inventory, key=lambda x: float(x['price']))
    elif choice == "3":
        inventory_sort = sorted(inventory, key=lambda x: int(x['quantity']))
    else:
        print("Option does not exist, please choose a valid option.")
        return

    print(f"\nSorted Products ({len(inventory_sort)}):\n")
    for item in inventory_sort:
        print(f"{item['product_id']} | {item['name']} | {item['category']} | R{item['price']} | Qty: {item['quantity']}")


# data filtering


def filtering(file_path="inventory.csv"):
    inventory = load_inventory(file_path)

    if not inventory:
        print("Empty.")
        return

    print("\nFilter Options:")
    print("1. Price Range")
    print("2. Category")
    print("3. Stock position")
    choice = input("Filter option (1-3): ").strip()

    if choice == "1":
        try:
            min_price = float(input("Minimum price: "))
            max_price = float(input("Maximum price: "))
        except ValueError:
            print("Invalid input.")
            return

        filtered = [
            i for i in inventory if min_price <= float(i['price']) <= max_price
        ]

    elif choice == "2":
        category = input("Category to Filter by: ").strip().lower()
        filtered = [
            i for i in inventory if i['category'].strip().lower() == category
        ]

    elif choice == "3":
        print("1. In Stock")
        print("2. Low Stock")
        print("3. Out of Stock")
        position = input("Select stock status (1-3): ").strip()

        if position == "1":
            filtered = [r for r in inventory if int(r['quantity']) > 0]
        elif position == "2":
            filtered = [r for r in inventory if 0 < int(r['quantity']) <= 10]
        elif position == "3":
            filtered = [r for r in inventory if int(r['quantity']) == 0]
        else:
            print("Invalid option.")
            return
    else:
        print("Invalid filter choice.")
        return

    if filtered:
        print(f"\nFiltered Products ({len(filtered)}):\n")
        for item in filtered:
            print(f"{item['product_id']} | {item['name']} | {item['category']} | R{item['price']} | Qty: {item['quantity']}")
    else:
        print("No products match the selected filter.")

# batch updates/ discounts


def discount(file_path="inventory.csv"):
    inventory = load_inventory(file_path)

    if not inventory:
        print("Inventory empty.")
        return

    category = input("Category to add discount to: ").strip().lower()
    try:
        added_discount = float(input("Enter discount percentage (e.g., 10 for 10%): "))
        if added_discount <= 0 or added_discount >= 100:
            print("Please enter a valid percentage between 0 and 100.")
            return
    except ValueError:
        print("Invalid percentage input.")
        return

    updated = False
    for product in inventory:
        if product["category"].strip().lower() == category:
            old_price = float(product["price"])
            new_price = round(old_price * (1 - added_discount / 100), 2)
            product["price"] = new_price
            product["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = True

    if updated:
        fieldnames = ["product_id", "name", "category", "price", "quantity", "last_updated"]
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory)
        print(f"\nDiscount of {discount}% applied to all products in category '{category}'.")
    else:
        print(f"No products found '{category}'.")


# csv import


def validate_product_row(row):
    try:
        product = {
            "product_id": row["product_id"].strip(),
            "name": row["name"].strip().title(),
            "category": row["category"].strip().title(),
            "price": round(float(row["price"]), 2),
            "quantity": int(row["quantity"]),
            "last_updated": row["last_updated"].strip()
        }
        return product
    except (KeyError, ValueError):
        return None


def import_inventory(file_path="inventory.csv"):
    path_import = input("Enter the path to the CSV file: ").strip()

    if not os.path.exists(path_import):
        print(f"File does not exist: {path_import}")
        return

    current_inventory = load_inventory(file_path)
    inventory_id = {item["product_id"]: item for item in current_inventory}

    imported = 0
    updated = 0
    invalid = 0

    with open(path_import, mode="r", newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            validate = validate_product_row(row)
            if not validate:
                invalid += 1
                continue

            product_id = validate["product_id"]

            if product_id in inventory_id:
                inventory_id[product_id] = validate
                updated += 1
            else:
                inventory_id[product_id] = validate
                imported += 1

    with open(file_path, mode="w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "name", "category", "price", "quantity", "last_updated"])
        writer.writeheader()
        writer.writerows(inventory_id.values())

    print("\n--- Import Information ---")
    print(f"Imported: {imported} new products")
    print(f"Updated: {updated} current products")
    print(f"Invalid rows skipped: {invalid}")


# export information

def export_inventory(
    file_path="inventory.csv",
    path_formatted="exported_inventory",
    export_format="csv",
    selected_fields=None,
    filters=None
):

    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        return

    inventory = load_inventory(file_path)

    if not inventory:
        print("Data to export is invalid.")
        return

    if filters:
        if "category" in filters:
            inventory = [i for i in inventory if i["category"].lower() == filters["category"].lower()]
        if "stock_status" in filters:
            def get_status(qty):
                t = int(qty)
                if t == 0:
                    return "out of stock"
                elif t <= 10:
                    return "low stock"
                else:
                    return "in stock"
            inventory = [q for q in inventory if get_status(q["quantity"]) == filters["stock_status"]]

    if selected_fields:
        inventory = [
            {field: item[field] for field in selected_fields if field in item}
            for item in inventory
        ]

    extension = "csv" if export_format == "csv" else "json"
    full_path = f"{path_formatted}.{extension}"

    try:
        if export_format == "csv":
            fieldnames = selected_fields if selected_fields else inventory[0].keys()
            with open(full_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(inventory)
        elif export_format == "json":
            with open(full_path, mode='w') as file:
                json.dump(inventory, file, indent=2)
        else:
            print("Unsupported export format.")
            return

        print(f"Successfully exported {len(inventory)} products to '{full_path}'.")
    except Exception as e:
        print(f"Error during export: {e}")


# Sales projection

class SalesManager:
    def __init__(self, inventory_file="inventory.csv"):
        self.inventory_file = inventory_file

    def _load_inventory_data(self):
        inventory = {}
        if not os.path.exists(self.inventory_file):
            return inventory

        with open(self.inventory_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    pid = row["product_id"]
                    inventory[pid] = {
                        "name": row.get("name", "Unknown"),
                        "stock": int(row.get("quantity", 0)),
                        "monthly_sales": int(row.get("monthly_sales", 0))
                    }
                except (KeyError, ValueError):
                    continue
        return inventory

    def forecast_inventory(self, months=1):
        inventory = self._load_inventory_data()
        today = datetime.now()
        season_multiplier = self._get_seasonal_multiplier(today.month)

        print(f"\nForecasting for next {months} month(s)...\n")
        print(f"{'Product ID':<12}{'Name':<25}{'Current Stock':<15}{'Forecast Demand':<20}{'Status'}")

        for prid, data in inventory.items():
            stock = data["stock"]
            name = data["name"]
            monthly_sales = data["monthly_sales"]

            demand = int(monthly_sales * months * season_multiplier)
            deficit = demand - stock
            status = "Still good" if deficit <= 0 else f"Time to restock {deficit}"

            print(f"{prid:<12}{name:<25}{stock:<15}{demand:<20}{status}")

    def _get_seasonal_multiplier(self, month):
        seasonal_effects = {
            12: 1.4,
            11: 1.2,
            1: 0.85
        }
        return seasonal_effects.get(month, 1.0)


# Inventory value tracking


class InventoryManager:
    def __init__(self, inventory_file="inventory.csv"):
        self.inventory_file = inventory_file
        self.inventory_data = self._load_inventory_data()
        self.inventory_value_history = []

    def _load_inventory_data(self):
        inventory = {}
        if not os.path.exists(self.inventory_file):
            return inventory

        with open(self.inventory_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                product_id = row["product_id"]
                price = float(row["price"])
                quantity = int(row["quantity"])
                inventory[product_id] = {
                    "name": row["name"],
                    "price": price,
                    "quantity": quantity,
                    "last_updated": row["last_updated"]
                }
        return inventory

    def log_inventory_value(self):
        total_value = 0
        for product in self.inventory_data.values():
            total_value += product["price"] * product["quantity"]
        self.inventory_value_history.append({"date": datetime.now(), "value": total_value})
        print(f"Current Inventory Value: R{total_value:.2f}")

    def filter_inventory_history_by_date(self, start_date, end_date):
        filtered_history = [
            entry for entry in self.inventory_value_history
            if start_date <= entry['date'] <= end_date
        ]
        return filtered_history

    def show_value_trend(self):
        start_date = datetime(2025, 3, 1)
        end_date = datetime.now()

        filtered_history = self.filter_inventory_history_by_date(start_date, end_date)

        if not filtered_history:
            print("No inventory value data available.")
            return

        dates = [entry['date'] for entry in filtered_history]
        values = [entry['value'] for entry in filtered_history]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', linestyle='-', color='b')
        plt.title('Inventory Value Trend (1st March 2025 to Today)')
        plt.xlabel('Date')
        plt.ylabel('Inventory Value (R)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def display_text_trend(self):
        if not self.inventory_value_history:
            print("No inventory value history available.")
            return

        print(f"\n{'Date':<25} {'Inventory Value (R)':<20}")
        print("-" * 45)
        for entry in self.inventory_value_history:
            print(f"{entry['date'].strftime('%Y-%m-%d %H:%M:%S'):<25} {entry['value']:<20.2f}")


inventory_manager = InventoryManager()
