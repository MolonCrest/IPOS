# Project Reflection

## What part of the project was hardest?

The hardest part of this project was making all of the pieces connect together without turning it into one giant file. Adding a product or adding a vendor was not too difficult by itself, but the harder part was making the purchase order system actually use those products and vendors in a useful way. The program had to know which vendor a product belongs to, which products are on a purchase order, and what should happen to inventory when an order is received. I had to slow down and decide how the data should be stored before writing too much of the menu code, because if the data structure was bad then everything after that would have been annoying to fix. I ended up using dictionaries for products, vendors, and purchase orders because it made the most sense for searching by ID.

## What bug took the longest to solve?

One bug that took the longest to handle was duplicate receiving for purchase orders. If the user marked the same purchase order as received twice, then the inventory quantity would get added twice, which would make the inventory numbers wrong. That is the kind of bug that would not always be obvious right away, because the program would still run, but the data would be incorrect. I fixed it by checking the purchase order status before changing any product quantities. If the PO is already marked as `Received`, the program prints a message and stops before it updates inventory again.

## How did you organize your code across multiple files?

I organized the project by giving each file one main job. `main.py` mostly just runs the menus and sends the dictionaries into the right functions. `models.py` stores the three custom classes, which are `Product`, `Vendor`, and `PurchaseOrder`. `inventory_manager.py` has most of the actual program actions, like adding products, editing vendors, creating purchase orders, receiving shipments, searching, and sorting. `file_manager.py` handles the JSON saving and loading so that code is not mixed in with the menu code. `reports.py` builds the reports that print in the console. This made the project easier to work with because I could usually tell which file I needed based on what part of the program I was changing.

## How does your save/load system work?

The save and load system uses JSON. Since custom Python objects do not save cleanly to JSON on their own, each class has a `to_dict()` method that turns the object into a normal dictionary. The program puts those dictionaries into lists and saves them into `inventory_data.json` with `json.dump()`. When the program starts, it reads the file with `json.load()` and then uses the `from_dict()` methods in the classes to rebuild the objects. If the normal save file is missing or empty, the program tries to load `sample_data.json` instead, which makes testing the project easier from a fresh folder.

## What would you improve if you had another week?

If I had another week, I would improve the menus and make the purchase order process more realistic. One thing I would add is partial shipment receiving, because in a real business, sometimes a vendor only sends part of an order at first. I would also add better report filters, like showing only one vendor's purchase orders or only products under a certain stock amount. Another thing I would improve is vendor validation, since the current program checks for blank fields but does not fully check whether an email address or phone number is formatted correctly. I would also probably add a safer archive option for old purchase orders, because products can already be deactivated, but old purchase orders just stay in the system. Overall, the project works as a console inventory program, but the next step would be making it feel smoother and closer to a real workplace tool.

## Extra feature reflection

The extra feature I added was the inventory transaction log. I chose this because it fits the project pretty naturally and gives the inventory changes more context. Without a log, the user might see that a product quantity changed but not know why it changed. The transaction log records actions like receiving a shipment, adding a product, or deactivating a product, along with the date, product ID, quantity, and notes. It is not a full audit system, but it adds another useful layer to the project and makes the program feel a little less like just a menu demo.
