# Inventory and Purchase Order System

**Name:** Jackson Hinks  
**Course Section:** - Python 54197

## Project Description

This project is a console-based Inventory and Purchase Order System made in Python. The business I used for the sample data is **Prairie Tech and Maker Supply**, which is basically a small local supply shop that sells 3D printing materials, basic IT parts, classroom electronics, networking equipment, office supplies, and repair tools.

The program is meant to act like a simple inventory workflow for that business. It lets the user keep track of products and vendors, create purchase orders, receive shipments, update stock counts, search and sort data, run reports, and save/load everything with JSON files. I split the program into several files so `main.py` is not doing every single thing, and so each file has a more specific purpose.

## Features

- Add, view, search, edit, and deactivate products
- Add, view, search, and edit vendors
- Create purchase orders for products from a selected vendor
- Add more than one product to a purchase order
- Calculate purchase order totals automatically
- View and search purchase orders
- Mark purchase orders as received
- Update inventory quantities when a shipment is received
- Prevent the same purchase order from being received twice
- Display low-stock products
- Search products by ID, name, category, and vendor
- Search vendors by ID and name/contact
- Search purchase orders by PO number
- Sort products by name, quantity, and price
- Sort purchase orders by date
- Save and load data using JSON
- Export a backup JSON file
- Generate reports

## Required Files

- `main.py` - Starts the program and contains the main menu system.
- `models.py` - Contains the `Product`, `Vendor`, and `PurchaseOrder` classes.
- `inventory_manager.py` - Contains most of the product, vendor, purchase order, search, sort, and receiving functions.
- `file_manager.py` - Handles JSON saving, loading, and backup exports.
- `reports.py` - Contains the report-building functions.
- `sample_data.json` - Contains the original sample dataset.
- `inventory_data.json` - Main working data file used by the program.
- `backup_inventory_data.json` - Extra JSON backup file created after testing.
- `reflection.md` - Reflection for the project.
- `code_explanation.txt` - Short written code defense answers.

The program first tries to load `inventory_data.json`. If that file is missing or empty, it tries `sample_data.json` so the project still has data to work with when it is first tested.

## How Data Is Stored

The program stores data in JSON files. Products, vendors, purchase orders, and the transaction log are converted into normal dictionaries and lists before saving. When the program starts again, the JSON data is read back in and converted back into `Product`, `Vendor`, and `PurchaseOrder` objects.

The main save file is `inventory_data.json`. The original sample data stays in `sample_data.json`, and the backup option creates or updates `backup_inventory_data.json`.

## Dataset

The project uses an original business scenario called Prairie Tech and Maker Supply. The sample data includes:

- 30 products
- 6 vendors
- 8 purchase orders
- 6 product categories

The product categories are:

- 3D Printing
- Computer Parts
- Networking
- Classroom Electronics
- Office Supplies
- Repair Tools

## Extra Feature Added

The extra feature I added is an **inventory transaction log**. When a product is added, deactivated, or received through a purchase order shipment, the program records that action in a simple log. The log saves the date, product ID, action, quantity, and a short note.

I added this because an inventory program should have at least some record of why stock changed. Without the log, a quantity could change and the user would only see the final number. This keeps a basic history without making the project overly complicated.

## Reports Included

- Full inventory report
- Low-stock report
- Total inventory value report
- Open purchase orders report
- Transaction log report

These reports print directly in the console so they are easy to test during the walkthrough.
