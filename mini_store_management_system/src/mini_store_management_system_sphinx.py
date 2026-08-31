"""Store management system implemented with Python classes and JSON persistence.

The module defines products, customers, inventory records, order items, orders,
store-level business operations, and persistence through a JSON file.
"""

import json


# =========================================================
# PRODUCT
# =========================================================

class Product:
    """Represent a product available in the store.
    
    A product contains identifying information, category, price, and brand.
    Its data can also be converted to and restored from a dictionary.
    """
    def __init__(self, name, id, category, price, brand):

        """Initialize a product.
        
        :param name: Product name.
        :type name: str
        :param id: Unique product identifier.
        :type id: int
        :param category: Product category.
        :type category: str
        :param price: Product price. Must not be negative.
        :type price: int or float
        :param brand: Product brand.
        :type brand: str
        :raises ValueError: If id is None or price is negative.
        """
        if id is None:
            raise ValueError("Product ID cannot be None!")

        if price < 0:
            raise ValueError("Product price cannot be negative!")

        self.name = name
        self.id = id
        self.category = category
        self.price = price
        self.brand = brand

    def display_product(self):

        """Display the product information in a readable format.
        """
        product_info = {
            "ID": self.id,
            "Category": self.category,
            "Name": self.name,
            "Brand": self.brand,
            "Price": self.price
        }

        for key, value in product_info.items():
            print(f"{key}: {value}")

    def change_product_info(
        self,
        name=None,
        category=None,
        price=None,
        brand=None
    ):

        """Update the product information that is provided.
        
        :param name: New product name, if provided.
        :type name: str or None
        :param category: New product category, if provided.
        :type category: str or None
        :param price: New product price, if provided.
        :type price: int or float or None
        :param brand: New product brand, if provided.
        :type brand: str or None
        :raises ValueError: If the provided price is negative.
        """
        if name is not None:
            self.name = name

        if category is not None:
            self.category = category

        if price is not None:

            if price < 0:
                raise ValueError(
                    "Product price cannot be negative!"
                )

            self.price = price

        if brand is not None:
            self.brand = brand

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        """Convert the product into a dictionary suitable for JSON serialization.
        
        :return: A dictionary containing the product attributes.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "brand": self.brand
        }

    @classmethod
    def from_dict(cls, data):

        """Create a product from serialized dictionary data.
        
        :param data: Dictionary containing product attributes.
        :type data: dict
        :return: A new Product instance.
        :rtype: Product
        """
        return cls(
            name=data["name"],
            id=data["id"],
            category=data["category"],
            price=data["price"],
            brand=data["brand"]
        )


# =========================================================
# CUSTOMER
# =========================================================

class Customer:
    """Represent a customer registered in the store.
    
    A customer has contact information and a customer ID that remains read-only
    through the public property after creation.
    """
    def __init__(
        self,
        name,
        email,
        call_number,
        address,
        customer_id
    ):

        """Initialize a customer.
        
        :param name: Customer name.
        :type name: str
        :param email: Customer email address.
        :type email: str
        :param call_number: Customer phone number.
        :type call_number: str
        :param address: Customer address.
        :type address: str
        :param customer_id: Unique customer identifier.
        :type customer_id: int
        :raises ValueError: If customer_id is None.
        """
        if customer_id is None:
            raise ValueError("Customer ID cannot be None!")

        self.name = name
        self.email = email
        self.call_number = call_number
        self.address = address

        # Customer ID represents the identity of the customer.
        # It should not be changed directly after creation!
        self._customer_id = customer_id

    @property
    def customer_id(self):
        """Return the customer's unique identifier.
        
        :return: The customer's ID.
        :rtype: int
        """
        return self._customer_id

    def change_customer_info(
        self,
        name=None,
        email=None,
        call_number=None,
        address=None
    ):

        """Update the customer information that is provided.
        
        :param name: New customer name, if provided.
        :type name: str or None
        :param email: New customer email, if provided.
        :type email: str or None
        :param call_number: New customer phone number, if provided.
        :type call_number: str or None
        :param address: New customer address, if provided.
        :type address: str or None
        """
        if name is not None:
            self.name = name

        if email is not None:
            self.email = email

        if call_number is not None:
            self.call_number = call_number

        if address is not None:
            self.address = address

    def display_customer(self):

        """Display the customer's information in a readable format.
        """
        customer_info = {
            "Customer ID": self.customer_id,
            "Customer Name": self.name,
            "Email": self.email,
            "Call Number": self.call_number,
            "Address": self.address
        }

        for key, value in customer_info.items():
            print(f"{key}: {value}")

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        """Convert the customer into a dictionary suitable for JSON serialization.
        
        :return: A dictionary containing the customer attributes.
        :rtype: dict
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "call_number": self.call_number,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):

        """Create a customer from serialized dictionary data.
        
        :param data: Dictionary containing customer attributes.
        :type data: dict
        :return: A new Customer instance.
        :rtype: Customer
        """
        return cls(
            name=data["name"],
            email=data["email"],
            call_number=data["call_number"],
            address=data["address"],
            customer_id=data["customer_id"]
        )


# =========================================================
# INVENTORY
# =========================================================

class Inventory:
    """Represent the stock quantity associated with a product.
    
    An inventory record belongs to one product and prevents invalid negative
    stock quantities.
    """
    def __init__(self, product, quantity):

        """Initialize an inventory record.
        
        :param product: Product associated with this inventory record.
        :type product: Product
        :param quantity: Initial stock quantity. Must not be negative.
        :type quantity: int
        :raises ValueError: If product is None or quantity is negative.
        """
        if product is None:
            raise ValueError("Product cannot be None!")

        if quantity < 0:
            raise ValueError(
                "Inventory quantity cannot be negative!"
            )

        self.product = product
        self.quantity = quantity

    def check_stock(self, requested_quantity):

        """Check whether enough stock is available.
        
        :param requested_quantity: Quantity requested by an operation.
        :type requested_quantity: int
        :return: True if the available stock is sufficient, otherwise False.
        :rtype: bool
        :raises ValueError: If requested_quantity is not greater than zero.
        """
        if requested_quantity <= 0:
            raise ValueError(
                "Requested quantity must be greater than zero!"
            )

        return self.quantity >= requested_quantity

    def add_stock(self, quantity):

        """Increase the available stock.
        
        :param quantity: Quantity to add.
        :type quantity: int
        :raises ValueError: If quantity is not greater than zero.
        """
        if quantity <= 0:
            raise ValueError(
                "Stock quantity to add must be greater than zero!"
            )

        self.quantity += quantity

    def remove_stock(self, quantity):

        """Decrease the available stock.
        
        :param quantity: Quantity to remove.
        :type quantity: int
        :raises ValueError: If quantity is not greater than zero or exceeds the available stock.
        """
        if quantity <= 0:
            raise ValueError(
                "Stock quantity to remove must be greater than zero!"
            )

        if self.quantity < quantity:
            raise ValueError("Not enough stock!")

        self.quantity -= quantity

    def set_stock(self, quantity):

        """Set the inventory quantity to an exact value.
        
        :param quantity: New stock quantity.
        :type quantity: int
        :raises ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError(
                "Stock quantity cannot be negative!"
            )

        self.quantity = quantity

    def display_inventory(self):

        """Display the product and its current stock quantity.
        """
        print(f"Product ID: {self.product.id}")
        print(f"Product Name: {self.product.name}")
        print(f"Quantity: {self.quantity}")

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        """Convert the inventory record into a dictionary for JSON serialization.
        
        :return: A dictionary containing the product ID and stock quantity.
        :rtype: dict
        """
        return {
            "product_id": self.product.id,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data, product):

        """Create an inventory record from serialized dictionary data.
        
        :param data: Dictionary containing inventory data.
        :type data: dict
        :param product: Product referenced by the inventory record.
        :type product: Product
        :return: A new Inventory instance.
        :rtype: Inventory
        """
        return cls(
            product=product,
            quantity=data["quantity"]
        )


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem:
    """Represent one product and quantity included in an order.
    
    The unit price is captured when the order item is created so historical
    orders are not affected by later product price changes.
    """
    def __init__(self, product, quantity):

        """Initialize an order item.
        
        :param product: Product being ordered.
        :type product: Product
        :param quantity: Number of units ordered. Must be greater than zero.
        :type quantity: int
        :raises ValueError: If product is None or quantity is not positive.
        """
        if product is None:
            raise ValueError("Product cannot be None!")

        if quantity <= 0:
            raise ValueError(
                "Order quantity must be greater than zero!"
            )

        self.product = product
        self.quantity = quantity

        # Store the price at the moment of the order.
        # Future Product price changes must not affect old order.
        self.unit_price = product.price

    def calculate_price(self):

        """Calculate the total price for this order item.
        
        :return: Unit price multiplied by the ordered quantity.
        :rtype: int or float
        """
        return self.unit_price * self.quantity

    def display_order_item(self):

        """Display the order item's details and calculated total.
        """
        print(f"Product ID: {self.product.id}")
        print(f"Product Name: {self.product.name}")
        print(f"Quantity: {self.quantity}")
        print(f"Unit Price: {self.unit_price}")
        print(f"Item Total: {self.calculate_price()}")

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        """Convert the order item into a dictionary for JSON serialization.
        
        :return: A dictionary containing the product ID, quantity, and historical unit price.
        :rtype: dict
        """
        return {
            "product_id": self.product.id,
            "quantity": self.quantity,
            "unit_price": self.unit_price
        }

    @classmethod
    def from_dict(cls, data, product):

        """Create an order item from serialized dictionary data.
        
        The serialized unit price is restored so the historical order price is preserved.
        
        :param data: Dictionary containing order-item data.
        :type data: dict
        :param product: Product referenced by the order item.
        :type product: Product
        :return: A new OrderItem instance with its historical unit price restored.
        :rtype: OrderItem
        """
        item = cls(
            product=product,
            quantity=data["quantity"]
        )

        # Restore historical price.
        item.unit_price = data["unit_price"]

        return item


# =========================================================
# ORDER
# =========================================================

class Order:
    """Represent a customer order and its lifecycle.
    
    Orders contain order items and support the statuses pending, completed,
    and cancelled. Completed and cancelled orders are final states.
    """
    VALID_STATUSES = {
        "pending",
        "completed",
        "cancelled"
    }

    def __init__(self, customer, status="pending"):

        """Initialize an order.
        
        :param customer: Customer who placed the order.
        :type customer: Customer
        :param status: Initial order status. Defaults to pending.
        :type status: str
        :raises ValueError: If customer is None or status is invalid.
        """
        if customer is None:
            raise ValueError("Customer cannot be None!")

        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid order status: {status}"
            )

        self.customer = customer
        self.status = status
        self.items = []

    def add_item(self, orderitem):

        """Add an order item to the order.
        
        :param orderitem: OrderItem to add.
        :type orderitem: OrderItem
        :raises ValueError: If orderitem is None.
        """
        if orderitem is None:
            raise ValueError("Order item cannot be None!")

        self.items.append(orderitem)

    def calculate_total(self):

        """Calculate the total price of all items in the order.
        
        :return: Sum of the calculated prices of all order items.
        :rtype: int or float
        """
        total = 0

        for item in self.items:
            total += item.calculate_price()

        return total

    def update_status(self, new_status):

        """Change the order status when the transition is valid.
        
        Only pending orders can transition to another status. Completed and cancelled
        orders are treated as final states.
        
        :param new_status: New order status.
        :type new_status: str
        :raises ValueError: If new_status is invalid or the current order is already final.
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid order status: {new_status}"
            )

        # Completed and cancelled are final states.
        if self.status != "pending":
            raise ValueError(
                f"Cannot change status from "
                f"{self.status} to {new_status}"
            )

        self.status = new_status

    def display_order(self):

        """Display the order, its items, status, and total price.
        """
        print(
            f"Customer ID: "
            f"{self.customer.customer_id}"
        )

        print(
            f"Customer Name: "
            f"{self.customer.name}"
        )

        print(f"Order Status: {self.status}")

        print("\nOrder Items:")
        print("-" * 30)

        for item in self.items:
            item.display_order_item()
            print("-" * 30)

        print(
            f"Order Total: "
            f"{self.calculate_total()}"
        )

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        """Convert the order into a dictionary for JSON serialization.
        
        :return: A dictionary containing the customer ID, status, and serialized items.
        :rtype: dict
        """
        return {
            "customer_id": self.customer.customer_id,
            "status": self.status,
            "items": [
                item.to_dict()
                for item in self.items
            ]
        }

    @classmethod
    def from_dict(cls, data, customer, products):

        """Create an order from serialized dictionary data.
        
        :param data: Dictionary containing order data.
        :type data: dict
        :param customer: Customer referenced by the order.
        :type customer: Customer
        :param products: Mapping of product IDs to Product instances.
        :type products: dict
        :return: A reconstructed Order instance.
        :rtype: Order
        :raises ValueError: If a referenced product does not exist.
        """
        order = cls(
            customer=customer,
            status=data["status"]
        )

        for item_data in data["items"]:

            product_id = item_data["product_id"]

            product = products.get(product_id)

            if product is None:
                raise ValueError(
                    f"Product with ID {product_id} "
                    f"referenced by order does not exist!"
                )

            order_item = OrderItem.from_dict(
                item_data,
                product
            )

            order.add_item(order_item)

        return order


# =========================================================
# STORE
# =========================================================

class Store:
    """Manage products, customers, inventory records, and orders.
    
    Store provides the main business operations of the application, including
    creation, lookup, update, removal, stock management, order processing,
    reporting, and conversion of the complete store state to and from dictionaries.
    """
    def __init__(self):

        """Initialize an empty store.
        """
        self.products = []
        self.customers = []
        self.inventories = []
        self.orders = []

    # =====================================================
    # PRODUCT MANAGEMENT
    # =====================================================

    def find_product(self, product_id):

        """Find a product by its ID.
        
        :param product_id: Product identifier to search for.
        :type product_id: int
        :return: The matching Product, or None if it does not exist.
        :rtype: Product or None
        """
        for product in self.products:

            if product.id == product_id:
                return product

        return None

    def add_product(self, product):

        """Register a product in the store.
        
        :param product: Product to add.
        :type product: Product
        :raises ValueError: If product is None or a product with the same ID exists.
        """
        if product is None:
            raise ValueError("Product cannot be None!")

        if self.find_product(product.id) is not None:
            raise ValueError(
                f"Product with ID {product.id} already exists!"
            )

        self.products.append(product)

    def update_product(
        self,
        product_id,
        name=None,
        category=None,
        price=None,
        brand=None
    ):

        """Update a registered product.
        
        :param product_id: ID of the product to update.
        :type product_id: int
        :param name: New product name, if provided.
        :type name: str or None
        :param category: New product category, if provided.
        :type category: str or None
        :param price: New product price, if provided.
        :type price: int or float or None
        :param brand: New product brand, if provided.
        :type brand: str or None
        :return: The updated Product, or None if the product does not exist.
        :rtype: Product or None
        :raises ValueError: If the new price is negative.
        """
        product = self.find_product(product_id)

        if product is None:
            return None

        product.change_product_info(
            name=name,
            category=category,
            price=price,
            brand=brand
        )

        return product

    def remove_product(self, product_id):

        """Remove a product when it has no remaining stock.
        
        :param product_id: ID of the product to remove.
        :type product_id: int
        :return: True if the product was removed, otherwise False.
        :rtype: bool
        :raises ValueError: If the product still has available stock.
        """
        product = self.find_product(product_id)

        if product is None:
            return False

        inventory = self.find_inventory(product)

        # Prevent removing a product while stock still exists.
        if inventory is not None and inventory.quantity > 0:
            raise ValueError(
                "Cannot remove product while stock is available!"
            )

        # Remove related empty inventory record.
        if inventory is not None:
            self.inventories.remove(inventory)

        self.products.remove(product)

        return True

    def display_products(self):

        """Display all registered products.
        """
        if not self.products:
            print("No products found!")
            return

        for product in self.products:
            product.display_product()
            print("-" * 30)

    # =====================================================
    # CUSTOMER MANAGEMENT
    # =====================================================

    def find_customer(self, customer_id):

        """Find a customer by customer ID.
        
        :param customer_id: Customer identifier to search for.
        :type customer_id: int
        :return: The matching Customer, or None if it does not exist.
        :rtype: Customer or None
        """
        for customer in self.customers:

            if customer.customer_id == customer_id:
                return customer

        return None

    def add_customer(self, customer):

        """Register a customer in the store.
        
        :param customer: Customer to add.
        :type customer: Customer
        :raises ValueError: If customer is None or a customer with the same ID exists.
        """
        if customer is None:
            raise ValueError("Customer cannot be None!")

        if self.find_customer(customer.customer_id) is not None:
            raise ValueError(
                f"Customer with ID "
                f"{customer.customer_id} already exists!"
            )

        self.customers.append(customer)

    def update_customer(
        self,
        customer_id,
        name=None,
        email=None,
        call_number=None,
        address=None
    ):

        """Update a registered customer's information.
        
        :param customer_id: ID of the customer to update.
        :type customer_id: int
        :param name: New customer name, if provided.
        :type name: str or None
        :param email: New customer email, if provided.
        :type email: str or None
        :param call_number: New customer phone number, if provided.
        :type call_number: str or None
        :param address: New customer address, if provided.
        :type address: str or None
        :return: The updated Customer, or None if the customer does not exist.
        :rtype: Customer or None
        """
        customer = self.find_customer(customer_id)

        if customer is None:
            return None

        customer.change_customer_info(
            name=name,
            email=email,
            call_number=call_number,
            address=address
        )

        return customer

    def remove_customer(self, customer_id):

        """Remove a customer who has no existing orders.
        
        :param customer_id: ID of the customer to remove.
        :type customer_id: int
        :return: True if the customer was removed, otherwise False.
        :rtype: bool
        :raises ValueError: If the customer has an existing order.
        """
        customer = self.find_customer(customer_id)

        if customer is None:
            return False

        # A customer with existing orders should not be removed.
        for order in self.orders:

            if order.customer == customer:
                raise ValueError(
                    "Cannot remove customer with existing orders!"
                )

        self.customers.remove(customer)

        return True

    def display_customers(self):

        """Display all registered customers.
        """
        if not self.customers:
            print("No customers found!")
            return

        for customer in self.customers:
            customer.display_customer()
            print("-" * 30)

    # =====================================================
    # INVENTORY MANAGEMENT
    # =====================================================

    def find_inventory(self, product):

        """Find the inventory record associated with a product.
        
        :param product: Product whose inventory should be found.
        :type product: Product
        :return: The matching Inventory, or None if no record exists.
        :rtype: Inventory or None
        """
        if product is None:
            return None

        for inventory in self.inventories:

            if inventory.product == product:
                return inventory

        return None

    def add_inventory(self, inventory):

        """Register an inventory record for an existing product.
        
        :param inventory: Inventory record to add.
        :type inventory: Inventory
        :raises ValueError: If inventory is None, its product is not registered,
            or an inventory record already exists for the product.
        """
        if inventory is None:
            raise ValueError("Inventory cannot be None!")

        # Inventory can only exist for a product
        # already registered in the store.
        if self.find_product(inventory.product.id) is None:
            raise ValueError(
                "Cannot add inventory for a product "
                "that does not exist in the store!"
            )

        if self.find_inventory(inventory.product) is not None:
            raise ValueError(
                "Inventory for this product already exists!"
            )

        self.inventories.append(inventory)

    def add_stock(self, product_id, quantity):

        """Increase stock for a registered product.
        
        :param product_id: ID of the product.
        :type product_id: int
        :param quantity: Quantity to add.
        :type quantity: int
        :return: The updated Inventory, or None if the product or inventory record does not exist.
        :rtype: Inventory or None
        """
        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.add_stock(quantity)

        return inventory

    def remove_stock(self, product_id, quantity):

        """Decrease stock for a registered product.
        
        :param product_id: ID of the product.
        :type product_id: int
        :param quantity: Quantity to remove.
        :type quantity: int
        :return: The updated Inventory, or None if the product or inventory record does not exist.
        :rtype: Inventory or None
        :raises ValueError: If the quantity is invalid or exceeds available stock.
        """
        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.remove_stock(quantity)

        return inventory

    def set_stock(self, product_id, quantity):

        """Set the stock quantity for a registered product.
        
        :param product_id: ID of the product.
        :type product_id: int
        :param quantity: New stock quantity.
        :type quantity: int
        :return: The updated Inventory, or None if the product or inventory record does not exist.
        :rtype: Inventory or None
        :raises ValueError: If quantity is negative.
        """
        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.set_stock(quantity)

        return inventory

    def display_inventory(self):

        """Display all inventory records.
        """
        if not self.inventories:
            print("No inventory found!")
            return

        for inventory in self.inventories:
            inventory.display_inventory()
            print("-" * 30)

    def low_stock(self, threshold=5):

        """Return inventory records whose stock is low but not zero.
        
        :param threshold: Maximum quantity considered low stock.
        :type threshold: int
        :return: A list of Inventory records with quantities between 1 and threshold.
        :rtype: list
        :raises ValueError: If threshold is negative.
        """
        if threshold < 0:
            raise ValueError(
                "Stock threshold cannot be negative!"
            )

        low_stock_products = []

        for inventory in self.inventories:

            if 0 < inventory.quantity <= threshold:
                low_stock_products.append(inventory)

        return low_stock_products

    def out_of_stock(self):

        """Return inventory records whose stock quantity is zero.
        
        :return: A list of out-of-stock Inventory records.
        :rtype: list
        """
        out_of_stock_products = []

        for inventory in self.inventories:

            if inventory.quantity == 0:
                out_of_stock_products.append(inventory)

        return out_of_stock_products

    # =====================================================
    # ORDER MANAGEMENT
    # =====================================================

    def add_order(self, order):

        """Register an order in the store.
        
        :param order: Order to add.
        :type order: Order
        :raises ValueError: If order is None.
        """
        if order is None:
            raise ValueError("Order cannot be None!")

        self.orders.append(order)

    def find_order(self, order_index):

        """Find an order by its zero-based index.
        
        :param order_index: Index of the order in the store.
        :type order_index: int
        :return: The matching Order, or None if the index is invalid.
        :rtype: Order or None
        """
        if order_index < 0 or order_index >= len(self.orders):
            return None

        return self.orders[order_index]

    def display_orders(self):

        """Display all registered orders.
        """
        if not self.orders:
            print("No orders found!")
            return

        for index, order in enumerate(self.orders):

            print(f"Order #{index + 1}")
            order.display_order()
            print("=" * 40)

    def get_orders_by_status(self, status):

        """Return all orders with the requested status.
        
        :param status: Order status to filter by.
        :type status: str
        :return: A list of matching Order instances.
        :rtype: list
        :raises ValueError: If status is invalid.
        """
        if status not in Order.VALID_STATUSES:
            raise ValueError(
                f"Invalid order status: {status}"
            )

        result = []

        for order in self.orders:

            if order.status == status:
                result.append(order)

        return result

    def cancel_order(self, order_index):

        """Cancel an existing order.
        
        :param order_index: Zero-based index of the order to cancel.
        :type order_index: int
        :return: The cancelled Order, or None if the index is invalid.
        :rtype: Order or None
        :raises ValueError: If the order cannot transition to cancelled.
        """
        order = self.find_order(order_index)

        if order is None:
            return None

        order.update_status("cancelled")

        return order

    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(self, customer_id, items):

        # -------------------------------------------------
        # Step 1: Find customer
        # -------------------------------------------------

        """Create, validate, and complete a customer order.
        
        The method validates the customer, requested items, referenced products,
        inventory records, and total required stock before changing inventory.
        After validation, it creates the order, captures item prices, removes stock,
        marks the order as completed, and stores it.
        
        :param customer_id: ID of the customer placing the order.
        :type customer_id: int
        :param items: List of (product_id, quantity) pairs.
        :type items: list
        :return: The completed Order, or None if the customer, product, or inventory
            referenced by the request does not exist.
        :rtype: Order or None
        :raises ValueError: If items are empty or contain invalid quantities, or if
            requested stock is insufficient.
        """
        customer = self.find_customer(customer_id)

        if customer is None:
            return None

        # -------------------------------------------------
        # Step 2: Validate order
        # -------------------------------------------------

        if not items:
            raise ValueError(
                "Order must contain at least one item!"
            )

        # We first calculate the total requested quantity
        # for every product.
        #
        # This is important when the same product appears
        # more than once in the order.
        required_quantities = {}

        for product_id, quantity in items:

            if quantity <= 0:
                raise ValueError(
                    "Order quantity must be greater than zero!"
                )

            product = self.find_product(product_id)

            if product is None:
                return None

            inventory = self.find_inventory(product)

            if inventory is None:
                return None

            required_quantities[product_id] = (
                required_quantities.get(product_id, 0)
                + quantity
            )

        # -------------------------------------------------
        # Step 3: Validate TOTAL stock
        # -------------------------------------------------

        validated_items = []

        for product_id, total_quantity in required_quantities.items():

            product = self.find_product(product_id)
            inventory = self.find_inventory(product)

            if not inventory.check_stock(total_quantity):
                return None

            validated_items.append(
                (product, inventory, total_quantity)
            )

        # -------------------------------------------------
        # Step 4: Create order
        # -------------------------------------------------

        order = Order(customer)

        # -------------------------------------------------
        # Step 5: Add items
        # -------------------------------------------------

        for product_id, quantity in items:

            product = self.find_product(product_id)

            order_item = OrderItem(
                product,
                quantity
            )

            order.add_item(order_item)

        # -------------------------------------------------
        # Step 6: Remove stock
        # -------------------------------------------------

        for product, inventory, total_quantity in validated_items:

            inventory.remove_stock(total_quantity)

        # -------------------------------------------------
        # Step 7: Complete order
        # -------------------------------------------------

        order.update_status("completed")

        # -------------------------------------------------
        # Step 8: Save order in Store
        # -------------------------------------------------

        self.add_order(order)

        return order

    # =====================================================
    # REPORTS
    # =====================================================

    def total_sales(self):

        """Calculate sales from all completed orders.
        
        :return: Total value of completed orders.
        :rtype: int or float
        """
        total = 0

        for order in self.orders:

            if order.status == "completed":
                total += order.calculate_total()

        return total

    def number_of_orders(self):

        """Return the total number of orders.
        
        :return: Number of orders registered in the store.
        :rtype: int
        """
        return len(self.orders)

    def number_of_completed_orders(self):

        """Return the number of completed orders.
        
        :return: Number of orders with completed status.
        :rtype: int
        """
        count = 0

        for order in self.orders:

            if order.status == "completed":
                count += 1

        return count

    def number_of_cancelled_orders(self):

        """Return the number of cancelled orders.
        
        :return: Number of orders with cancelled status.
        :rtype: int
        """
        count = 0

        for order in self.orders:

            if order.status == "cancelled":
                count += 1

        return count

    def number_of_pending_orders(self):

        """Return the number of pending orders.
        
        :return: Number of orders with pending status.
        :rtype: int
        """
        count = 0

        for order in self.orders:

            if order.status == "pending":
                count += 1

        return count

    def display_sales_report(self):

        """Display a summary of store sales and order counts.
        """
        print("=" * 40)
        print("SALES REPORT")
        print("=" * 40)

        print(
            f"Total Orders: "
            f"{self.number_of_orders()}"
        )

        print(
            f"Completed Orders: "
            f"{self.number_of_completed_orders()}"
        )

        print(
            f"Cancelled Orders: "
            f"{self.number_of_cancelled_orders()}"
        )

        print(
            f"Pending Orders: "
            f"{self.number_of_pending_orders()}"
        )

        print(
            f"Total Sales: "
            f"{self.total_sales()}"
        )

    def display_low_stock_report(self, threshold=5):

        """Display products whose stock is below the given threshold.
        
        :param threshold: Maximum quantity considered low stock.
        :type threshold: int
        :raises ValueError: If threshold is negative.
        """
        low_stock_products = self.low_stock(threshold)

        print("=" * 40)
        print("LOW STOCK REPORT")
        print("=" * 40)

        if not low_stock_products:
            print("No low-stock products found!")
            return

        for inventory in low_stock_products:

            print(
                f"{inventory.product.name}: "
                f"{inventory.quantity}"
            )

    def display_out_of_stock_report(self):

        """Display products that currently have no stock.
        """
        out_of_stock_products = self.out_of_stock()

        print("=" * 40)
        print("OUT OF STOCK REPORT")
        print("=" * 40)

        if not out_of_stock_products:
            print("No out-of-stock products found!")
            return

        for inventory in out_of_stock_products:

            print(
                f"{inventory.product.name}: "
                f"{inventory.quantity}"
            )

    # =====================================================
    # JSON SERIALIZATION
    # =====================================================

    def to_dict(self):

        """Convert the complete store state into a dictionary.
        
        :return: A dictionary containing serialized products, customers, inventory records,
            and orders.
        :rtype: dict
        """
        return {
            "products": [
                product.to_dict()
                for product in self.products
            ],

            "customers": [
                customer.to_dict()
                for customer in self.customers
            ],

            "inventories": [
                inventory.to_dict()
                for inventory in self.inventories
            ],

            "orders": [
                order.to_dict()
                for order in self.orders
            ]
        }

    @classmethod
    def from_dict(cls, data):

        """Reconstruct a Store from serialized dictionary data.
        
        Products and customers are restored first so inventory and orders can resolve
        their references by ID.
        
        :param data: Dictionary containing serialized store data.
        :type data: dict
        :return: A reconstructed Store instance.
        :rtype: Store
        :raises ValueError: If inventory or order data references a missing product
            or customer.
        """
        store = cls()

        # -------------------------------------------------
        # 1. Restore Products
        # -------------------------------------------------

        product_map = {}

        for product_data in data.get("products", []):

            product = Product.from_dict(product_data)

            store.add_product(product)

            product_map[product.id] = product

        # -------------------------------------------------
        # 2. Restore Customers
        # -------------------------------------------------

        customer_map = {}

        for customer_data in data.get("customers", []):

            customer = Customer.from_dict(customer_data)

            store.add_customer(customer)

            customer_map[customer.customer_id] = customer

        # -------------------------------------------------
        # 3. Restore Inventory
        # -------------------------------------------------

        for inventory_data in data.get("inventories", []):

            product_id = inventory_data["product_id"]

            product = product_map.get(product_id)

            if product is None:
                raise ValueError(
                    f"Product with ID {product_id} "
                    f"referenced by inventory does not exist!"
                )

            inventory = Inventory.from_dict(
                inventory_data,
                product
            )

            store.add_inventory(inventory)

        # -------------------------------------------------
        # 4. Restore Orders
        # -------------------------------------------------

        for order_data in data.get("orders", []):

            customer_id = order_data["customer_id"]

            customer = customer_map.get(customer_id)

            if customer is None:
                raise ValueError(
                    f"Customer with ID {customer_id} "
                    f"referenced by order does not exist!"
                )

            order = Order.from_dict(
                order_data,
                customer,
                product_map
            )

            store.add_order(order)

        return store


# =========================================================
# STORE PERSISTENCE
# =========================================================

class StorePersistence:

    """Save and load Store data using a JSON file.
    """
    def __init__(self, filename="store.json"):

        """Initialize the persistence handler.
        
        :param filename: Path of the JSON file used for persistence.
        :type filename: str
        """
        self.filename = filename

    def save(self, store):

        """Serialize and save a store to the configured JSON file.
        
        :param store: Store instance to save.
        :type store: Store
        :raises ValueError: If store is None.
        :raises OSError: If the file cannot be written.
        """
        if store is None:
            raise ValueError("Store cannot be None!")

        data = store.to_dict()

        try:

            with open(
                self.filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:

            raise OSError(
                f"Could not save store data: {error}"
            ) from error

    def load(self):

        """Load a store from the configured JSON file.
        
        :return: A reconstructed Store. If the file does not exist, an empty Store is returned.
        :rtype: Store
        :raises ValueError: If the JSON content is invalid or does not have the expected
            root structure.
        :raises OSError: If the file cannot be read.
        """
        try:

            with open(
                self.filename,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except FileNotFoundError:

            return Store()

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid JSON file: {error}"
            ) from error

        except OSError as error:

            raise OSError(
                f"Could not load store data: {error}"
            ) from error

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid store data: root must be a JSON object!"
            )

        return Store.from_dict(data)


# =========================================================
# EXAMPLE / MANUAL DEMONSTRATION
# =========================================================

if __name__ == "__main__":

    store = Store()

    product = Product(
        "Mouse",
        101,
        "Accessory",
        500000,
        "Logitech"
    )

    store.add_product(product)

    inventory = Inventory(product, 10)
    store.add_inventory(inventory)

    customer = Customer(
        "Ali",
        "ali@example.com",
        "09120000000",
        "Tehran",
        1
    )

    store.add_customer(customer)

    order = store.create_order(
        customer_id=1,
        items=[
            (101, 2)
        ]
    )

    persistence = StorePersistence("store.json")

    persistence.save(store)

    print("Store saved successfully!")

    loaded_store = persistence.load()

    print("\nLoaded store:")

    loaded_store.display_products()
    loaded_store.display_customers()
    loaded_store.display_inventory()
    loaded_store.display_orders()

    print(
        f"\nTotal sales: "
        f"{loaded_store.total_sales()}"
    )