# Jackson Hinks
# Inventory and Purchase Order System
# models.py
# This file stores the custom classes used by the program.
# The classes mainly hold data and give the save/load system a clean structure.


class Product:
    def __init__(self, product_id, name, category, quantity, reorder_level, reorder_quantity, unit_price, vendor_id, active=True):
        """Creates a Product object. Params: product_id, name, category, quantity, reorder_level, reorder_quantity, unit_price, vendor_id, active. Returns: None."""
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = int(quantity)
        self.reorder_level = int(reorder_level)
        self.reorder_quantity = int(reorder_quantity)
        self.unit_price = float(unit_price)
        self.vendor_id = vendor_id
        self.active = bool(active)

    def is_low_stock(self):
        """Checks if the product is at or below its reorder level. Params: None. Returns: True if stock is low, otherwise False."""
        return self.active and self.quantity <= self.reorder_level

    def inventory_value(self):
        """Calculates the current value of this product's stock. Params: None. Returns: The product quantity multiplied by unit price."""
        return self.quantity * self.unit_price

    def add_stock(self, amount):
        """Adds a positive quantity to the product's current stock. Params: amount, which is the number of units to add. Returns: None."""
        self.quantity += int(amount)

    def to_dict(self):
        """Converts the Product object into a dictionary for JSON saving. Params: None. Returns: A dictionary version of the product."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "reorder_quantity": self.reorder_quantity,
            "unit_price": self.unit_price,
            "vendor_id": self.vendor_id,
            "active": self.active
        }

    @staticmethod
    def from_dict(data):
        """Creates a Product object from a dictionary loaded from JSON. Params: data, which is a dictionary containing product information. Returns: A Product object."""
        return Product(
            data["product_id"],
            data["name"],
            data["category"],
            data["quantity"],
            data["reorder_level"],
            data["reorder_quantity"],
            data["unit_price"],
            data["vendor_id"],
            data.get("active", True)
        )

    def display_lines(self):
        """Builds readable display lines for one product. Params: None. Returns: A list of strings."""
        status = "Active" if self.active else "Inactive"
        return [
            f"Product ID: {self.product_id}",
            f"Name: {self.name}",
            f"Category: {self.category}",
            f"Quantity: {self.quantity}",
            f"Reorder Level: {self.reorder_level}",
            f"Reorder Quantity: {self.reorder_quantity}",
            f"Unit Price: ${self.unit_price:.2f}",
            f"Vendor ID: {self.vendor_id}",
            f"Status: {status}"
        ]


class Vendor:
    def __init__(self, vendor_id, name, contact_name, phone, email, address):
        """Creates a Vendor object. Params: vendor_id, name, contact_name, phone, email, address. Returns: None."""
        self.vendor_id = vendor_id
        self.name = name
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        """Converts the Vendor object into a dictionary for JSON saving. Params: None. Returns: A dictionary version of the vendor."""
        return {
            "vendor_id": self.vendor_id,
            "name": self.name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        """Creates a Vendor object from a dictionary loaded from JSON. Params: data, which is a dictionary containing vendor information. Returns: A Vendor object."""
        return Vendor(
            data["vendor_id"],
            data["name"],
            data["contact_name"],
            data["phone"],
            data["email"],
            data["address"]
        )

    def display_lines(self):
        """Builds readable display lines for one vendor. Params: None. Returns: A list of strings."""
        return [
            f"Vendor ID: {self.vendor_id}",
            f"Vendor Name: {self.name}",
            f"Contact: {self.contact_name}",
            f"Phone: {self.phone}",
            f"Email: {self.email}",
            f"Address: {self.address}"
        ]


class PurchaseOrder:
    def __init__(self, po_number, vendor_id, date_created, items_ordered, status="Open"):
        """Creates a PurchaseOrder object. Params: po_number, vendor_id, date_created, items_ordered, status. Returns: None."""
        self.po_number = po_number
        self.vendor_id = vendor_id
        self.date_created = date_created
        self.items_ordered = items_ordered
        self.status = status
        self.total_cost = self.calculate_total()

    def calculate_total(self):
        """Calculates the total cost of all line items on the purchase order. Params: None. Returns: The total cost as a float."""
        total = 0.0

        # Each item is stored as a small dictionary, so this multiplies quantity by unit price.
        for item in self.items_ordered:
            quantity = int(item["quantity"])
            unit_price = float(item["unit_price"])
            total += quantity * unit_price

        return total

    def mark_received(self):
        """Changes the purchase order status to Received. Params: None. Returns: None."""
        self.status = "Received"

    def to_dict(self):
        """Converts the PurchaseOrder object into a dictionary for JSON saving. Params: None. Returns: A dictionary version of the purchase order."""
        return {
            "po_number": self.po_number,
            "vendor_id": self.vendor_id,
            "date_created": self.date_created,
            "items_ordered": self.items_ordered,
            "total_cost": self.calculate_total(),
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Creates a PurchaseOrder object from a dictionary loaded from JSON. Params: data, which is a dictionary containing purchase order information. Returns: A PurchaseOrder object."""
        po = PurchaseOrder(
            data["po_number"],
            data["vendor_id"],
            data["date_created"],
            data["items_ordered"],
            data.get("status", "Open")
        )
        po.total_cost = float(data.get("total_cost", po.calculate_total()))
        return po

    def display_lines(self):
        """Builds readable display lines for one purchase order. Params: None. Returns: A list of strings."""
        lines = [
            f"PO Number: {self.po_number}",
            f"Vendor ID: {self.vendor_id}",
            f"Date Created: {self.date_created}",
            f"Status: {self.status}",
            "Items Ordered:"
        ]

        for item in self.items_ordered:
            quantity = int(item["quantity"])
            unit_price = float(item["unit_price"])
            line_total = quantity * unit_price

            line = (
                f"  - {item['product_id']} | Qty: {quantity} | "
                f"Unit Price: ${unit_price:.2f} | "
                f"Line Total: ${line_total:.2f}"
            )
            lines.append(line)

        lines.append(f"Total Cost: ${self.calculate_total():.2f}")
        return lines
