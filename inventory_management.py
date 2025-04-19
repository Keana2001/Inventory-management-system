import csv
import random
from datetime import datetime, timedelta
from code import (show_all_products, add_product, update_product, search_product,
                  inventory_report, export_inventory, product_sorting, filtering, discount, import_inventory,
                  export_data, SalesManager, inventory_manager)


def generate_sample_data(file_path="inventory.csv", num_products=25):
    """Generate sample inventory data and save to CSV file"""

    # Product categories
    categories = ["Electronics", "Clothing", "Home", "Sports", "Beauty", "Books", "Food", "Toys", "Other"]

    # Sample product names for each category
    product_names = {
        "Electronics": [
            "Wireless Earbuds", "Bluetooth Speaker", "Power Bank", "USB-C Cable", "Smart Watch",
            "Webcam HD", "Wireless Mouse", "Mechanical Keyboard", "External SSD", "HDMI Cable"
        ],
        "Clothing": [
            "T-Shirt Basic", "Denim Jeans", "Hoodie", "Athletic Socks", "Winter Jacket",
            "Cotton Shorts", "Yoga Pants", "Casual Shirt", "Baseball Cap", "Wool Sweater"
        ],
        "Home": [
            "Throw Pillow", "Ceramic Mug", "Bath Towel Set", "Kitchen Knife", "Cutting Board",
            "Bed Sheets", "Scented Candle", "Picture Frame", "Storage Basket", "Wall Clock"
        ],
        "Sports": [
            "Yoga Mat", "Jump Rope", "Water Bottle", "Resistance Bands", "Tennis Balls",
            "Running Shorts", "Dumbbell Set", "Golf Balls", "Basketball", "Swimming Goggles"
        ],
        "Beauty": [
            "Face Moisturizer", "Shampoo", "Body Lotion", "Facial Cleanser", "Hair Brush",
            "Nail Polish", "Lip Balm", "Eye Shadow Palette", "Facial Mask", "Sunscreen"
        ],
        "Books": [
            "Fiction Bestseller", "Cookbook", "Self-Help Guide", "Travel Guide", "History Book",
            "Biography", "Children's Book", "Science Fiction", "Business Book", "Art Book"
        ],
        "Food": [
            "Protein Bars", "Mixed Nuts", "Dark Chocolate", "Granola", "Coffee Beans",
            "Herbal Tea", "Olive Oil", "Pasta", "Spice Mix", "Energy Drink"
        ],
        "Toys": [
            "Building Blocks", "Stuffed Animal", "Puzzle Set", "Board Game", "Action Figure",
            "Art Supplies", "Remote Car", "Card Game", "Educational Toy", "Frisbee"
        ],
        "Other": [
            "Gift Card", "Phone Case", "Keychain", "Stickers Pack", "Notebook",
            "Pen Set", "Calendar", "Umbrella", "Tote Bag", "Sunglasses"
        ]
    }

    # Create products list
    products = []
    used_product_ids = set()

    for _ in range(num_products):
        # Generate unique product ID
        while True:
            product_id = f"P{random.randint(10000, 99999)}"
            if product_id not in used_product_ids:
                used_product_ids.add(product_id)
                break

        # Select random category and product name
        category = random.choice(categories)
        name = random.choice(product_names[category])
        # Add some variation to avoid exact duplicates
        name_suffix = random.choice(["", " Pro", " Plus", " Mini", " XL", " Premium", " Lite", " Basic"])
        full_name = f"{name}{name_suffix}"

        # Generate price (realistic range based on category)
        price_ranges = {
            "Electronics": (15.99, 199.99),
            "Clothing": (9.99, 89.99),
            "Home": (7.99, 79.99),
            "Sports": (8.99, 69.99),
            "Beauty": (5.99, 49.99),
            "Books": (10.99, 29.99),
            "Food": (3.99, 19.99),
            "Toys": (9.99, 39.99),
            "Other": (4.99, 24.99)
        }

        min_price, max_price = price_ranges[category]
        price = round(random.uniform(min_price, max_price), 2)

        # Generate quantity (some items might be low stock or out of stock)
        quantity_weights = [1, 3, 5, 10, 20, 15, 10, 5, 3, 2]  # Weights for 0-9 quantities
        if random.random() < 0.7:  # 70% chance for regular stock levels
            quantity = random.randint(10, 100)
        else:  # 30% chance for low or out of stock
            quantity = random.choices(range(10), weights=quantity_weights)[0]

        # Generate last updated date (within the last 30 days)
        days_ago = random.randint(0, 30)
        last_updated = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")

        # Create product dictionary
        product = {
            "product_id": product_id,
            "name": full_name,
            "category": category,
            "price": price,
            "quantity": quantity,
            "last_updated": last_updated
        }

        products.append(product)

    # Write to CSV file
    fieldnames = ["product_id", "name", "category", "price", "quantity", "last_updated"]

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"Generated {num_products} sample products in {file_path}")
    return products


def load_inventory(file_path="inventory.csv"):
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def options():
    while True:
        print("\nInventory Menu")
        print("1. Sample data")
        print("2. Add a new product")
        print("3. Update an exiting product")
        print("4. Search for a product")
        print("5. Inventory report")
        print("6. Export report")
        print("7. Sort products")
        print("8. Filter products")
        print("9. Add discount")
        print("10. Inventory import")
        print("11.Export data in different file formats ")
        print("12. Future inventory")
        print("13. Log inventory value")
        print("14. Display inventory value history")
        print("15. Display inventory value trend")
        print("16. Export inventory data")
        print("17. Exit")

        choice = input("Enter an option (1-20): ").strip()

        if choice == "1":
            show_all_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            search_product()
        elif choice == "5":
            inventory_report()
        elif choice == "6":
            export_data()
        elif choice == '7':
            product_sorting()
        elif choice == '8':
            filtering()
        elif choice == '9':
            discount()
        elif choice == '10':
            import_inventory()
        elif choice == "11":
            format_choice = input("Export format (csv/json): ").strip().lower()
            field_input = input("Enter fields to include (comma-separated) or leave blank for all: ").strip()
            category_filter = input("Filter by category (or leave blank): ").strip()
            stock_filter = input("Filter by stock status (in stock, low stock, out of stock or leave blank): ").strip()

            fields = [f.strip() for f in field_input.split(",")] if field_input else None
            filters = {}
            if category_filter:
                filters["category"] = category_filter
            if stock_filter:
                filters["stock_status"] = stock_filter.lower()

            export_inventory(
                export_format=format_choice,
                selected_fields=fields,
                filters=filters if filters else None
            )
        elif choice == "12":
            try:
                months = int(input("Forecast how many months ahead? (default 1): ").strip() or "1")
            except ValueError:
                months = 1

            sales_manager = SalesManager()
            sales_manager.forecast_inventory(months)
        elif choice == "13":
            inventory_manager.log_inventory_value()
        elif choice == "14":
            inventory_manager.display_text_trend()
        elif choice == "15":
            inventory_manager.show_value_trend()


if __name__ == "__main__":
    options()
