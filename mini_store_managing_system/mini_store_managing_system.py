class Product:
    def __init__(self, name, id, category, price, brand):

        if id is None:
            raise ValueError("Product ID cannot be None")

        if price < 0:
            raise ValueError("Product price cannot be negative")

        self.name = name
        self.id = id
        self.category = category
        self.price = price
        self.brand = brand

    def display_product(self):
        print(
            f"{self.category},"
            f"{self.brand},"
            f"{self.name},"
            f"{self.id},"
            f"{self.price}"
        )

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
            self.price = price

            # هنگام تغییر قیمت هم نباید اجازه بدهیم
            # قیمت جدید منفی باشد.
            if price < 0:
                raise ValueError("Product price cannot be negative!")

        if brand is not None:
            self.brand = brand


class Customer:
    def __init__(
    self,
    name,
    email,
    call_number: int,
    address,
    customer_id
    ):


        if customer_id is None:
            raise ValueError("Customer ID cannot be None!")

        self.name = name
        self.email = email
        self.call_number = call_number
        self.address = address
        self._customer_id = customer_id  # encapsulation customer id

    def display_customer(self):
        customer_info = {
            "Customer_id": self._customer_id,
            "Customer_name": self.name,
            "Email": self.email,
            "Call_number": self.call_number,
            "Address": self.address
        }

        for key, value in customer_info.items():
            print(f"{key}: {value}")


class Inventory:
    def __init__(self, product, quantity):


        if quantity < 0:
            raise ValueError("Inventory quantity cannot be negative!")

        self.product = product
        self.quantity = quantity

    def check_stock(self, requested_quantity):
        if requested_quantity <= 0:
            raise ValueError("Requested quantity must be greater than zero!")

        return self.quantity >= requested_quantity

    def add_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Stock quantity to ad must be greater than zero!")

        # اگر موجودی کافی نباشد، به‌جای اینکه
        # متد silently هیچ کاری نکند، خطا می‌دهیم.
        # اگر موجودی کافی نبود، هیچ اتفاقی نمی‌افتاد.
        # این خطرناک است،
        # چون برنامه ممکن است فکر کند
        # operation
        # انجام شده.
        if self.quantity < quantity:
            raise ValueError("Not enough stock!")

        self.quantity -= quantity


class Order:
    def __init__(self, customer, status="pending"):

    
        if customer is None:
            raise ValueError("Customer cannot be None!")

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

        valid_statuses = [
            "pending",
            "completed",
            "cancelled"
        ]

        if new_status in valid_statuses:
            raise ValueError(f"Invalid order status: {new_status}")

        if self.status != "pending":
            raise ValueError(
                f"Cannot change status from"
                f"{self.status} to {new_status}"
            )

        self.status = new_status


class OrderItem:
    def __init__(self, product, quantity):


        if product is None:
            raise ValueError("Product cannot be None!")

        if quantity <= 0:
            raise ValueError("Order quiantity must be greater than zero!")

        self.product = product
        self.quantity = quantity
        self.unit_price = product.price

    def calculate_price(self):
        return self.unit_price * self.quantity


class Store:
    def __init__(self):


        self.products = []
        self.customers = []
        self.inventories = []
        self.orders = []

    def find_product(self, product_id):

        for product in self.products:

            if product.id == product_id:
                return product

        return None

    def find_customer(self, customer_id):

        for customer in self.customers:

            if customer._customer_id == customer_id:
                return customer

        return None

    def find_inventory(self, product):

        for inventory in self.inventories:

            if inventory.product == product:
                return inventory

        return None

    def add_product(self, product):

        if product is None:
            raise ValueError("Product cannot be None")

        if self.find_product(product.id) is not None:
            raise ValueError(f"Product with ID {product.id} already exists")

        self.products.append(product)

    def add_customer(self, customer):

        if customer is None:
            raise ValueError("Customer cannot be None!")

        if self.find_customer(customer.customer_id) is not None:
            raise ValueError(
                f"Customer with ID "
                f"{customer.customer_id} already exists!"
            )

        self.customers.append(customer)

    def add_inventory(self, inventory):

        if inventory is None:
            raise ValueError("Inventory cannot be None!")

        if self.find_inventory(inventory.product) is not None:
            raise ValueError("Inventory for this product already exist!")

        self.inventories.append(inventory)

    def add_order(self, order):

        if order is None:
            raise ValueError("Order cannot be None!")

        self.orders.append(order)

    def create_order(self, customer_id, items):

        customer = self.find_customer(customer_id)

        if customer is None:
            return None

        if not items:
            raise ValueError("Order must contain at least one item!")

        validate_items = []

        for product_id, quantity in items:

            if quantity <= 0:
                raise ValueError("Order quantity must be greater than zero!")

            product = self.find_product(product_id)

            if product is None:
                return None

            inventory = self.find_inventory(product)

            if inventory is None:
                return None

            if not inventory.chech_stock(quantity):
                return None

            validate_items.append((product, inventory, quantity))

        order = Order(customer)

        for product, inventory, quantity in validate_items:

            order_item = OrderItem(product, quantity)
            order.add_item(order_item)
            inventory.remove_stock(quantity)
            order.update_status("completed")
            self.add_order(order)

            return order
        

# =========================

# Products

# =========================

product_1 = Product(
"Laptop",
101,
"Laptop",
178490,
"Lenovo"
)

product_2 = Product(
"Mouse",
102,
"Other",
185,
"A4Tech"
)

product_3 = Product(
"Keyboard",
103,
"Other",
650,
"A4Tech"
)

product_4 = Product(
"S22 Ultra",
104,
"Cell Phone",
78460,
"Samsung"
)

product_5 = Product(
"Glass",
105,
"Other",
88,
"Suzuki"
)

# =========================

# Customers

# =========================

customer_1 = Customer(
"Ali",
"[ali@gmail.com](mailto:ali@gmail.com)",
9121111111,
"Tehran",
1
)

customer_2 = Customer(
"Reza",
"[reza@gmail.com](mailto:reza@gmail.com)",
9122222222,
"Karaj",
2
)

customer_3 = Customer(
"Sara",
"[sara@gmail.com](mailto:sara@gmail.com)",
9123333333,
"Qazvin",
3
)

# =========================

# Inventories

# =========================

stock_1 = Inventory(product_1, 10)
stock_2 = Inventory(product_2, 20)
stock_3 = Inventory(product_3, 8)
stock_4 = Inventory(product_4, 5)
stock_5 = Inventory(product_5, 15)

# =========================

# Customer 1 - Order 1

# =========================

order_1 = Order(customer_1)

order_line_1 = OrderItem(product_1, 2)
order_line_2 = OrderItem(product_2, 3)

order_1.add_item(order_line_1)
order_1.add_item(order_line_2)

if stock_1.check_stock(order_line_1.quantity) and stock_2.check_stock(order_line_2.quantity):

    # stock_1.remove_stock(order_line_1.quantity)
    # stock_2.remove_stock(order_line_2.quantity)
    order_1.update_status("completed")


# =========================

# Customer 1 - Order 2

# =========================

order_2 = Order(customer_1)

order_line_3 = OrderItem(product_4, 1)
order_line_4 = OrderItem(product_5, 2)

order_2.add_item(order_line_3)
order_2.add_item(order_line_4)

if stock_4.check_stock(order_line_3.quantity) and stock_5.check_stock(order_line_4.quantity):

    # stock_4.remove_stock(order_line_3.quantity)
    # stock_5.remove_stock(order_line_4.quantity)
    order_2.update_status("completed")


# =========================

# Customer 2 - Order 3

# =========================

order_3 = Order(customer_2)

order_line_5 = OrderItem(product_1, 3)
order_line_6 = OrderItem(product_3, 2)

order_3.add_item(order_line_5)
order_3.add_item(order_line_6)

if stock_1.check_stock(order_line_5.quantity) and stock_3.check_stock(order_line_6.quantity):

    # stock_1.remove_stock(order_line_5.quantity)
    # stock_3.remove_stock(order_line_6.quantity)
    order_3.update_status("completed")


# =========================

# Customer 2 - Order 4

# =========================

order_4 = Order(customer_2)

order_line_7 = OrderItem(product_4, 5)

order_4.add_item(order_line_7)

if stock_4.check_stock(order_line_7.quantity):

    # stock_4.remove_stock(order_line_7.quantity)
    order_4.update_status("completed")


else:
    order_4.update_status("cancelled")


# =========================

# Customer 3 - Order 5

# =========================

order_5 = Order(customer_3)

order_line_8 = OrderItem(product_2, 4)
order_line_9 = OrderItem(product_3, 1)
order_line_10 = OrderItem(product_5, 3)

order_5.add_item(order_line_8)
order_5.add_item(order_line_9)
order_5.add_item(order_line_10)

if stock_2.check_stock(order_line_8.quantity) and stock_3.check_stock(order_line_9.quantity) and stock_5.check_stock(order_line_10.quantity):

    # stock_2.remove_stock(order_line_8.quantity)
    # stock_3.remove_stock(order_line_9.quantity)
    # stock_5.remove_stock(order_line_10.quantity)
    order_5.update_status("completed")


# =========================

# Final Results

# =========================

print("Order 1:", order_1.status)
print("Order 1 Total:", order_1.calculate_total())

print()

print("Order 2:", order_2.status)
print("Order 2 Total:", order_2.calculate_total())

print()

print("Order 3:", order_3.status)
print("Order 3 Total:", order_3.calculate_total())

print()

print("Order 4:", order_4.status)
print("Order 4 Total:", order_4.calculate_total())

print()

print("Order 5:", order_5.status)
print("Order 5 Total:", order_5.calculate_total())

print()

print("Stock 1:", stock_1.quantity)
print("Stock 2:", stock_2.quantity)
print("Stock 3:", stock_3.quantity)
print("Stock 4:", stock_4.quantity)
print("Stock 5:", stock_5.quantity)

# ==========================================

# Create Store

# ==========================================

store = Store()

# ==========================================

# Add Products

# ==========================================

store.add_product(product_1)
store.add_product(product_2)
store.add_product(product_3)
store.add_product(product_4)
store.add_product(product_5)

# ==========================================

# Add Customers

# ==========================================

store.add_customer(customer_1)
store.add_customer(customer_2)
store.add_customer(customer_3)

# ==========================================

# Add Inventories

# ==========================================

store.add_inventory(stock_1)
store.add_inventory(stock_2)
store.add_inventory(stock_3)
store.add_inventory(stock_4)
store.add_inventory(stock_5)

# ==========================================

# Test Store.create_order()

# ==========================================

# ساخت یک Store جدید

store = Store()

# اضافه کردن محصولات

store.add_product(product_1)
store.add_product(product_2)
store.add_product(product_3)
store.add_product(product_4)
store.add_product(product_5)

# اضافه کردن مشتری‌ها

store.add_customer(customer_1)
store.add_customer(customer_2)
store.add_customer(customer_3)

# اضافه کردن موجودی‌ها

store.add_inventory(stock_1)
store.add_inventory(stock_2)
store.add_inventory(stock_3)
store.add_inventory(stock_4)
store.add_inventory(stock_5)

# ==========================================

# Successful Order

# ==========================================

order_1 = store.create_order(
1,
[
(101, 2),
(102, 3),
(103, 1)
]
)

print("===== SUCCESSFUL ORDER =====")

# print("Order status:", order_1.status)
# print("Order total:", order_1.calculate_total())
# print("Number of items:", len(order_1.items))

print("Product 1 stock:", stock_1.quantity)
print("Product 2 stock:", stock_2.quantity)
print("Product 3 stock:", stock_3.quantity)

print("Orders in store:", len(store.orders))

# ==========================================

# Failed Order

# ==========================================

stock_4_before = stock_4.quantity

order_2 = store.create_order(
2,
[
(104, 100)
]
)

print()
print("===== FAILED ORDER =====")

print("Order result:", order_2)
print("Product 4 stock:", stock_4.quantity)
print("Stock changed:", stock_4.quantity != stock_4_before)

# ==========================================

# Invalid Customer

# ==========================================

order_3 = store.create_order(
999,
[
(101, 1)
]
)

print()
print("===== INVALID CUSTOMER =====")

print("Order result:", order_3)
print("Orders in store:", len(store.orders))
