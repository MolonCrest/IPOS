# Jackson Hinks
# Inventory and Purchase Order System
# file_manager.py
# This file handles saving and loading JSON data.
# Keeping this separate keeps main.py from turning into a giant file.

import json
from models import Product, Vendor, PurchaseOrder


def data_to_dict(products, vendors, purchase_orders, transaction_log):
    """converts the object dictionaries into regular lists/dictionaries for JSON. Params: products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list. Returns: A dictionary containing all save data."""
    # JSON cannot save the custom objects directly, so each object gets turned
    # into a plain dictionary first.
    product_list = []
    for product in products.values():
        product_list.append(product.to_dict())

    vendor_list = []
    for vendor in vendors.values():
        vendor_list.append(vendor.to_dict())

    po_list = []
    for po in purchase_orders.values():
        po_list.append(po.to_dict())

    save_data_dictionary = {
        "products": product_list,
        "vendors": vendor_list,
        "purchase_orders": po_list,
        "transaction_log": transaction_log
    }

    return save_data_dictionary


def dict_to_data(data):
    """Converts JSON dictionary data back into program objects. Params: data, which is the dictionary loaded from a JSON file. Returns: products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list."""
    products = {}
    vendors = {}
    purchase_orders = {}

    # Vendors are loaded first because products point back to vendor IDs.
    for vendor_data in data.get("vendors", []):
        vendor = Vendor.from_dict(vendor_data)
        vendors[vendor.vendor_id] = vendor

    for product_data in data.get("products", []):
        product = Product.from_dict(product_data)
        products[product.product_id] = product

    for po_data in data.get("purchase_orders", []):
        purchase_order = PurchaseOrder.from_dict(po_data)
        purchase_orders[purchase_order.po_number] = purchase_order

    # Older test files might not have a transaction_log yet, so an empty list is safer.
    transaction_log = data.get("transaction_log", [])
    return products, vendors, purchase_orders, transaction_log


def save_data(file_name, products, vendors, purchase_orders, transaction_log):
    """Saves products, vendors, purchase orders, and transaction log data to a JSON file. Params: file_name, products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list. Returns: True if the save worked, otherwise False."""
    try:
        data = data_to_dict(products, vendors, purchase_orders, transaction_log)
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_name}.")
        return True
    except OSError as error:
        print(f"Save failed because the file could not be written: {error}")
        return False


def load_data(file_name):
    """Loads products, vendors, purchase orders, and transaction log data from a JSON file. Params: file_name, which is the JSON file to load. Returns: products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"Data loaded from {file_name}.")
        return dict_to_data(data)
    except FileNotFoundError:
        print(f"File {file_name} was not found.")
        return {}, {}, {}, []
    except json.JSONDecodeError:
        print(f"File {file_name} is not valid JSON.")
        return {}, {}, {}, []
    except KeyError as error:
        print(f"The JSON file is missing expected data: {error}")
        return {}, {}, {}, []


# This function is used when the program first opens.
def load_starting_data(main_file="inventory_data.json", sample_file="sample_data.json"):
    """Loads the main data file first, then falls back to sample data if needed. Params: main_file and sample_file file name strings. Returns: products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list."""
    products, vendors, purchase_orders, transaction_log = load_data(main_file)

    if len(products) == 0 and len(vendors) == 0 and len(purchase_orders) == 0:
        print("Trying to load sample data instead.")
        products, vendors, purchase_orders, transaction_log = load_data(sample_file)

    return products, vendors, purchase_orders, transaction_log


# A second save option, mostly so the project has a simple backup feature.
def export_json_backup(file_name, products, vendors, purchase_orders, transaction_log):
    """Saves a second JSON backup file with the current program data. Params: file_name, products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list. Returns: True if the backup worked, otherwise False."""
    return save_data(file_name, products, vendors, purchase_orders, transaction_log)


# Quick JSON load test I used while checking the sample data.
# This is commented out because main.py should be the file that starts the program.
# if __name__ == "__main__":
#     products, vendors, purchase_orders, transaction_log = load_starting_data()
#     print(len(products), len(vendors), len(purchase_orders), len(transaction_log))
