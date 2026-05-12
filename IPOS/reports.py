# Jackson Hinks
# Inventory and Purchase Order System
# reports.py
# This file stores the reporting functions for the project.

from inventory_manager import print_divider


# -------------------------
# Report builder functions
# -------------------------

def build_full_inventory_report(products, vendors):
    """Builds a full inventory report with product and vendor information. Params: products dictionary and vendors dictionary. Returns: A formatted report string."""
    lines = []
    lines.append("FULL INVENTORY REPORT")
    lines.append("=" * 60)

    if len(products) == 0:
        lines.append("No products are currently stored.")
        return "\n".join(lines)

    for product in products.values():
        vendor_name = "Unknown Vendor"
        if product.vendor_id in vendors:
            vendor_name = vendors[product.vendor_id].name

        status = "Active" if product.active else "Inactive"
        lines.append(f"{product.product_id} | {product.name}")
        lines.append(f"Category: {product.category}")
        lines.append(f"Quantity: {product.quantity}")
        lines.append(f"Reorder Level: {product.reorder_level}")
        lines.append(f"Unit Price: ${product.unit_price:.2f}")
        lines.append(f"Vendor: {vendor_name} ({product.vendor_id})")
        lines.append(f"Status: {status}")
        lines.append("-" * 60)

    return "\n".join(lines)


def build_low_stock_report(products, vendors):
    """Builds a report of products that are at or below reorder level. Params: products dictionary and vendors dictionary. Returns: A formatted report string."""
    lines = []
    lines.append("LOW-STOCK REPORT")
    lines.append("=" * 60)

    low_stock_items = []
    for product in products.values():
        if product.is_low_stock():
            low_stock_items.append(product)

    if len(low_stock_items) == 0:
        lines.append("No products are currently low on stock.")
        return "\n".join(lines)

    for product in low_stock_items:
        vendor_name = vendors[product.vendor_id].name if product.vendor_id in vendors else "Unknown Vendor"
        lines.append(f"{product.product_id} | {product.name}")
        lines.append(f"Current Quantity: {product.quantity}")
        lines.append(f"Reorder Level: {product.reorder_level}")
        lines.append(f"Suggested Reorder Quantity: {product.reorder_quantity}")
        lines.append(f"Vendor: {vendor_name}")
        lines.append("-" * 60)

    return "\n".join(lines)


def build_inventory_value_report(products):
    """Builds a report showing the total value of active inventory. Params: products dictionary. Returns: A formatted report string."""
    lines = []
    total_value = 0.0
    lines.append("TOTAL INVENTORY VALUE REPORT")
    lines.append("=" * 60)

    for product in products.values():
        if product.active:
            product_value = product.inventory_value()
            total_value += product_value
            lines.append(f"{product.product_id} | {product.name} | ${product_value:.2f}")

    lines.append("-" * 60)
    lines.append(f"Total Active Inventory Value: ${total_value:.2f}")
    return "\n".join(lines)


def build_open_purchase_orders_report(purchase_orders, vendors):
    """Builds a report showing all purchase orders that have not been received yet. Params: purchase_orders dictionary and vendors dictionary. Returns: A formatted report string."""
    lines = []
    lines.append("OPEN PURCHASE ORDERS REPORT")
    lines.append("=" * 60)

    # Keeping this as a normal loop makes the report logic easier to follow.
    open_orders = []
    for po in purchase_orders.values():
        if po.status != "Received":
            open_orders.append(po)

    if len(open_orders) == 0:
        lines.append("There are no open purchase orders.")
        return "\n".join(lines)

    for po in open_orders:
        vendor_name = vendors[po.vendor_id].name if po.vendor_id in vendors else "Unknown Vendor"
        lines.append(f"{po.po_number} | Vendor: {vendor_name} | Date: {po.date_created}")
        lines.append(f"Items Ordered: {len(po.items_ordered)}")
        lines.append(f"Total Cost: ${po.calculate_total():.2f}")
        lines.append("-" * 60)

    return "\n".join(lines)


def build_transaction_log_report(transaction_log):
    """Builds a report of inventory transactions, which is the extra feature for this project. Params: transaction_log list. Returns: A formatted report string."""
    lines = []
    lines.append("INVENTORY TRANSACTION LOG")
    lines.append("=" * 60)

    if len(transaction_log) == 0:
        lines.append("No transactions have been logged yet.")
        return "\n".join(lines)

    for transaction in transaction_log:
        lines.append(f"Date: {transaction.get('date', 'Unknown')}")
        lines.append(f"Product ID: {transaction.get('product_id', 'Unknown')}")
        lines.append(f"Action: {transaction.get('action', 'Unknown')}")
        lines.append(f"Quantity: {transaction.get('quantity', 0)}")
        lines.append(f"Notes: {transaction.get('notes', '')}")
        lines.append("-" * 60)

    return "\n".join(lines)


# -------------------------
# Report display function
# -------------------------

def print_report(report_text):
    """Prints a formatted report string to the console. Params: report_text string. Returns: None."""
    print("\n" + report_text)


def reports_menu(products, vendors, purchase_orders, transaction_log):
    """Displays the reports menu and runs the selected report. Params: products dictionary, vendors dictionary, purchase_orders dictionary, transaction_log list. Returns: None."""
    while True:
        print("\nReports Menu")
        print("1. Full Inventory Report")
        print("2. Low-Stock Report")
        print("3. Total Inventory Value Report")
        print("4. Open Purchase Orders Report")
        print("5. Transaction Log Report")
        print("6. Back")

        choice = input("Choose an option: ").strip()
        report_text = None

        if choice == "1":
            report_text = build_full_inventory_report(products, vendors)
        elif choice == "2":
            report_text = build_low_stock_report(products, vendors)
        elif choice == "3":
            report_text = build_inventory_value_report(products)
        elif choice == "4":
            report_text = build_open_purchase_orders_report(purchase_orders, vendors)
        elif choice == "5":
            report_text = build_transaction_log_report(transaction_log)
        elif choice == "6":
            break
        else:
            print("Invalid menu choice. Please choose 1 through 6.")

        if report_text is not None:
            print_report(report_text)
            print_divider()
