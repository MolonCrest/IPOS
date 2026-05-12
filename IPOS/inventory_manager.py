# Jackson Hinks
# Inventory and Purchase Order System
# inventory_manager.py
# This file has the main inventory, vendor, and purchase order functions.
# Most functions use normal dictionaries because that matched my earlier Python projects.

from datetime import date
from models import Product, Vendor, PurchaseOrder


# -------------------------
# Small input helper functions
# -------------------------

def get_required_input(prompt):
    """Gets input from the user and makes sure it is not blank. Params: prompt, which is the message shown to the user. Returns: The user's non-empty input as a string."""
    while True:
        user_value = input(prompt).strip()
        if user_value != "":
            return user_value
        print("That field cannot be blank. Please try again.")


def get_valid_int(prompt, minimum=None):
    """gets a whole number from the user and checks the minimum when one is given. Params: prompt string and optional minimum integer. Returns: A valid integer."""
    while True:
        user_input = input(prompt).strip()

        try:
            number = int(user_input)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if minimum is not None and number < minimum:
            print(f"Please enter a number that is at least {minimum}.")
            continue

        return number


def get_valid_float(prompt, minimum=None):
    """Gets a decimal number from the user and validates the number. Params: prompt and an optional minimum value. Returns: A valid float."""
    while True:
        try:
            number = float(input(prompt))
            if minimum is not None and number < minimum:
                print(f"Please enter a number that is at least {minimum}.")
            else:
                return number
        except ValueError:
            print("Please enter a valid number.")


def get_yes_or_no(prompt):
    """Gets a yes or no answer from the user. Params: prompt, which is the message shown to the user. Returns: True for yes and False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False
        print("Please enter yes or no.")


def print_divider():
    """Prints a divider line to make console output easier to read. Params: None. Returns: None."""
    print("-" * 60)


# -------------------------
# Product functions
# -------------------------

def add_product(products, vendors, transaction_log=None):
    """Adds a new product after checking for duplicate product IDs. Params: products dictionary, vendors dictionary, and optional transaction_log list. Returns: None."""
    print("\nAdd Product")
    product_id = get_required_input("Product ID: ").upper()

    if product_id in products:
        print("A product with that ID already exists.")
        return

    if len(vendors) == 0:
        print("You need to add a vendor before adding products.")
        return

    name = get_required_input("Product Name: ")
    category = get_required_input("Category: ")
    quantity = get_valid_int("Quantity in Stock: ", 0)
    reorder_level = get_valid_int("Reorder Level: ", 0)
    reorder_quantity = get_valid_int("Reorder Quantity: ", 1)
    unit_price = get_valid_float("Unit Price: ", 0)

    # Show vendors first so the user does not have to remember the ID.
    view_all_vendors(vendors)
    vendor_id = get_required_input("Vendor ID: ").upper()

    if vendor_id not in vendors:
        print("That vendor ID was not found. Product was not added.")
        return

    products[product_id] = Product(
        product_id,
        name,
        category,
        quantity,
        reorder_level,
        reorder_quantity,
        unit_price,
        vendor_id,
        True
    )

    if transaction_log is not None:
        add_transaction(transaction_log, product_id, "Product Added", quantity, "New product added to inventory")

    print("Product added successfully.")


def view_all_products(products, include_inactive=True):
    """Displays all products currently stored in the program. Params: products dictionary and include_inactive boolean. Returns: None."""
    print("\nAll Products")
    if len(products) == 0:
        print("No products have been added yet.")
        return

    for product in products.values():
        if include_inactive or product.active:
            print_divider()
            for line in product.display_lines():
                print(line)
    print_divider()


def search_product_by_id(products, product_id):
    """Searches for a product by exact product ID. Params: products dictionary and product_id string. Returns: The matching Product object or None."""
    return products.get(product_id.upper())


def search_products_by_name(products, name_search):
    """Searches for products by part of the product name. Params: products dictionary and name_search string. Returns: A list of matching Product objects."""
    matches = []
    for product in products.values():
        if name_search.lower() in product.name.lower():
            matches.append(product)
    return matches


def search_products_by_category(products, category_search):
    """Searches for products by category. Params: products dictionary and category_search string. Returns: A list of matching Product objects."""
    matches = []
    for product in products.values():
        if category_search.lower() in product.category.lower():
            matches.append(product)
    return matches


def search_products_by_vendor(products, vendor_id):
    """Searches for products connected to one vendor ID. Params: products dictionary and vendor_id string. Returns: A list of matching Product objects."""
    matches = []
    for product in products.values():
        if product.vendor_id.upper() == vendor_id.upper():
            matches.append(product)
    return matches


def display_product_matches(matches):
    """Displays a list of product search results. Params: matches, which is a list of Product objects. Returns: None."""
    if len(matches) == 0:
        print("No matching products were found.")
        return

    for product in matches:
        print_divider()
        for line in product.display_lines():
            print(line)
    print_divider()


def search_products_menu(products):
    """Displays the product search menu and runs the selected search. Params: products dictionary. Returns: None."""
    while True:
        print("\nProduct Search Menu")
        print("1. Search by Product ID")
        print("2. Search by Product Name")
        print("3. Search by Category")
        print("4. Search by Vendor ID")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            product_id = get_required_input("Product ID: ")
            product = search_product_by_id(products, product_id)
            display_product_matches([product] if product else [])
        elif choice == "2":
            name_search = get_required_input("Product Name Search: ")
            display_product_matches(search_products_by_name(products, name_search))
        elif choice == "3":
            category_search = get_required_input("Category Search: ")
            display_product_matches(search_products_by_category(products, category_search))
        elif choice == "4":
            vendor_id = get_required_input("Vendor ID: ")
            display_product_matches(search_products_by_vendor(products, vendor_id))
        elif choice == "5":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 5.")


def edit_product(products, vendors):
    """Edits one product's information while keeping the same product ID. Params: products dictionary and vendors dictionary. Returns: None."""
    product_id = get_required_input("Enter Product ID to edit: ").upper()
    product = search_product_by_id(products, product_id)

    if product is None:
        print("Product was not found.")
        return

    print("Press Enter to keep the current value.")
    new_name = input(f"Name [{product.name}]: ").strip()
    new_category = input(f"Category [{product.category}]: ").strip()
    new_quantity = input(f"Quantity [{product.quantity}]: ").strip()
    new_reorder_level = input(f"Reorder Level [{product.reorder_level}]: ").strip()
    new_reorder_quantity = input(f"Reorder Quantity [{product.reorder_quantity}]: ").strip()
    new_unit_price = input(f"Unit Price [{product.unit_price}]: ").strip()
    new_vendor_id = input(f"Vendor ID [{product.vendor_id}]: ").strip().upper()

    if new_name:
        product.name = new_name
    if new_category:
        product.category = new_category
    if new_quantity:
        try:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                print("Quantity cannot be negative. Quantity was not changed.")
            else:
                product.quantity = new_quantity
        except ValueError:
            print("Invalid quantity. Quantity was not changed.")
    if new_reorder_level:
        try:
            new_reorder_level = int(new_reorder_level)
            if new_reorder_level < 0:
                print("Reorder level cannot be negative. Reorder level was not changed.")
            else:
                product.reorder_level = new_reorder_level
        except ValueError:
            print("Invalid reorder level. Reorder level was not changed.")
    if new_reorder_quantity:
        try:
            new_reorder_quantity = int(new_reorder_quantity)
            if new_reorder_quantity < 1:
                print("Reorder quantity must be at least 1. Reorder quantity was not changed.")
            else:
                product.reorder_quantity = new_reorder_quantity
        except ValueError:
            print("Invalid reorder quantity. Reorder quantity was not changed.")
    if new_unit_price:
        try:
            new_unit_price = float(new_unit_price)
            if new_unit_price < 0:
                print("Unit price cannot be negative. Unit price was not changed.")
            else:
                product.unit_price = new_unit_price
        except ValueError:
            print("Invalid unit price. Unit price was not changed.")
    if new_vendor_id:
        if new_vendor_id in vendors:
            product.vendor_id = new_vendor_id
        else:
            print("Vendor ID was not found. Vendor was not changed.")

    print("Product edit complete.")


def deactivate_product(products, transaction_log=None):
    """Marks a product as inactive instead of deleting it. Params: products dictionary and optional transaction_log list. Returns: None."""
    product_id = get_required_input("Enter Product ID to deactivate: ").upper()
    product = search_product_by_id(products, product_id)

    if product is None:
        print("Product was not found.")
        return

    if not product.active:
        print("This product is already inactive.")
        return

    product.active = False

    if transaction_log is not None:
        add_transaction(transaction_log, product_id, "Product Deactivated", 0, "Product was marked inactive")

    print("Product deactivated successfully.")


def display_low_stock_products(products):
    """Displays all active products that are at or under their reorder level. Params: products dictionary. Returns: None."""
    low_stock_items = []
    for product in products.values():
        if product.is_low_stock():
            low_stock_items.append(product)

    print("\nLow-Stock Products")
    display_product_matches(low_stock_items)


# -------------------------
# Vendor functions
# -------------------------

def add_vendor(vendors):
    """Adds a new vendor after checking for duplicate vendor IDs. Params: vendors dictionary. Returns: None."""
    print("\nAdd Vendor")
    vendor_id = get_required_input("Vendor ID: ").upper()

    if vendor_id in vendors:
        print("A vendor with that ID already exists.")
        return

    name = get_required_input("Vendor Name: ")
    contact_name = get_required_input("Contact Name: ")
    phone = get_required_input("Phone: ")
    email = get_required_input("Email: ")
    address = get_required_input("City/State or Address: ")

    vendors[vendor_id] = Vendor(vendor_id, name, contact_name, phone, email, address)
    print("Vendor added successfully.")


def view_all_vendors(vendors):
    """Displays all vendors currently stored in the program. Params: vendors dictionary. Returns: None."""
    print("\nAll Vendors")
    if len(vendors) == 0:
        print("No vendors have been added yet.")
        return

    for vendor in vendors.values():
        print_divider()
        for line in vendor.display_lines():
            print(line)
    print_divider()


def search_vendor_by_id(vendors, vendor_id):
    """Searches for a vendor by exact vendor ID. Params: vendors dictionary and vendor_id string. Returns: The matching Vendor object or None."""
    return vendors.get(vendor_id.upper())


def search_vendors_by_name(vendors, name_search):
    """Searches for vendors by part of the vendor name or contact name. Params: vendors dictionary and name_search string. Returns: A list of matching Vendor objects."""
    matches = []
    for vendor in vendors.values():
        name_match = name_search.lower() in vendor.name.lower()
        contact_match = name_search.lower() in vendor.contact_name.lower()
        if name_match or contact_match:
            matches.append(vendor)
    return matches


def display_vendor_matches(matches):
    """Displays a list of vendor search results. Params: matches, which is a list of Vendor objects. Returns: None."""
    if len(matches) == 0:
        print("No matching vendors were found.")
        return

    for vendor in matches:
        print_divider()
        for line in vendor.display_lines():
            print(line)
    print_divider()


def search_vendors_menu(vendors):
    """Displays the vendor search menu and runs the selected search. Params: vendors dictionary. Returns: None."""
    while True:
        print("\nVendor Search Menu")
        print("1. Search by Vendor ID")
        print("2. Search by Vendor Name or Contact")
        print("3. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            vendor_id = get_required_input("Vendor ID: ")
            vendor = search_vendor_by_id(vendors, vendor_id)
            display_vendor_matches([vendor] if vendor else [])
        elif choice == "2":
            name_search = get_required_input("Vendor Name or Contact Search: ")
            display_vendor_matches(search_vendors_by_name(vendors, name_search))
        elif choice == "3":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 3.")


def edit_vendor(vendors):
    """Edits one vendor's information while keeping the same vendor ID. Params: vendors dictionary. Returns: None."""
    vendor_id = get_required_input("Enter Vendor ID to edit: ").upper()
    vendor = search_vendor_by_id(vendors, vendor_id)

    if vendor is None:
        print("Vendor was not found.")
        return

    print("Press Enter to keep the current value.")
    new_name = input(f"Vendor Name [{vendor.name}]: ").strip()
    new_contact = input(f"Contact Name [{vendor.contact_name}]: ").strip()
    new_phone = input(f"Phone [{vendor.phone}]: ").strip()
    new_email = input(f"Email [{vendor.email}]: ").strip()
    new_address = input(f"Address [{vendor.address}]: ").strip()

    if new_name:
        vendor.name = new_name
    if new_contact:
        vendor.contact_name = new_contact
    if new_phone:
        vendor.phone = new_phone
    if new_email:
        vendor.email = new_email
    if new_address:
        vendor.address = new_address

    print("Vendor edit complete.")


# -------------------------
# Purchase order functions
# -------------------------

def get_next_po_number(purchase_orders):
    """Finds the next purchase order number based on existing purchase orders. Params: purchase_orders dictionary. Returns: A string like PO-1009."""
    highest_number = 1000

    for po_number in purchase_orders.keys():
        try:
            number_part = int(po_number.replace("PO-", ""))
            if number_part > highest_number:
                highest_number = number_part
        except ValueError:
            continue

    return f"PO-{highest_number + 1}"


def create_purchase_order(products, vendors, purchase_orders):
    """Creates a new purchase order with one or more products from the selected vendor. Params: products dictionary, vendors dictionary, and purchase_orders dictionary. Returns: None."""
    if len(vendors) == 0 or len(products) == 0:
        print("You need vendors and products before creating a purchase order.")
        return

    print("\nCreate Purchase Order")
    view_all_vendors(vendors)
    vendor_id = get_required_input("Choose Vendor ID: ").upper()

    if vendor_id not in vendors:
        print("Vendor was not found. Purchase order was not created.")
        return

    vendor_products = search_products_by_vendor(products, vendor_id)

    # Only active products should be ordered, so inactive items get skipped here.
    active_vendor_products = []
    for product in vendor_products:
        # I filter inactive products here so old/discontinued items cannot be reordered by mistake.
        if product.active:
            active_vendor_products.append(product)
    vendor_products = active_vendor_products

    if len(vendor_products) == 0:
        print("This vendor does not have any active products.")
        return

    print("\nProducts for this vendor:")
    display_product_matches(vendor_products)

    items_ordered = []

    # The PO can have more than one line item, so this loop keeps asking until the user is done.
    while True:
        product_id = get_required_input("Product ID to add to PO: ").upper()
        product = search_product_by_id(products, product_id)

        if product is None or product.vendor_id != vendor_id or not product.active:
            print("That product is not an active product for this vendor.")
        else:
            quantity = get_valid_int("Quantity to order: ", 1)
            items_ordered.append({
                "product_id": product.product_id,
                "quantity": quantity,
                "unit_price": product.unit_price
            })
            print("Item added to purchase order.")

        if not get_yes_or_no("Add another item to this PO? (y/n): "):
            break

    if len(items_ordered) == 0:
        print("No items were added. Purchase order was not created.")
        return

    # The PO number is created after items are added, so empty orders do not use up a number.
    po_number = get_next_po_number(purchase_orders)
    new_po = PurchaseOrder(po_number, vendor_id, str(date.today()), items_ordered, "Open")
    purchase_orders[po_number] = new_po

    print(f"Purchase order {po_number} created successfully.")
    print(f"Total Cost: ${new_po.calculate_total():.2f}")


def view_purchase_orders(purchase_orders):
    """Displays all purchase orders in the system. Params: purchase_orders dictionary. Returns: None."""
    print("\nPurchase Orders")
    if len(purchase_orders) == 0:
        print("No purchase orders have been created yet.")
        return

    for po in purchase_orders.values():
        print_divider()
        for line in po.display_lines():
            print(line)
    print_divider()


def search_purchase_order_by_number(purchase_orders, po_number):
    """Searches for a purchase order by exact PO number. Params: purchase_orders dictionary and po_number string. Returns: The matching PurchaseOrder object or None."""
    return purchase_orders.get(po_number.upper())


def search_purchase_orders_menu(purchase_orders):
    """Displays a purchase order search menu. Params: purchase_orders dictionary. Returns: None."""
    print("\nSearch Purchase Order")
    po_number = get_required_input("PO Number: ").upper()
    po = search_purchase_order_by_number(purchase_orders, po_number)

    if po is None:
        print("Purchase order was not found.")
        return

    print_divider()
    for line in po.display_lines():
        print(line)
    print_divider()


def mark_order_received(products, purchase_orders, transaction_log):
    """Marks a purchase order as received and updates inventory quantities once. Params: products dictionary, purchase_orders dictionary, and transaction_log list. Returns: None."""
    po_number = get_required_input("Enter PO Number to receive: ").upper()
    po = search_purchase_order_by_number(purchase_orders, po_number)

    if po is None:
        print("Purchase order was not found.")
        return

    if po.status == "Received":
        print("This purchase order has already been received. Inventory was not changed again.")
        return

    # This is the important receiving step. It updates stock once, then the PO is marked received.
    for item in po.items_ordered:
        product_id = item["product_id"]
        quantity = int(item["quantity"])

        if product_id in products:
            products[product_id].add_stock(quantity)
            add_transaction(
                transaction_log,
                product_id,
                "Shipment Received",
                quantity,
                f"Received through {po.po_number}"
            )
        else:
            print(f"Warning: Product {product_id} was not found and could not be updated.")

    po.mark_received()
    print(f"Purchase order {po.po_number} has been marked as received.")


# -------------------------
# Sort functions
# -------------------------

def sort_products_by_name(products):
    """Sorts products alphabetically by name. Params: products dictionary. Returns: A sorted list of Product objects."""
    product_list = list(products.values())
    product_list.sort(key=lambda product: product.name.lower())
    return product_list


def sort_products_by_quantity(products):
    """Sorts products by quantity in stock from lowest to highest. Params: products dictionary. Returns: A sorted list of Product objects."""
    sorted_products = sorted(products.values(), key=lambda product: product.quantity)
    return sorted_products


def sort_products_by_price(products):
    """Sorts products by unit price from lowest to highest. Params: products dictionary. Returns: A sorted list of Product objects."""
    return sorted(products.values(), key=lambda product: product.unit_price)


def sort_purchase_orders_by_date(purchase_orders):
    """Sorts purchase orders by date created. Params: purchase_orders dictionary. Returns: A sorted list of PurchaseOrder objects."""
    return sorted(purchase_orders.values(), key=lambda po: po.date_created)


def sort_products_menu(products, purchase_orders):
    """Displays the sort menu and prints sorted results. Params: products dictionary and purchase_orders dictionary. Returns: None."""
    while True:
        print("\nSort Menu")
        print("1. Sort Products by Name")
        print("2. Sort Products by Quantity")
        print("3. Sort Products by Price")
        print("4. Sort Purchase Orders by Date")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_product_matches(sort_products_by_name(products))
        elif choice == "2":
            display_product_matches(sort_products_by_quantity(products))
        elif choice == "3":
            display_product_matches(sort_products_by_price(products))
        elif choice == "4":
            sorted_orders = sort_purchase_orders_by_date(purchase_orders)
            for po in sorted_orders:
                print_divider()
                for line in po.display_lines():
                    print(line)
            print_divider()
        elif choice == "5":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 5.")


# -------------------------
# Extra feature: transaction log
# -------------------------

# Small testing idea I used while checking the transaction log.
# It stays commented out so it will not run during the final project.
# for test_transaction in transaction_log:
#     print(test_transaction)


def add_transaction(transaction_log, product_id, action, quantity, notes):
    """Adds one inventory transaction to the transaction log. Params: transaction_log list, product_id, action, quantity, and notes. Returns: None."""
    transaction_log.append({
        "date": str(date.today()),
        "product_id": product_id,
        "action": action,
        "quantity": int(quantity),
        "notes": notes
    })
