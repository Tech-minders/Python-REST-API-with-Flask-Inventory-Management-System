import requests  
import json      

BASE_URL = "http://127.0.0.1:5000" 

def print_response(response):
    try:
        data = response.json()
        print(json.dumps(data, indent=2))  # indent=2 makes it nicely formatted
    except Exception:
        print(response.text)


# View all inventory items

def view_all_items():
    print("\n--- All Inventory Items ---")
    response = requests.get(f"{BASE_URL}/inventory")
    print_response(response)


# View one item by ID

def view_one_item():
    item_id = input("\nEnter item ID: ").strip()
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    print_response(response)

# Add a new item manually

def add_item():
    print("\n--- Add New Inventory Item ---")
    product_name = input("Product name: ").strip()
    brands = input("Brand (or press Enter to skip): ").strip()
    ingredients = input("Ingredients (or press Enter to skip): ").strip()

    # Keep asking for price until the user enters a valid number
    while True:
        try:
            price = float(input("Price (e.g. 3.99): ").strip())
            break
        except ValueError:
            print("Please enter a valid number for price.")

    # Keep asking for stock until the user enters a valid whole number
    while True:
        try:
            stock = int(input("Stock quantity: ").strip())
            break
        except ValueError:
            print("Please enter a valid whole number for stock.")

    new_item = {
        "product_name": product_name,
        "brands": brands,
        "ingredients_text": ingredients,
        "price": price,
        "stock": stock
    }

    response = requests.post(f"{BASE_URL}/inventory", json=new_item)
    print("\nItem created:")
    print_response(response)


#  Update an existing item

def update_item():
    print("\n--- Update Inventory Item ---")
    item_id = input("Enter item ID to update: ").strip()

    print("What do you want to update?")
    print("  1. Price")
    print("  2. Stock")
    print("  3. Product name")

    choice = input("Enter 1, 2, or 3: ").strip()

    updates = {}  # we only send the fields that changed

    if choice == "1":
        while True:
            try:
                updates["price"] = float(input("New price: ").strip())
                break
            except ValueError:
                print("Please enter a valid number.")

    elif choice == "2":
        while True:
            try:
                updates["stock"] = int(input("New stock quantity: ").strip())
                break
            except ValueError:
                print("Please enter a valid whole number.")

    elif choice == "3":
        updates["product_name"] = input("New product name: ").strip()

    else:
        print("Invalid choice.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=updates)
    print("\nUpdated item:")
    print_response(response)

#  Delete an item

def delete_item():
    print("\n--- Delete Inventory Item ---")
    item_id = input("Enter item ID to delete: ").strip()

    confirm = input(f"Are you sure you want to delete item {item_id}? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print_response(response)


# Find a product on OpenFoodFacts by barcode

def find_by_barcode():
    print("\n--- Search OpenFoodFacts by Barcode ---")
    barcode = input("Enter barcode number: ").strip()

    response = requests.get(f"{BASE_URL}/search/barcode/{barcode}")
    print_response(response)


# Search products by name on OpenFoodFacts

def search_by_name():
    print("\n--- Search OpenFoodFacts by Name ---")
    name = input("Enter product name to search: ").strip()

    response = requests.get(f"{BASE_URL}/search/name/{name}")
    print_response(response)


# MAIN MENU

def main():
    print("\n====================================")
    print("   Inventory Management System ")
    print("====================================")

    # Check if the server is running before showing menu
    try:
        requests.get(f"{BASE_URL}/inventory", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\nERROR: Flask server is not running!")
        print("Please start it first: python app.py")
        return

    # Keep showing the menu until user quits
    while True:
        print("\n--- Main Menu ---")
        print("1. View all inventory items")
        print("2. View one item by ID")
        print("3. Add a new item")
        print("4. Update an item")
        print("5. Delete an item")
        print("6. Find product by barcode (OpenFoodFacts)")
        print("7. Search product by name (OpenFoodFacts)")
        print("8. Quit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_one_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            find_by_barcode()
        elif choice == "7":
            search_by_name()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()