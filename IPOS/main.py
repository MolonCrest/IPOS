# Jackson Hinks
# Inventory and Purchase Order System
# main.py
# This is the starting point for the program. I kept the menus pretty plain,
# because for this kind of console project it is easier to test and explain that way.

from file_manager import load_starting_data, save_data, export_json_backup
from inventory_manager import (
    add_product,
    view_all_products,
    search_products_menu,
    edit_product,
    deactivate_product,
    display_low_stock_products,
    add_vendor,
    view_all_vendors,
    search_vendors_menu,
    edit_vendor,
    create_purchase_order,
    view_purchase_orders,
    search_purchase_orders_menu,
    mark_order_received,
    sort_products_menu
)
from reports import reports_menu

DATA_FILE = "inventory_data.json"
BACKUP_FILE = "backup_inventory_data.json"


def product_management_menu(products, vendors, transaction_log):
    """Shows the product menu and calls the product-related functions. Params: products dictionary, vendors dictionary, and transaction_log list. Returns: None."""
    while True:
        print("\nProduct Management")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Products")
        print("4. Edit Product")
        print("5. Deactivate Product")
        print("6. Display Low-Stock Products")
        print("7. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_product(products, vendors, transaction_log)
        elif choice == "2":
            view_all_products(products)
        elif choice == "3":
            search_products_menu(products)
        elif choice == "4":
            edit_product(products, vendors)
        elif choice == "5":
            deactivate_product(products, transaction_log)
        elif choice == "6":
            display_low_stock_products(products)
        elif choice == "7":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 7.")


def vendor_management_menu(vendors):
    """Shows the vendor menu and calls the vendor functions. Params: vendors dictionary. Returns: None."""
    while True:
        print("\nVendor Management")
        print("1. Add Vendor")
        print("2. View All Vendors")
        print("3. Search Vendors")
        print("4. Edit Vendor")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_vendor(vendors)
        elif choice == "2":
            view_all_vendors(vendors)
        elif choice == "3":
            search_vendors_menu(vendors)
        elif choice == "4":
            edit_vendor(vendors)
        elif choice == "5":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 5.")


def purchase_order_menu(products, vendors, purchase_orders, transaction_log):
    """Shows the purchase order menu and sends the user to PO actions. Params: products dictionary, vendors dictionary, purchase_orders dictionary, and transaction_log list. Returns: None."""
    while True:
        print("\nPurchase Order System")
        print("1. Create Purchase Order")
        print("2. View Existing Purchase Orders")
        print("3. Search Purchase Order by PO Number")
        print("4. Mark Purchase Order as Received")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_purchase_order(products, vendors, purchase_orders)
        elif choice == "2":
            view_purchase_orders(purchase_orders)
        elif choice == "3":
            search_purchase_orders_menu(purchase_orders)
        elif choice == "4":
            mark_order_received(products, purchase_orders, transaction_log)
        elif choice == "5":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 5.")


def save_menu(products, vendors, purchase_orders, transaction_log):
    """Gives the user the normal save and backup save options. Params: products dictionary, vendors dictionary, purchase_orders dictionary, and transaction_log list. Returns: None."""
    while True:
        print("\nSave and Backup Menu")
        print("1. Save Data")
        print("2. Save Backup JSON File")
        print("3. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            save_data(DATA_FILE, products, vendors, purchase_orders, transaction_log)
        elif choice == "2":
            export_json_backup(BACKUP_FILE, products, vendors, purchase_orders, transaction_log)
        elif choice == "3":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 3.")


def main_menu():
    """Loads saved data, runs the main menu loop, and saves before closing. Params: None. Returns: None."""
    # These four variables are passed around instead of using globals everywhere.
    products, vendors, purchase_orders, transaction_log = load_starting_data(DATA_FILE, "sample_data.json")

    while True:
        print("\nInventory and Purchase Order System")
        print("1. Product Management")
        print("2. Vendor Management")
        print("3. Purchase Order System")
        print("4. Sort Features")
        print("5. Reports")
        print("6. Save and Backup")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            product_management_menu(products, vendors, transaction_log)
        elif choice == "2":
            vendor_management_menu(vendors)
        elif choice == "3":
            purchase_order_menu(products, vendors, purchase_orders, transaction_log)
        elif choice == "4":
            sort_products_menu(products, purchase_orders)
        elif choice == "5":
            reports_menu(products, vendors, purchase_orders, transaction_log)
        elif choice == "6":
            save_menu(products, vendors, purchase_orders, transaction_log)
        elif choice == "7":
            save_data(DATA_FILE, products, vendors, purchase_orders, transaction_log)
            print("Program closed. Data was saved.")
            break
        else:
            print("Invalid menu choice. Please choose 1 through 7.")


# This is the only file that should directly start the program.
if __name__ == "__main__":
    main_menu()
