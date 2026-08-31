import json
import os
import tempfile
import unittest

from src.mini_store_management_system import (
    Product,
    Customer,
    Inventory,
    OrderItem,
    Order,
    Store,
    StorePersistence
)


# =========================================================
# PRODUCT TESTS
# =========================================================

class TestProduct(unittest.TestCase):

    def test_create_product(self):

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.id, 101)
        self.assertEqual(product.category, "Accessory")
        self.assertEqual(product.price, 500000)
        self.assertEqual(product.brand, "Logitech")

    def test_product_id_cannot_be_none(self):

        with self.assertRaises(ValueError):

            Product(
                "Mouse",
                None,
                "Accessory",
                500000,
                "Logitech"
            )

    def test_product_price_cannot_be_negative(self):

        with self.assertRaises(ValueError):

            Product(
                "Mouse",
                101,
                "Accessory",
                -100,
                "Logitech"
            )

    def test_change_product_info(self):

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        product.change_product_info(
            name="Gaming Mouse",
            category="Gaming",
            price=700000,
            brand="Razer"
        )

        self.assertEqual(product.name, "Gaming Mouse")
        self.assertEqual(product.category, "Gaming")
        self.assertEqual(product.price, 700000)
        self.assertEqual(product.brand, "Razer")

    def test_change_product_info_partial_update(self):

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        product.change_product_info(price=600000)

        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.category, "Accessory")
        self.assertEqual(product.price, 600000)
        self.assertEqual(product.brand, "Logitech")

    def test_change_product_price_cannot_be_negative(self):

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        with self.assertRaises(ValueError):

            product.change_product_info(price=-1)

    def test_product_to_dict(self):

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        data = product.to_dict()

        expected = {
            "id": 101,
            "name": "Mouse",
            "category": "Accessory",
            "price": 500000,
            "brand": "Logitech"
        }

        self.assertEqual(data, expected)

    def test_product_from_dict(self):

        data = {
            "id": 101,
            "name": "Mouse",
            "category": "Accessory",
            "price": 500000,
            "brand": "Logitech"
        }

        product = Product.from_dict(data)

        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, 101)
        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.price, 500000)


# =========================================================
# CUSTOMER TESTS
# =========================================================

class TestCustomer(unittest.TestCase):

    def test_create_customer(self):

        customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.assertEqual(customer.name, "Ali")
        self.assertEqual(customer.email, "ali@example.com")
        self.assertEqual(customer.call_number, "09120000000")
        self.assertEqual(customer.address, "Tehran")
        self.assertEqual(customer.customer_id, 1)

    def test_customer_id_cannot_be_none(self):

        with self.assertRaises(ValueError):

            Customer(
                "Ali",
                "ali@example.com",
                "09120000000",
                "Tehran",
                None
            )

    def test_customer_id_is_read_only_property(self):

        customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        with self.assertRaises(AttributeError):

            customer.customer_id = 10

    def test_change_customer_info(self):

        customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        customer.change_customer_info(
            name="Reza",
            email="reza@example.com",
            call_number="09350000000",
            address="Shiraz"
        )

        self.assertEqual(customer.name, "Reza")
        self.assertEqual(customer.email, "reza@example.com")
        self.assertEqual(customer.call_number, "09350000000")
        self.assertEqual(customer.address, "Shiraz")
        self.assertEqual(customer.customer_id, 1)

    def test_customer_to_dict(self):

        customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        data = customer.to_dict()

        expected = {
            "customer_id": 1,
            "name": "Ali",
            "email": "ali@example.com",
            "call_number": "09120000000",
            "address": "Tehran"
        }

        self.assertEqual(data, expected)

    def test_customer_from_dict(self):

        data = {
            "customer_id": 1,
            "name": "Ali",
            "email": "ali@example.com",
            "call_number": "09120000000",
            "address": "Tehran"
        }

        customer = Customer.from_dict(data)

        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(customer.name, "Ali")


# =========================================================
# INVENTORY TESTS
# =========================================================

class TestInventory(unittest.TestCase):

    def setUp(self):

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

    def test_create_inventory(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.assertIs(inventory.product, self.product)
        self.assertEqual(inventory.quantity, 10)

    def test_inventory_product_cannot_be_none(self):

        with self.assertRaises(ValueError):

            Inventory(None, 10)

    def test_inventory_quantity_cannot_be_negative(self):

        with self.assertRaises(ValueError):

            Inventory(self.product, -1)

    def test_check_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.assertTrue(inventory.check_stock(5))
        self.assertTrue(inventory.check_stock(10))
        self.assertFalse(inventory.check_stock(11))

    def test_check_stock_invalid_quantity(self):

        inventory = Inventory(
            self.product,
            10
        )

        with self.assertRaises(ValueError):
            inventory.check_stock(0)

        with self.assertRaises(ValueError):
            inventory.check_stock(-1)

    def test_add_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        inventory.add_stock(5)

        self.assertEqual(
            inventory.quantity,
            15
        )

    def test_add_stock_invalid_quantity(self):

        inventory = Inventory(
            self.product,
            10
        )

        with self.assertRaises(ValueError):
            inventory.add_stock(0)

        with self.assertRaises(ValueError):
            inventory.add_stock(-5)

    def test_remove_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        inventory.remove_stock(4)

        self.assertEqual(
            inventory.quantity,
            6
        )

    def test_remove_stock_not_enough(self):

        inventory = Inventory(
            self.product,
            10
        )

        with self.assertRaises(ValueError):

            inventory.remove_stock(11)

        self.assertEqual(
            inventory.quantity,
            10
        )

    def test_remove_stock_invalid_quantity(self):

        inventory = Inventory(
            self.product,
            10
        )

        with self.assertRaises(ValueError):
            inventory.remove_stock(0)

        with self.assertRaises(ValueError):
            inventory.remove_stock(-1)

    def test_set_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        inventory.set_stock(25)

        self.assertEqual(
            inventory.quantity,
            25
        )

    def test_set_stock_negative(self):

        inventory = Inventory(
            self.product,
            10
        )

        with self.assertRaises(ValueError):

            inventory.set_stock(-1)

    def test_inventory_to_dict(self):

        inventory = Inventory(
            self.product,
            10
        )

        data = inventory.to_dict()

        expected = {
            "product_id": 101,
            "quantity": 10
        }

        self.assertEqual(
            data,
            expected
        )

    def test_inventory_from_dict(self):

        data = {
            "product_id": 101,
            "quantity": 10
        }

        inventory = Inventory.from_dict(
            data,
            self.product
        )

        self.assertIsInstance(
            inventory,
            Inventory
        )

        self.assertIs(
            inventory.product,
            self.product
        )

        self.assertEqual(
            inventory.quantity,
            10
        )


# =========================================================
# ORDER ITEM TESTS
# =========================================================

class TestOrderItem(unittest.TestCase):

    def setUp(self):

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

    def test_create_order_item(self):

        item = OrderItem(
            self.product,
            3
        )

        self.assertIs(
            item.product,
            self.product
        )

        self.assertEqual(
            item.quantity,
            3
        )

        self.assertEqual(
            item.unit_price,
            500000
        )

    def test_order_item_product_cannot_be_none(self):

        with self.assertRaises(ValueError):

            OrderItem(None, 1)

    def test_order_item_quantity_must_be_positive(self):

        with self.assertRaises(ValueError):
            OrderItem(self.product, 0)

        with self.assertRaises(ValueError):
            OrderItem(self.product, -1)

    def test_calculate_price(self):

        item = OrderItem(
            self.product,
            3
        )

        self.assertEqual(
            item.calculate_price(),
            1500000
        )

    def test_historical_unit_price(self):

        item = OrderItem(
            self.product,
            2
        )

        self.product.price = 700000

        self.assertEqual(
            item.unit_price,
            500000
        )

        self.assertEqual(
            item.calculate_price(),
            1000000
        )

    def test_order_item_to_dict(self):

        item = OrderItem(
            self.product,
            2
        )

        data = item.to_dict()

        expected = {
            "product_id": 101,
            "quantity": 2,
            "unit_price": 500000
        }

        self.assertEqual(
            data,
            expected
        )

    def test_order_item_from_dict(self):

        data = {
            "product_id": 101,
            "quantity": 2,
            "unit_price": 450000
        }

        item = OrderItem.from_dict(
            data,
            self.product
        )

        self.assertEqual(
            item.quantity,
            2
        )

        self.assertEqual(
            item.unit_price,
            450000
        )

        self.assertEqual(
            item.calculate_price(),
            900000
        )


# =========================================================
# ORDER TESTS
# =========================================================

class TestOrder(unittest.TestCase):

    def setUp(self):

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

    def test_create_order_default_status(self):

        order = Order(self.customer)

        self.assertIs(
            order.customer,
            self.customer
        )

        self.assertEqual(
            order.status,
            "pending"
        )

        self.assertEqual(
            order.items,
            []
        )

    def test_create_order_with_valid_status(self):

        for status in [
            "pending",
            "completed",
            "cancelled"
        ]:

            order = Order(
                self.customer,
                status
            )

            self.assertEqual(
                order.status,
                status
            )

    def test_order_customer_cannot_be_none(self):

        with self.assertRaises(ValueError):

            Order(None)

    def test_invalid_order_status(self):

        with self.assertRaises(ValueError):

            Order(
                self.customer,
                "invalid"
            )

    def test_add_item(self):

        order = Order(
            self.customer
        )

        item = OrderItem(
            self.product,
            2
        )

        order.add_item(item)

        self.assertEqual(
            len(order.items),
            1
        )

        self.assertIs(
            order.items[0],
            item
        )

    def test_add_none_item(self):

        order = Order(
            self.customer
        )

        with self.assertRaises(ValueError):

            order.add_item(None)

    def test_calculate_total(self):

        order = Order(
            self.customer
        )

        item1 = OrderItem(
            self.product,
            2
        )

        product2 = Product(
            "Keyboard",
            102,
            "Accessory",
            800000,
            "Logitech"
        )

        item2 = OrderItem(
            product2,
            1
        )

        order.add_item(item1)
        order.add_item(item2)

        self.assertEqual(
            order.calculate_total(),
            1800000
        )

    def test_update_status_pending_to_completed(self):

        order = Order(
            self.customer
        )

        order.update_status("completed")

        self.assertEqual(
            order.status,
            "completed"
        )

    def test_update_status_pending_to_cancelled(self):

        order = Order(
            self.customer
        )

        order.update_status("cancelled")

        self.assertEqual(
            order.status,
            "cancelled"
        )

    def test_update_status_invalid(self):

        order = Order(
            self.customer
        )

        with self.assertRaises(ValueError):

            order.update_status("invalid")

    def test_completed_order_is_final(self):

        order = Order(
            self.customer,
            "completed"
        )

        with self.assertRaises(ValueError):
            order.update_status("pending")

        with self.assertRaises(ValueError):
            order.update_status("cancelled")

    def test_cancelled_order_is_final(self):

        order = Order(
            self.customer,
            "cancelled"
        )

        with self.assertRaises(ValueError):
            order.update_status("pending")

        with self.assertRaises(ValueError):
            order.update_status("completed")

    def test_order_to_dict(self):

        order = Order(
            self.customer
        )

        item = OrderItem(
            self.product,
            2
        )

        order.add_item(item)
        order.update_status("completed")

        data = order.to_dict()

        expected = {
            "customer_id": 1,
            "status": "completed",
            "items": [
                {
                    "product_id": 101,
                    "quantity": 2,
                    "unit_price": 500000
                }
            ]
        }

        self.assertEqual(
            data,
            expected
        )

    def test_order_from_dict(self):

        data = {
            "customer_id": 1,
            "status": "completed",
            "items": [
                {
                    "product_id": 101,
                    "quantity": 2,
                    "unit_price": 500000
                }
            ]
        }

        products = {
            101: self.product
        }

        order = Order.from_dict(
            data,
            self.customer,
            products
        )

        self.assertEqual(
            order.status,
            "completed"
        )

        self.assertIs(
            order.customer,
            self.customer
        )

        self.assertEqual(
            len(order.items),
            1
        )

        self.assertEqual(
            order.items[0].quantity,
            2
        )

        self.assertEqual(
            order.items[0].unit_price,
            500000
        )

    def test_order_from_dict_missing_product(self):

        data = {
            "customer_id": 1,
            "status": "completed",
            "items": [
                {
                    "product_id": 999,
                    "quantity": 2,
                    "unit_price": 500000
                }
            ]
        }

        with self.assertRaises(ValueError):

            Order.from_dict(
                data,
                self.customer,
                {}
            )


# =========================================================
# STORE PRODUCT TESTS
# =========================================================

class TestStoreProducts(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

    def test_add_product(self):

        self.store.add_product(
            self.product
        )

        self.assertEqual(
            len(self.store.products),
            1
        )

        self.assertIs(
            self.store.products[0],
            self.product
        )

    def test_add_none_product(self):

        with self.assertRaises(ValueError):

            self.store.add_product(None)

    def test_duplicate_product_id(self):

        self.store.add_product(
            self.product
        )

        duplicate = Product(
            "Keyboard",
            101,
            "Accessory",
            800000,
            "Logitech"
        )

        with self.assertRaises(ValueError):

            self.store.add_product(
                duplicate
            )

    def test_find_product(self):

        self.store.add_product(
            self.product
        )

        found = self.store.find_product(101)

        self.assertIs(
            found,
            self.product
        )

    def test_find_missing_product(self):

        self.assertIsNone(
            self.store.find_product(999)
        )

    def test_update_product(self):

        self.store.add_product(
            self.product
        )

        updated = self.store.update_product(
            101,
            name="Gaming Mouse",
            price=700000
        )

        self.assertIs(
            updated,
            self.product
        )

        self.assertEqual(
            self.product.name,
            "Gaming Mouse"
        )

        self.assertEqual(
            self.product.price,
            700000
        )

    def test_update_missing_product(self):

        result = self.store.update_product(
            999,
            name="Unknown"
        )

        self.assertIsNone(result)

    def test_remove_product_without_inventory(self):

        self.store.add_product(
            self.product
        )

        result = self.store.remove_product(101)

        self.assertTrue(result)

        self.assertIsNone(
            self.store.find_product(101)
        )

    def test_remove_missing_product(self):

        result = self.store.remove_product(999)

        self.assertFalse(result)


# =========================================================
# STORE CUSTOMER TESTS
# =========================================================

class TestStoreCustomers(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

    def test_add_customer(self):

        self.store.add_customer(
            self.customer
        )

        self.assertEqual(
            len(self.store.customers),
            1
        )

    def test_add_none_customer(self):

        with self.assertRaises(ValueError):

            self.store.add_customer(None)

    def test_duplicate_customer_id(self):

        self.store.add_customer(
            self.customer
        )

        duplicate = Customer(
            "Reza",
            "reza@example.com",
            "09350000000",
            "Shiraz",
            1
        )

        with self.assertRaises(ValueError):

            self.store.add_customer(
                duplicate
            )

    def test_find_customer(self):

        self.store.add_customer(
            self.customer
        )

        found = self.store.find_customer(1)

        self.assertIs(
            found,
            self.customer
        )

    def test_find_missing_customer(self):

        self.assertIsNone(
            self.store.find_customer(999)
        )

    def test_update_customer(self):

        self.store.add_customer(
            self.customer
        )

        updated = self.store.update_customer(
            1,
            name="Reza",
            address="Shiraz"
        )

        self.assertIs(
            updated,
            self.customer
        )

        self.assertEqual(
            self.customer.name,
            "Reza"
        )

        self.assertEqual(
            self.customer.address,
            "Shiraz"
        )

    def test_update_missing_customer(self):

        result = self.store.update_customer(
            999,
            name="Unknown"
        )

        self.assertIsNone(result)

    def test_remove_customer_without_orders(self):

        self.store.add_customer(
            self.customer
        )

        result = self.store.remove_customer(1)

        self.assertTrue(result)

        self.assertIsNone(
            self.store.find_customer(1)
        )

    def test_remove_missing_customer(self):

        result = self.store.remove_customer(999)

        self.assertFalse(result)


# =========================================================
# STORE INVENTORY TESTS
# =========================================================

class TestStoreInventory(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.store.add_product(
            self.product
        )

    def test_add_inventory(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        self.assertEqual(
            len(self.store.inventories),
            1
        )

        self.assertIs(
            self.store.inventories[0],
            inventory
        )

    def test_add_inventory_for_unknown_product(self):

        unknown_product = Product(
            "Keyboard",
            999,
            "Accessory",
            800000,
            "Logitech"
        )

        inventory = Inventory(
            unknown_product,
            10
        )

        with self.assertRaises(ValueError):

            self.store.add_inventory(
                inventory
            )

    def test_duplicate_inventory(self):

        inventory1 = Inventory(
            self.product,
            10
        )

        inventory2 = Inventory(
            self.product,
            20
        )

        self.store.add_inventory(
            inventory1
        )

        with self.assertRaises(ValueError):

            self.store.add_inventory(
                inventory2
            )

    def test_find_inventory(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        found = self.store.find_inventory(
            self.product
        )

        self.assertIs(
            found,
            inventory
        )

    def test_find_inventory_none(self):

        self.assertIsNone(
            self.store.find_inventory(None)
        )

    def test_add_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.add_stock(
            101,
            5
        )

        self.assertIs(
            result,
            inventory
        )

        self.assertEqual(
            inventory.quantity,
            15
        )

    def test_remove_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.remove_stock(
            101,
            4
        )

        self.assertIs(
            result,
            inventory
        )

        self.assertEqual(
            inventory.quantity,
            6
        )

    def test_set_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.set_stock(
            101,
            25
        )

        self.assertIs(
            result,
            inventory
        )

        self.assertEqual(
            inventory.quantity,
            25
        )

    def test_stock_operation_missing_product(self):

        self.assertIsNone(
            self.store.add_stock(999, 5)
        )

        self.assertIsNone(
            self.store.remove_stock(999, 5)
        )

        self.assertIsNone(
            self.store.set_stock(999, 5)
        )

    def test_stock_operation_missing_inventory(self):

        self.assertIsNone(
            self.store.add_stock(101, 5)
        )

        self.assertIsNone(
            self.store.remove_stock(101, 5)
        )

        self.assertIsNone(
            self.store.set_stock(101, 5)
        )

    def test_remove_product_with_stock(self):

        inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            inventory
        )

        with self.assertRaises(ValueError):

            self.store.remove_product(101)

        self.assertIsNotNone(
            self.store.find_product(101)
        )

    def test_remove_product_with_zero_stock(self):

        inventory = Inventory(
            self.product,
            0
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.remove_product(101)

        self.assertTrue(result)

        self.assertIsNone(
            self.store.find_product(101)
        )

        self.assertEqual(
            len(self.store.inventories),
            0
        )

    def test_low_stock(self):

        inventory = Inventory(
            self.product,
            3
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.low_stock(5)

        self.assertEqual(
            len(result),
            1
        )

        self.assertIs(
            result[0],
            inventory
        )

    def test_low_stock_excludes_zero_stock(self):

        inventory = Inventory(
            self.product,
            0
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.low_stock(5)

        self.assertEqual(
            result,
            []
        )

    def test_low_stock_negative_threshold(self):

        with self.assertRaises(ValueError):

            self.store.low_stock(-1)

    def test_out_of_stock(self):

        inventory = Inventory(
            self.product,
            0
        )

        self.store.add_inventory(
            inventory
        )

        result = self.store.out_of_stock()

        self.assertEqual(
            len(result),
            1
        )

        self.assertIs(
            result[0],
            inventory
        )


# =========================================================
# STORE ORDER TESTS
# =========================================================

class TestStoreOrders(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.product1 = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.product2 = Product(
            "Keyboard",
            102,
            "Accessory",
            800000,
            "Logitech"
        )

        self.store.add_product(
            self.product1
        )

        self.store.add_product(
            self.product2
        )

        self.inventory1 = Inventory(
            self.product1,
            10
        )

        self.inventory2 = Inventory(
            self.product2,
            10
        )

        self.store.add_inventory(
            self.inventory1
        )

        self.store.add_inventory(
            self.inventory2
        )

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.store.add_customer(
            self.customer
        )

    def test_add_order(self):

        order = Order(
            self.customer
        )

        self.store.add_order(
            order
        )

        self.assertEqual(
            len(self.store.orders),
            1
        )

        self.assertIs(
            self.store.orders[0],
            order
        )

    def test_add_none_order(self):

        with self.assertRaises(ValueError):

            self.store.add_order(None)

    def test_find_order(self):

        order = Order(
            self.customer
        )

        self.store.add_order(
            order
        )

        self.assertIs(
            self.store.find_order(0),
            order
        )

    def test_find_order_invalid_index(self):

        self.assertIsNone(
            self.store.find_order(0)
        )

        self.assertIsNone(
            self.store.find_order(-1)
        )

    def test_create_successful_order(self):

        order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2),
                (102, 3)
            ]
        )

        self.assertIsInstance(
            order,
            Order
        )

        self.assertEqual(
            order.status,
            "completed"
        )

        self.assertEqual(
            len(order.items),
            2
        )

        self.assertEqual(
            self.inventory1.quantity,
            8
        )

        self.assertEqual(
            self.inventory2.quantity,
            7
        )

        self.assertEqual(
            order.calculate_total(),
            3400000
        )

        self.assertEqual(
            self.store.number_of_orders(),
            1
        )

        self.assertEqual(
            self.store.total_sales(),
            3400000
        )

    def test_create_order_invalid_customer(self):

        result = self.store.create_order(
            customer_id=999,
            items=[
                (101, 2)
            ]
        )

        self.assertIsNone(result)

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_empty_items(self):

        with self.assertRaises(ValueError):

            self.store.create_order(
                customer_id=1,
                items=[]
            )

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_unknown_product(self):

        result = self.store.create_order(
            customer_id=1,
            items=[
                (999, 2)
            ]
        )

        self.assertIsNone(result)

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_without_inventory(self):

        product3 = Product(
            "Monitor",
            103,
            "Display",
            5000000,
            "LG"
        )

        self.store.add_product(
            product3
        )

        result = self.store.create_order(
            customer_id=1,
            items=[
                (103, 1)
            ]
        )

        self.assertIsNone(result)

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_insufficient_stock(self):

        result = self.store.create_order(
            customer_id=1,
            items=[
                (101, 11)
            ]
        )

        self.assertIsNone(result)

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_zero_quantity(self):

        with self.assertRaises(ValueError):

            self.store.create_order(
                customer_id=1,
                items=[
                    (101, 0)
                ]
            )

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_negative_quantity(self):

        with self.assertRaises(ValueError):

            self.store.create_order(
                customer_id=1,
                items=[
                    (101, -1)
                ]
            )

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_is_atomic_when_later_item_fails(self):

        result = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2),
                (102, 11)
            ]
        )

        self.assertIsNone(result)

        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.inventory2.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_same_product_multiple_times_success(self):

        result = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2),
                (101, 3)
            ]
        )

        self.assertIsInstance(
            result,
            Order
        )

        self.assertEqual(
            result.status,
            "completed"
        )

        self.assertEqual(
            len(result.items),
            2
        )

        self.assertEqual(
            result.items[0].quantity,
            2
        )

        self.assertEqual(
            result.items[1].quantity,
            3
        )

        self.assertEqual(
            self.inventory1.quantity,
            5
        )

        self.assertEqual(
            result.calculate_total(),
            2500000
        )

    def test_create_order_same_product_multiple_times_exceeds_stock(self):

        result = self.store.create_order(
            customer_id=1,
            items=[
                (101, 6),
                (101, 6)
            ]
        )

        self.assertIsNone(result)

        # Stock must not change because the complete
        # order failed.
        self.assertEqual(
            self.inventory1.quantity,
            10
        )

        self.assertEqual(
            self.store.number_of_orders(),
            0
        )

    def test_create_order_price_snapshot(self):

        order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        self.product1.price = 700000

        self.assertEqual(
            order.items[0].unit_price,
            500000
        )

        self.assertEqual(
            order.calculate_total(),
            1000000
        )

    def test_get_orders_by_status(self):

        completed_order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        pending_order = Order(
            self.customer,
            "pending"
        )

        self.store.add_order(
            pending_order
        )

        completed = self.store.get_orders_by_status(
            "completed"
        )

        pending = self.store.get_orders_by_status(
            "pending"
        )

        self.assertEqual(
            len(completed),
            1
        )

        self.assertIs(
            completed[0],
            completed_order
        )

        self.assertEqual(
            len(pending),
            1
        )

        self.assertIs(
            pending[0],
            pending_order
        )

    def test_get_orders_by_status_invalid(self):

        with self.assertRaises(ValueError):

            self.store.get_orders_by_status(
                "invalid"
            )

    def test_cancel_pending_order(self):

        order = Order(
            self.customer,
            "pending"
        )

        self.store.add_order(
            order
        )

        result = self.store.cancel_order(0)

        self.assertIs(
            result,
            order
        )

        self.assertEqual(
            order.status,
            "cancelled"
        )

    def test_cancel_invalid_order_index(self):

        result = self.store.cancel_order(999)

        self.assertIsNone(result)

    def test_cancel_completed_order_fails(self):

        order = Order(
            self.customer,
            "completed"
        )

        self.store.add_order(
            order
        )

        with self.assertRaises(ValueError):

            self.store.cancel_order(0)

        self.assertEqual(
            order.status,
            "completed"
        )

    def test_remove_customer_with_existing_order(self):

        order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 1)
            ]
        )

        self.assertIsNotNone(order)

        with self.assertRaises(ValueError):

            self.store.remove_customer(1)

        self.assertIsNotNone(
            self.store.find_customer(1)
        )


# =========================================================
# STORE REPORT TESTS
# =========================================================

class TestStoreReports(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.store.add_product(
            self.product
        )

        self.inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            self.inventory
        )

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.store.add_customer(
            self.customer
        )

    def test_order_count_reports(self):

        completed_order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        pending_order = Order(
            self.customer,
            "pending"
        )

        self.store.add_order(
            pending_order
        )

        cancelled_order = Order(
            self.customer,
            "cancelled"
        )

        self.store.add_order(
            cancelled_order
        )

        self.assertIsNotNone(
            completed_order
        )

        self.assertEqual(
            self.store.number_of_orders(),
            3
        )

        self.assertEqual(
            self.store.number_of_completed_orders(),
            1
        )

        self.assertEqual(
            self.store.number_of_pending_orders(),
            1
        )

        self.assertEqual(
            self.store.number_of_cancelled_orders(),
            1
        )

    def test_total_sales_only_completed_orders(self):

        completed_order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        pending_order = Order(
            self.customer,
            "pending"
        )

        pending_item = OrderItem(
            self.product,
            3
        )

        pending_order.add_item(
            pending_item
        )

        self.store.add_order(
            pending_order
        )

        self.assertEqual(
            completed_order.calculate_total(),
            1000000
        )

        self.assertEqual(
            pending_order.calculate_total(),
            1500000
        )

        self.assertEqual(
            self.store.total_sales(),
            1000000
        )

    def test_low_stock_report_data(self):

        self.inventory.set_stock(3)

        result = self.store.low_stock(5)

        self.assertEqual(
            len(result),
            1
        )

        self.assertIs(
            result[0],
            self.inventory
        )

    def test_out_of_stock_report_data(self):

        self.inventory.set_stock(0)

        result = self.store.out_of_stock()

        self.assertEqual(
            len(result),
            1
        )

        self.assertIs(
            result[0],
            self.inventory
        )


# =========================================================
# STORE JSON SERIALIZATION TESTS
# =========================================================

class TestStoreSerialization(unittest.TestCase):

    def setUp(self):

        self.store = Store()

        self.product1 = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.product2 = Product(
            "Keyboard",
            102,
            "Accessory",
            800000,
            "Logitech"
        )

        self.store.add_product(
            self.product1
        )

        self.store.add_product(
            self.product2
        )

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.store.add_customer(
            self.customer
        )

        self.inventory1 = Inventory(
            self.product1,
            8
        )

        self.inventory2 = Inventory(
            self.product2,
            10
        )

        self.store.add_inventory(
            self.inventory1
        )

        self.store.add_inventory(
            self.inventory2
        )

        self.order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2),
                (102, 3)
            ]
        )

    def test_store_to_dict(self):

        data = self.store.to_dict()

        self.assertIn(
            "products",
            data
        )

        self.assertIn(
            "customers",
            data
        )

        self.assertIn(
            "inventories",
            data
        )

        self.assertIn(
            "orders",
            data
        )

        self.assertEqual(
            len(data["products"]),
            2
        )

        self.assertEqual(
            len(data["customers"]),
            1
        )

        self.assertEqual(
            len(data["inventories"]),
            2
        )

        self.assertEqual(
            len(data["orders"]),
            1
        )

    def test_store_from_dict(self):

        data = self.store.to_dict()

        restored_store = Store.from_dict(
            data
        )

        self.assertEqual(
            len(restored_store.products),
            2
        )

        self.assertEqual(
            len(restored_store.customers),
            1
        )

        self.assertEqual(
            len(restored_store.inventories),
            2
        )

        self.assertEqual(
            len(restored_store.orders),
            1
        )

        restored_product = (
            restored_store.find_product(101)
        )

        restored_customer = (
            restored_store.find_customer(1)
        )

        restored_order = (
            restored_store.find_order(0)
        )

        self.assertIsNotNone(
            restored_product
        )

        self.assertIsNotNone(
            restored_customer
        )

        self.assertIsNotNone(
            restored_order
        )

        self.assertEqual(
            restored_product.name,
            "Mouse"
        )

        self.assertEqual(
            restored_product.price,
            500000
        )

        self.assertEqual(
            restored_customer.name,
            "Ali"
        )

        self.assertEqual(
            restored_order.status,
            "completed"
        )

        self.assertEqual(
            restored_order.calculate_total(),
            3400000
        )

    def test_store_round_trip_preserves_data(self):

        original_data = self.store.to_dict()

        restored_store = Store.from_dict(
            original_data
        )

        restored_data = restored_store.to_dict()

        self.assertEqual(
            original_data,
            restored_data
        )

    def test_store_from_dict_missing_inventory_product(self):

        data = self.store.to_dict()

        data["inventories"].append({
            "product_id": 999,
            "quantity": 5
        })

        with self.assertRaises(ValueError):

            Store.from_dict(data)

    def test_store_from_dict_missing_order_customer(self):

        data = self.store.to_dict()

        data["orders"][0]["customer_id"] = 999

        with self.assertRaises(ValueError):

            Store.from_dict(data)

    def test_store_from_dict_missing_order_product(self):

        data = self.store.to_dict()

        data["orders"][0]["items"][0]["product_id"] = 999

        with self.assertRaises(ValueError):

            Store.from_dict(data)


# =========================================================
# STORE PERSISTENCE TESTS
# =========================================================

class TestStorePersistence(unittest.TestCase):

    def setUp(self):

        self.temp_directory = tempfile.TemporaryDirectory()

        self.file_path = os.path.join(
            self.temp_directory.name,
            "test_store.json"
        )

        self.store = Store()

        self.product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        self.store.add_product(
            self.product
        )

        self.inventory = Inventory(
            self.product,
            10
        )

        self.store.add_inventory(
            self.inventory
        )

        self.customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        self.store.add_customer(
            self.customer
        )

    def tearDown(self):

        self.temp_directory.cleanup()

    def test_save_creates_json_file(self):

        persistence = StorePersistence(
            self.file_path
        )

        persistence.save(
            self.store
        )

        self.assertTrue(
            os.path.exists(
                self.file_path
            )
        )

    def test_save_and_load(self):

        order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        self.assertIsNotNone(order)

        persistence = StorePersistence(
            self.file_path
        )

        persistence.save(
            self.store
        )

        loaded_store = persistence.load()

        self.assertIsInstance(
            loaded_store,
            Store
        )

        self.assertEqual(
            len(loaded_store.products),
            1
        )

        self.assertEqual(
            len(loaded_store.customers),
            1
        )

        self.assertEqual(
            len(loaded_store.inventories),
            1
        )

        self.assertEqual(
            len(loaded_store.orders),
            1
        )

        loaded_order = (
            loaded_store.find_order(0)
        )

        self.assertEqual(
            loaded_order.status,
            "completed"
        )

        self.assertEqual(
            loaded_order.calculate_total(),
            1000000
        )

        loaded_inventory = (
            loaded_store.find_inventory(
                loaded_store.find_product(101)
            )
        )

        self.assertEqual(
            loaded_inventory.quantity,
            8
        )

    def test_load_preserves_historical_order_price(self):

        order = self.store.create_order(
            customer_id=1,
            items=[
                (101, 2)
            ]
        )

        self.assertEqual(
            order.items[0].unit_price,
            500000
        )

        # Product price changes after the order.
        self.product.price = 700000

        persistence = StorePersistence(
            self.file_path
        )

        persistence.save(
            self.store
        )

        loaded_store = persistence.load()

        loaded_order = (
            loaded_store.find_order(0)
        )

        loaded_product = (
            loaded_store.find_product(101)
        )

        self.assertEqual(
            loaded_product.price,
            700000
        )

        self.assertEqual(
            loaded_order.items[0].unit_price,
            500000
        )

        self.assertEqual(
            loaded_order.calculate_total(),
            1000000
        )

    def test_load_missing_file_returns_empty_store(self):

        persistence = StorePersistence(
            self.file_path
        )

        loaded_store = persistence.load()

        self.assertIsInstance(
            loaded_store,
            Store
        )

        self.assertEqual(
            loaded_store.products,
            []
        )

        self.assertEqual(
            loaded_store.customers,
            []
        )

        self.assertEqual(
            loaded_store.inventories,
            []
        )

        self.assertEqual(
            loaded_store.orders,
            []
        )

    def test_load_invalid_json(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "{ invalid json"
            )

        persistence = StorePersistence(
            self.file_path
        )

        with self.assertRaises(ValueError):

            persistence.load()

    def test_load_json_root_must_be_dict(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file
            )

        persistence = StorePersistence(
            self.file_path
        )

        with self.assertRaises(ValueError):

            persistence.load()

    def test_save_none_store(self):

        persistence = StorePersistence(
            self.file_path
        )

        with self.assertRaises(ValueError):

            persistence.save(None)


# =========================================================
# DISPLAY METHOD TESTS
# =========================================================

class TestDisplayMethods(unittest.TestCase):

    def test_display_methods_do_not_raise_errors(self):

        store = Store()

        product = Product(
            "Mouse",
            101,
            "Accessory",
            500000,
            "Logitech"
        )

        customer = Customer(
            "Ali",
            "ali@example.com",
            "09120000000",
            "Tehran",
            1
        )

        inventory = Inventory(
            product,
            5
        )

        store.add_product(
            product
        )

        store.add_customer(
            customer
        )

        store.add_inventory(
            inventory
        )

        order = store.create_order(
            customer_id=1,
            items=[
                (101, 1)
            ]
        )

        self.assertIsNotNone(order)

        product.display_product()
        customer.display_customer()
        inventory.display_inventory()
        order.items[0].display_order_item()
        order.display_order()

        store.display_products()
        store.display_customers()
        store.display_inventory()
        store.display_orders()
        store.display_sales_report()
        store.display_low_stock_report()
        store.display_out_of_stock_report()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)