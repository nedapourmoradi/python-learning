import json


# =========================================================
# PRODUCT
# =========================================================

class Product:
    def __init__(self, name, id, category, price, brand):

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

        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "brand": self.brand
        }

    @classmethod
    def from_dict(cls, data):

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
    def __init__(
        self,
        name,
        email,
        call_number,
        address,
        customer_id
    ):

        if customer_id is None:
            raise ValueError("Customer ID cannot be None!")

        self.name = name
        self.email = email
        self.call_number = call_number
        self.address = address

        # Customer ID represents the identity of the customer.
        # It should not be changed directly after creation.
        self._customer_id = customer_id

    @property
    def customer_id(self):
        return self._customer_id

    def change_customer_info(
        self,
        name=None,
        email=None,
        call_number=None,
        address=None
    ):

        if name is not None:
            self.name = name

        if email is not None:
            self.email = email

        if call_number is not None:
            self.call_number = call_number

        if address is not None:
            self.address = address

    def display_customer(self):

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

        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "call_number": self.call_number,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):

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
    def __init__(self, product, quantity):

        if product is None:
            raise ValueError("Product cannot be None!")

        if quantity < 0:
            raise ValueError(
                "Inventory quantity cannot be negative!"
            )

        self.product = product
        self.quantity = quantity

    def check_stock(self, requested_quantity):

        if requested_quantity <= 0:
            raise ValueError(
                "Requested quantity must be greater than zero!"
            )

        return self.quantity >= requested_quantity

    def add_stock(self, quantity):

        if quantity <= 0:
            raise ValueError(
                "Stock quantity to add must be greater than zero!"
            )

        self.quantity += quantity

    def remove_stock(self, quantity):

        if quantity <= 0:
            raise ValueError(
                "Stock quantity to remove must be greater than zero!"
            )

        if self.quantity < quantity:
            raise ValueError("Not enough stock!")

        self.quantity -= quantity

    def set_stock(self, quantity):

        if quantity < 0:
            raise ValueError(
                "Stock quantity cannot be negative!"
            )

        self.quantity = quantity

    def display_inventory(self):

        print(f"Product ID: {self.product.id}")
        print(f"Product Name: {self.product.name}")
        print(f"Quantity: {self.quantity}")

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        return {
            "product_id": self.product.id,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data, product):

        return cls(
            product=product,
            quantity=data["quantity"]
        )


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem:
    def __init__(self, product, quantity):

        if product is None:
            raise ValueError("Product cannot be None!")

        if quantity <= 0:
            raise ValueError(
                "Order quantity must be greater than zero!"
            )

        self.product = product
        self.quantity = quantity

        # Store the price at the moment of the order.
        # Future Product price changes must not affect
        # old orders.
        self.unit_price = product.price

    def calculate_price(self):

        return self.unit_price * self.quantity

    def display_order_item(self):

        print(f"Product ID: {self.product.id}")
        print(f"Product Name: {self.product.name}")
        print(f"Quantity: {self.quantity}")
        print(f"Unit Price: {self.unit_price}")
        print(f"Item Total: {self.calculate_price()}")

    # -----------------------------------------------------
    # JSON SERIALIZATION
    # -----------------------------------------------------

    def to_dict(self):

        return {
            "product_id": self.product.id,
            "quantity": self.quantity,
            "unit_price": self.unit_price
        }

    @classmethod
    def from_dict(cls, data, product):

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
    VALID_STATUSES = {
        "pending",
        "completed",
        "cancelled"
    }

    def __init__(self, customer, status="pending"):

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

        if orderitem is None:
            raise ValueError("Order item cannot be None!")

        self.items.append(orderitem)

    def calculate_total(self):

        total = 0

        for item in self.items:
            total += item.calculate_price()

        return total

    def update_status(self, new_status):

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
    def __init__(self):

        self.products = []
        self.customers = []
        self.inventories = []
        self.orders = []

    # =====================================================
    # PRODUCT MANAGEMENT
    # =====================================================

    def find_product(self, product_id):

        for product in self.products:

            if product.id == product_id:
                return product

        return None

    def add_product(self, product):

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

        for customer in self.customers:

            if customer.customer_id == customer_id:
                return customer

        return None

    def add_customer(self, customer):

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

        if product is None:
            return None

        for inventory in self.inventories:

            if inventory.product == product:
                return inventory

        return None

    def add_inventory(self, inventory):

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

        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.add_stock(quantity)

        return inventory

    def remove_stock(self, product_id, quantity):

        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.remove_stock(quantity)

        return inventory

    def set_stock(self, product_id, quantity):

        product = self.find_product(product_id)

        if product is None:
            return None

        inventory = self.find_inventory(product)

        if inventory is None:
            return None

        inventory.set_stock(quantity)

        return inventory

    def display_inventory(self):

        if not self.inventories:
            print("No inventory found!")
            return

        for inventory in self.inventories:
            inventory.display_inventory()
            print("-" * 30)

    def low_stock(self, threshold=5):

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

        out_of_stock_products = []

        for inventory in self.inventories:

            if inventory.quantity == 0:
                out_of_stock_products.append(inventory)

        return out_of_stock_products

    # =====================================================
    # ORDER MANAGEMENT
    # =====================================================

    def add_order(self, order):

        if order is None:
            raise ValueError("Order cannot be None!")

        self.orders.append(order)

    def find_order(self, order_index):

        if order_index < 0 or order_index >= len(self.orders):
            return None

        return self.orders[order_index]

    def display_orders(self):

        if not self.orders:
            print("No orders found!")
            return

        for index, order in enumerate(self.orders):

            print(f"Order #{index + 1}")
            order.display_order()
            print("=" * 40)

    def get_orders_by_status(self, status):

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

        total = 0

        for order in self.orders:

            if order.status == "completed":
                total += order.calculate_total()

        return total

    def number_of_orders(self):

        return len(self.orders)

    def number_of_completed_orders(self):

        count = 0

        for order in self.orders:

            if order.status == "completed":
                count += 1

        return count

    def number_of_cancelled_orders(self):

        count = 0

        for order in self.orders:

            if order.status == "cancelled":
                count += 1

        return count

    def number_of_pending_orders(self):

        count = 0

        for order in self.orders:

            if order.status == "pending":
                count += 1

        return count

    def display_sales_report(self):

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

    def __init__(self, filename="store.json"):

        self.filename = filename

    def save(self, store):

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