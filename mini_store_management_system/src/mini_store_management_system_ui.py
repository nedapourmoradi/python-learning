import os
import tkinter as tk
from tkinter import ttk, messagebox

from src.mini_store_management_system import (
    Store,
    Product,
    Customer,
    Inventory,
    StorePersistence,
)


# =========================================================
# MAIN APPLICATION
# =========================================================

class StoreApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Mini Store Management System")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.persistence = StorePersistence("store.json")
        self.store = self.load_store()

        # Temporary items for order creation
        self.current_order_items = []

        self.create_style()
        self.create_header()
        self.create_notebook()
        self.create_status_bar()

        self.refresh_all()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # =====================================================
    # APPLICATION SETUP
    # =====================================================

    def create_style(self):

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 20, "bold")
        )

        style.configure(
            "Section.TLabel",
            font=("Arial", 14, "bold")
        )

        style.configure(
            "Action.TButton",
            padding=6
        )

    def create_header(self):

        header = ttk.Frame(self, padding=15)
        header.pack(fill="x")

        title = ttk.Label(
            header,
            text="Mini Store Management System",
            style="Title.TLabel"
        )

        title.pack(side="left")

        save_button = ttk.Button(
            header,
            text="Save Store",
            command=self.save_store
        )

        save_button.pack(
            side="right",
            padx=5
        )

        load_button = ttk.Button(
            header,
            text="Load Store",
            command=self.reload_store
        )

        load_button.pack(
            side="right",
            padx=5
        )

    def create_notebook(self):

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        self.create_products_tab()
        self.create_customers_tab()
        self.create_inventory_tab()
        self.create_orders_tab()
        self.create_reports_tab()

    def create_status_bar(self):

        self.status_var = tk.StringVar(
            value="Ready"
        )

        status = ttk.Label(
            self,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=5
        )

        status.pack(
            fill="x",
            side="bottom"
        )

    # =====================================================
    # GENERAL HELPERS
    # =====================================================

    def set_status(self, message):

        self.status_var.set(message)

    def load_store(self):

        try:
            return self.persistence.load()

        except (ValueError, OSError) as error:

            messagebox.showwarning(
                "Load Error",
                f"Could not load store data.\n\n{error}"
            )

            return Store()

    def save_store(self):

        try:

            self.persistence.save(self.store)

            self.set_status(
                "Store saved successfully."
            )

            messagebox.showinfo(
                "Success",
                "Store saved successfully."
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )

    def reload_store(self):

        try:

            self.store = self.persistence.load()
            self.refresh_all()

            self.set_status(
                "Store loaded successfully."
            )

            messagebox.showinfo(
                "Success",
                "Store loaded successfully."
            )

        except (ValueError, OSError) as error:

            messagebox.showerror(
                "Load Error",
                str(error)
            )

    def on_close(self):

        answer = messagebox.askyesnocancel(
            "Exit",
            "Do you want to save the store before exiting?"
        )

        if answer is None:
            return

        if answer:

            try:
                self.persistence.save(self.store)

            except (ValueError, OSError) as error:

                messagebox.showerror(
                    "Save Error",
                    str(error)
                )

                return

        self.destroy()

    def refresh_all(self):

        self.refresh_products()
        self.refresh_customers()
        self.refresh_inventory()
        self.refresh_orders()
        self.refresh_reports()
        self.refresh_order_product_combobox()
        self.refresh_order_customer_combobox()

    # =====================================================
    # PRODUCTS TAB
    # =====================================================

    def create_products_tab(self):

        tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            tab,
            text="Products"
        )

        toolbar = ttk.Frame(tab)
        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            toolbar,
            text="Add Product",
            command=self.add_product_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Update Product",
            command=self.update_product_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Remove Product",
            command=self.remove_product
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_products
        ).pack(side="right", padx=3)

        columns = (
            "id",
            "name",
            "category",
            "price",
            "brand"
        )

        self.products_tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings"
        )

        self.products_tree.heading(
            "id",
            text="ID"
        )

        self.products_tree.heading(
            "name",
            text="Name"
        )

        self.products_tree.heading(
            "category",
            text="Category"
        )

        self.products_tree.heading(
            "price",
            text="Price"
        )

        self.products_tree.heading(
            "brand",
            text="Brand"
        )

        self.products_tree.column(
            "id",
            width=80
        )

        self.products_tree.column(
            "name",
            width=200
        )

        self.products_tree.column(
            "category",
            width=180
        )

        self.products_tree.column(
            "price",
            width=150
        )

        self.products_tree.column(
            "brand",
            width=180
        )

        scrollbar = ttk.Scrollbar(
            tab,
            orient="vertical",
            command=self.products_tree.yview
        )

        self.products_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.products_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.products_tree.bind(
            "<Double-1>",
            lambda event: self.update_product_dialog()
        )

    def refresh_products(self):

        if not hasattr(self, "products_tree"):
            return

        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        for product in self.store.products:

            self.products_tree.insert(
                "",
                "end",
                values=(
                    product.id,
                    product.name,
                    product.category,
                    product.price,
                    product.brand
                )
            )

    def get_selected_product_id(self):

        selection = self.products_tree.selection()

        if not selection:
            messagebox.showwarning(
                "Selection",
                "Please select a product first."
            )
            return None

        values = self.products_tree.item(
            selection[0],
            "values"
        )

        return int(values[0])

    def add_product_dialog(self):

        dialog = tk.Toplevel(self)

        dialog.title("Add Product")
        dialog.geometry("400x350")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        fields = {}

        labels = [
            ("Name", "name"),
            ("Product ID", "id"),
            ("Category", "category"),
            ("Price", "price"),
            ("Brand", "brand")
        ]

        for row, (label, key) in enumerate(labels):

            ttk.Label(
                frame,
                text=f"{label}:"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=7
            )

            entry = ttk.Entry(
                frame,
                width=30
            )

            entry.grid(
                row=row,
                column=1,
                pady=7
            )

            fields[key] = entry

        def submit():

            name = fields["name"].get().strip()
            category = fields["category"].get().strip()
            brand = fields["brand"].get().strip()

            if not name or not category or not brand:

                messagebox.showwarning(
                    "Validation",
                    "Please fill in all text fields.",
                    parent=dialog
                )

                return

            try:

                product_id = int(
                    fields["id"].get()
                )

                price = float(
                    fields["price"].get()
                )

                product = Product(
                    name=name,
                    id=product_id,
                    category=category,
                    price=price,
                    brand=brand
                )

                self.store.add_product(product)

                self.refresh_all()
                self.set_status(
                    "Product added successfully."
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text="Add Product",
            command=submit
        ).grid(
            row=len(labels),
            column=0,
            columnspan=2,
            pady=20
        )

    def update_product_dialog(self):

        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        product = self.store.find_product(
            product_id
        )

        if product is None:
            messagebox.showerror(
                "Error",
                "Product not found."
            )
            return

        dialog = tk.Toplevel(self)

        dialog.title("Update Product")
        dialog.geometry("400x350")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        fields = {}

        values = {
            "Name": product.name,
            "Category": product.category,
            "Price": product.price,
            "Brand": product.brand
        }

        for row, (label, value) in enumerate(values.items()):

            ttk.Label(
                frame,
                text=f"{label}:"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=7
            )

            entry = ttk.Entry(
                frame,
                width=30
            )

            entry.insert(
                0,
                str(value)
            )

            entry.grid(
                row=row,
                column=1,
                pady=7
            )

            fields[label] = entry

        def submit():

            try:

                self.store.update_product(
                    product_id,
                    name=fields["Name"].get().strip(),
                    category=fields["Category"].get().strip(),
                    price=float(
                        fields["Price"].get()
                    ),
                    brand=fields["Brand"].get().strip()
                )

                self.refresh_all()

                self.set_status(
                    "Product updated successfully."
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text="Update Product",
            command=submit
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

    def remove_product(self):

        product_id = self.get_selected_product_id()

        if product_id is None:
            return

        answer = messagebox.askyesno(
            "Confirm",
            "Remove selected product?"
        )

        if not answer:
            return

        try:

            result = self.store.remove_product(
                product_id
            )

            if result:

                self.refresh_all()

                self.set_status(
                    "Product removed successfully."
                )

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # =====================================================
    # CUSTOMERS TAB
    # =====================================================

    def create_customers_tab(self):

        tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            tab,
            text="Customers"
        )

        toolbar = ttk.Frame(tab)
        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            toolbar,
            text="Add Customer",
            command=self.add_customer_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Update Customer",
            command=self.update_customer_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Remove Customer",
            command=self.remove_customer
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_customers
        ).pack(side="right", padx=3)

        columns = (
            "id",
            "name",
            "email",
            "phone",
            "address"
        )

        self.customers_tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Name",
            "email": "Email",
            "phone": "Call Number",
            "address": "Address"
        }

        widths = {
            "id": 80,
            "name": 180,
            "email": 220,
            "phone": 160,
            "address": 250
        }

        for column in columns:

            self.customers_tree.heading(
                column,
                text=headings[column]
            )

            self.customers_tree.column(
                column,
                width=widths[column]
            )

        self.customers_tree.pack(
            fill="both",
            expand=True
        )

        self.customers_tree.bind(
            "<Double-1>",
            lambda event: self.update_customer_dialog()
        )

    def refresh_customers(self):

        if not hasattr(self, "customers_tree"):
            return

        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        for customer in self.store.customers:

            self.customers_tree.insert(
                "",
                "end",
                values=(
                    customer.customer_id,
                    customer.name,
                    customer.email,
                    customer.call_number,
                    customer.address
                )
            )

    def get_selected_customer_id(self):

        selection = self.customers_tree.selection()

        if not selection:

            messagebox.showwarning(
                "Selection",
                "Please select a customer first."
            )

            return None

        values = self.customers_tree.item(
            selection[0],
            "values"
        )

        return int(values[0])

    def add_customer_dialog(self):

        dialog = tk.Toplevel(self)

        dialog.title("Add Customer")
        dialog.geometry("430x380")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        fields = {}

        labels = [
            ("Name", "name"),
            ("Email", "email"),
            ("Call Number", "phone"),
            ("Address", "address"),
            ("Customer ID", "id")
        ]

        for row, (label, key) in enumerate(labels):

            ttk.Label(
                frame,
                text=f"{label}:"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=7
            )

            entry = ttk.Entry(
                frame,
                width=32
            )

            entry.grid(
                row=row,
                column=1,
                pady=7
            )

            fields[key] = entry

        def submit():

            try:

                customer = Customer(
                    name=fields["name"].get().strip(),
                    email=fields["email"].get().strip(),
                    call_number=fields["phone"].get().strip(),
                    address=fields["address"].get().strip(),
                    customer_id=int(
                        fields["id"].get()
                    )
                )

                self.store.add_customer(
                    customer
                )

                self.refresh_all()

                self.set_status(
                    "Customer added successfully."
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text="Add Customer",
            command=submit
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20
        )

    def update_customer_dialog(self):

        customer_id = self.get_selected_customer_id()

        if customer_id is None:
            return

        customer = self.store.find_customer(
            customer_id
        )

        if customer is None:
            return

        dialog = tk.Toplevel(self)

        dialog.title("Update Customer")
        dialog.geometry("430x380")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        data = {
            "Name": customer.name,
            "Email": customer.email,
            "Call Number": customer.call_number,
            "Address": customer.address
        }

        fields = {}

        for row, (label, value) in enumerate(data.items()):

            ttk.Label(
                frame,
                text=f"{label}:"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=7
            )

            entry = ttk.Entry(
                frame,
                width=32
            )

            entry.insert(
                0,
                str(value)
            )

            entry.grid(
                row=row,
                column=1,
                pady=7
            )

            fields[label] = entry

        def submit():

            try:

                self.store.update_customer(
                    customer_id,
                    name=fields["Name"].get().strip(),
                    email=fields["Email"].get().strip(),
                    call_number=fields[
                        "Call Number"
                    ].get().strip(),
                    address=fields[
                        "Address"
                    ].get().strip()
                )

                self.refresh_all()

                self.set_status(
                    "Customer updated successfully."
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text="Update Customer",
            command=submit
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20
        )

    def remove_customer(self):

        customer_id = self.get_selected_customer_id()

        if customer_id is None:
            return

        if not messagebox.askyesno(
            "Confirm",
            "Remove selected customer?"
        ):
            return

        try:

            result = self.store.remove_customer(
                customer_id
            )

            if result:

                self.refresh_all()

                self.set_status(
                    "Customer removed successfully."
                )

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # =====================================================
    # INVENTORY TAB
    # =====================================================

    def create_inventory_tab(self):

        tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            tab,
            text="Inventory"
        )

        toolbar = ttk.Frame(tab)
        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            toolbar,
            text="Add Inventory",
            command=self.add_inventory_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Add Stock",
            command=self.add_stock_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Remove Stock",
            command=self.remove_stock_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Set Stock",
            command=self.set_stock_dialog
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_inventory
        ).pack(side="right", padx=3)

        columns = (
            "id",
            "name",
            "category",
            "stock",
            "status"
        )

        self.inventory_tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Product ID",
            "name": "Product",
            "category": "Category",
            "stock": "Stock",
            "status": "Status"
        }

        widths = {
            "id": 100,
            "name": 220,
            "category": 180,
            "stock": 120,
            "status": 150
        }

        for column in columns:

            self.inventory_tree.heading(
                column,
                text=headings[column]
            )

            self.inventory_tree.column(
                column,
                width=widths[column]
            )

        self.inventory_tree.pack(
            fill="both",
            expand=True
        )

    def refresh_inventory(self):

        if not hasattr(self, "inventory_tree"):
            return

        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        for inventory in self.store.inventories:

            if inventory.quantity == 0:
                status = "Out of stock"

            elif inventory.quantity <= 5:
                status = "Low stock"

            else:
                status = "Available"

            self.inventory_tree.insert(
                "",
                "end",
                values=(
                    inventory.product.id,
                    inventory.product.name,
                    inventory.product.category,
                    inventory.quantity,
                    status
                )
            )

    def get_inventory_product_id(self):

        selection = self.inventory_tree.selection()

        if not selection:

            messagebox.showwarning(
                "Selection",
                "Please select an inventory item first."
            )

            return None

        values = self.inventory_tree.item(
            selection[0],
            "values"
        )

        return int(values[0])

    def add_inventory_dialog(self):

        products = [
            f"{product.id} - {product.name}"
            for product in self.store.products
        ]

        if not products:

            messagebox.showwarning(
                "Inventory",
                "Add at least one product first."
            )

            return

        dialog = tk.Toplevel(self)

        dialog.title("Add Inventory")
        dialog.geometry("400x230")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text="Product:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=10
        )

        combo = ttk.Combobox(
            frame,
            values=products,
            state="readonly",
            width=28
        )

        combo.grid(
            row=0,
            column=1,
            pady=10
        )

        combo.current(0)

        ttk.Label(
            frame,
            text="Quantity:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=10
        )

        quantity_entry = ttk.Entry(
            frame,
            width=30
        )

        quantity_entry.grid(
            row=1,
            column=1,
            pady=10
        )

        def submit():

            try:

                product_id = int(
                    combo.get().split(" - ")[0]
                )

                quantity = int(
                    quantity_entry.get()
                )

                product = self.store.find_product(
                    product_id
                )

                inventory = Inventory(
                    product,
                    quantity
                )

                self.store.add_inventory(
                    inventory
                )

                self.refresh_all()

                self.set_status(
                    "Inventory added successfully."
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text="Add Inventory",
            command=submit
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

    def stock_operation_dialog(
        self,
        operation,
        title,
        success_message
    ):

        product_id = self.get_inventory_product_id()

        if product_id is None:
            return

        dialog = tk.Toplevel(self)

        dialog.title(title)
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        product = self.store.find_product(
            product_id
        )

        ttk.Label(
            frame,
            text=f"Product: {product.name}"
        ).pack(
            pady=5
        )

        entry = ttk.Entry(
            frame,
            width=25
        )

        entry.pack(
            pady=10
        )

        def submit():

            try:

                quantity = int(
                    entry.get()
                )

                if operation == "add":

                    result = self.store.add_stock(
                        product_id,
                        quantity
                    )

                elif operation == "remove":

                    result = self.store.remove_stock(
                        product_id,
                        quantity
                    )

                else:

                    result = self.store.set_stock(
                        product_id,
                        quantity
                    )

                if result is None:

                    raise ValueError(
                        "Product or inventory was not found."
                    )

                self.refresh_all()

                self.set_status(
                    success_message
                )

                dialog.destroy()

            except (ValueError, TypeError) as error:

                messagebox.showerror(
                    "Error",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            frame,
            text=title,
            command=submit
        ).pack(
            pady=10
        )

    def add_stock_dialog(self):

        self.stock_operation_dialog(
            "add",
            "Add Stock",
            "Stock added successfully."
        )

    def remove_stock_dialog(self):

        self.stock_operation_dialog(
            "remove",
            "Remove Stock",
            "Stock removed successfully."
        )

    def set_stock_dialog(self):

        self.stock_operation_dialog(
            "set",
            "Set Stock",
            "Stock updated successfully."
        )

    # =====================================================
    # ORDERS TAB
    # =====================================================

    def create_orders_tab(self):

        tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            tab,
            text="Orders"
        )

        main_frame = ttk.Frame(tab)
        main_frame.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # LEFT SIDE - ORDER LIST
        # -------------------------------------------------

        left_frame = ttk.LabelFrame(
            main_frame,
            text="Orders",
            padding=10
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        toolbar = ttk.Frame(left_frame)
        toolbar.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh_orders
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Cancel Selected",
            command=self.cancel_selected_order
        ).pack(side="left", padx=3)

        columns = (
            "number",
            "customer",
            "status",
            "items",
            "total"
        )

        self.orders_tree = ttk.Treeview(
            left_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "number": "Order #",
            "customer": "Customer",
            "status": "Status",
            "items": "Items",
            "total": "Total"
        }

        widths = {
            "number": 80,
            "customer": 180,
            "status": 120,
            "items": 80,
            "total": 150
        }

        for column in columns:

            self.orders_tree.heading(
                column,
                text=headings[column]
            )

            self.orders_tree.column(
                column,
                width=widths[column]
            )

        self.orders_tree.pack(
            fill="both",
            expand=True
        )

        self.orders_tree.bind(
            "<Double-1>",
            lambda event: self.show_selected_order()
        )

        # -------------------------------------------------
        # RIGHT SIDE - CREATE ORDER
        # -------------------------------------------------

        right_frame = ttk.LabelFrame(
            main_frame,
            text="Create Order",
            padding=15
        )

        right_frame.pack(
            side="right",
            fill="y"
        )

        ttk.Label(
            right_frame,
            text="Customer:"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.order_customer_combo = ttk.Combobox(
            right_frame,
            state="readonly",
            width=30
        )

        self.order_customer_combo.pack(
            pady=(0, 15)
        )

        ttk.Label(
            right_frame,
            text="Product:"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.order_product_combo = ttk.Combobox(
            right_frame,
            state="readonly",
            width=30
        )

        self.order_product_combo.pack(
            pady=(0, 10)
        )

        ttk.Label(
            right_frame,
            text="Quantity:"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.order_quantity_entry = ttk.Entry(
            right_frame,
            width=33
        )

        self.order_quantity_entry.pack(
            pady=(0, 10)
        )

        ttk.Button(
            right_frame,
            text="Add Item",
            command=self.add_order_item
        ).pack(
            fill="x",
            pady=5
        )

        self.order_items_tree = ttk.Treeview(
            right_frame,
            columns=(
                "product",
                "quantity"
            ),
            show="headings",
            height=8
        )

        self.order_items_tree.heading(
            "product",
            text="Product"
        )

        self.order_items_tree.heading(
            "quantity",
            text="Qty"
        )

        self.order_items_tree.column(
            "product",
            width=190
        )

        self.order_items_tree.column(
            "quantity",
            width=60
        )

        self.order_items_tree.pack(
            pady=10
        )

        ttk.Button(
            right_frame,
            text="Remove Selected Item",
            command=self.remove_order_item
        ).pack(
            fill="x",
            pady=5
        )

        ttk.Button(
            right_frame,
            text="Create Order",
            command=self.submit_order
        ).pack(
            fill="x",
            pady=(10, 5)
        )

        ttk.Button(
            right_frame,
            text="Clear Order",
            command=self.clear_order_items
        ).pack(
            fill="x"
        )

    def refresh_orders(self):

        if not hasattr(self, "orders_tree"):
            return

        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for index, order in enumerate(
            self.store.orders,
            start=1
        ):

            self.orders_tree.insert(
                "",
                "end",
                values=(
                    index,
                    order.customer.name,
                    order.status,
                    len(order.items),
                    order.calculate_total()
                )
            )

    def refresh_order_customer_combobox(self):

        if not hasattr(
            self,
            "order_customer_combo"
        ):
            return

        values = [
            f"{customer.customer_id} - {customer.name}"
            for customer in self.store.customers
        ]

        self.order_customer_combo["values"] = values

        if values:
            self.order_customer_combo.current(0)

        else:
            self.order_customer_combo.set("")

    def refresh_order_product_combobox(self):

        if not hasattr(
            self,
            "order_product_combo"
        ):
            return

        values = [
            f"{product.id} - {product.name}"
            for product in self.store.products
        ]

        self.order_product_combo["values"] = values

        if values:
            self.order_product_combo.current(0)

        else:
            self.order_product_combo.set("")

    def add_order_item(self):

        if not self.order_customer_combo.get():

            messagebox.showwarning(
                "Order",
                "Please select a customer."
            )

            return

        if not self.order_product_combo.get():

            messagebox.showwarning(
                "Order",
                "Please select a product."
            )

            return

        try:

            product_id = int(
                self.order_product_combo
                .get()
                .split(" - ")[0]
            )

            quantity = int(
                self.order_quantity_entry.get()
            )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            product = self.store.find_product(
                product_id
            )

            if product is None:
                raise ValueError(
                    "Product not found."
                )

            self.current_order_items.append(
                (product_id, quantity)
            )

            self.order_items_tree.insert(
                "",
                "end",
                values=(
                    product.name,
                    quantity
                )
            )

            self.order_quantity_entry.delete(
                0,
                tk.END
            )

            self.set_status(
                "Item added to current order."
            )

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    def remove_order_item(self):

        selection = self.order_items_tree.selection()

        if not selection:
            return

        index = self.order_items_tree.index(
            selection[0]
        )

        self.order_items_tree.delete(
            selection[0]
        )

        del self.current_order_items[index]

    def clear_order_items(self):

        self.current_order_items.clear()

        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)

        self.set_status(
            "Current order cleared."
        )

    def submit_order(self):

        customer_text = (
            self.order_customer_combo.get()
        )

        if not customer_text:

            messagebox.showwarning(
                "Order",
                "Please select a customer."
            )

            return

        if not self.current_order_items:

            messagebox.showwarning(
                "Order",
                "Add at least one product."
            )

            return

        try:

            customer_id = int(
                customer_text.split(" - ")[0]
            )

            order = self.store.create_order(
                customer_id=customer_id,
                items=self.current_order_items.copy()
            )

            if order is None:

                messagebox.showwarning(
                    "Order",
                    "Order could not be created.\n\n"
                    "Check the product and inventory."
                )

                return

            total = order.calculate_total()

            self.clear_order_items()
            self.refresh_all()

            self.set_status(
                "Order created successfully."
            )

            messagebox.showinfo(
                "Success",
                f"Order created successfully.\n\n"
                f"Order total: {total}"
            )

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Order Error",
                str(error)
            )

    def get_selected_order_index(self):

        selection = self.orders_tree.selection()

        if not selection:

            messagebox.showwarning(
                "Selection",
                "Please select an order."
            )

            return None

        values = self.orders_tree.item(
            selection[0],
            "values"
        )

        displayed_number = int(
            values[0]
        )

        # Store.find_order uses zero-based index.
        return displayed_number - 1

    def show_selected_order(self):

        order_index = self.get_selected_order_index()

        if order_index is None:
            return

        order = self.store.find_order(
            order_index
        )

        if order is None:
            return

        dialog = tk.Toplevel(self)

        dialog.title(
            f"Order #{order_index + 1}"
        )

        dialog.geometry("550x500")

        frame = ttk.Frame(
            dialog,
            padding=20
        )

        frame.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            frame,
            text=f"Customer: {order.customer.name}",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=5
        )

        ttk.Label(
            frame,
            text=f"Status: {order.status}"
        ).pack(
            anchor="w",
            pady=5
        )

        columns = (
            "product",
            "quantity",
            "unit_price",
            "total"
        )

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=12
        )

        tree.heading(
            "product",
            text="Product"
        )

        tree.heading(
            "quantity",
            text="Qty"
        )

        tree.heading(
            "unit_price",
            text="Unit Price"
        )

        tree.heading(
            "total",
            text="Total"
        )

        tree.pack(
            fill="both",
            expand=True,
            pady=15
        )

        for item in order.items:

            tree.insert(
                "",
                "end",
                values=(
                    item.product.name,
                    item.quantity,
                    item.unit_price,
                    item.calculate_price()
                )
            )

        ttk.Label(
            frame,
            text=f"Order Total: {order.calculate_total()}",
            style="Section.TLabel"
        ).pack(
            anchor="e",
            pady=10
        )

    def cancel_selected_order(self):

        order_index = self.get_selected_order_index()

        if order_index is None:
            return

        if not messagebox.askyesno(
            "Confirm",
            "Cancel selected order?"
        ):
            return

        try:

            result = self.store.cancel_order(
                order_index
            )

            if result is not None:

                self.refresh_all()

                self.set_status(
                    "Order cancelled successfully."
                )

        except (ValueError, TypeError) as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # =====================================================
    # REPORTS TAB
    # =====================================================

    def create_reports_tab(self):

        tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            tab,
            text="Reports"
        )

        self.report_frame = tab

        self.sales_frame = ttk.LabelFrame(
            tab,
            text="Sales Report",
            padding=15
        )

        self.sales_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.low_stock_frame = ttk.LabelFrame(
            tab,
            text="Low Stock",
            padding=15
        )

        self.low_stock_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.out_stock_frame = ttk.LabelFrame(
            tab,
            text="Out of Stock",
            padding=15
        )

        self.out_stock_frame.pack(
            fill="x"
        )

    def refresh_reports(self):

        if not hasattr(
            self,
            "sales_frame"
        ):
            return

        # Clear frames
        for widget in self.sales_frame.winfo_children():
            widget.destroy()

        for widget in self.low_stock_frame.winfo_children():
            widget.destroy()

        for widget in self.out_stock_frame.winfo_children():
            widget.destroy()

        # -------------------------------------------------
        # SALES REPORT
        # -------------------------------------------------

        sales_data = [
            (
                "Total Orders",
                self.store.number_of_orders()
            ),
            (
                "Completed Orders",
                self.store.number_of_completed_orders()
            ),
            (
                "Pending Orders",
                self.store.number_of_pending_orders()
            ),
            (
                "Cancelled Orders",
                self.store.number_of_cancelled_orders()
            ),
            (
                "Total Sales",
                self.store.total_sales()
            )
        ]

        for row, (label, value) in enumerate(
            sales_data
        ):

            ttk.Label(
                self.sales_frame,
                text=f"{label}:",
                font=("Arial", 11, "bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=15,
                pady=4
            )

            ttk.Label(
                self.sales_frame,
                text=str(value)
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=15,
                pady=4
            )

        # -------------------------------------------------
        # LOW STOCK
        # -------------------------------------------------

        low_stock_items = self.store.low_stock(5)

        if not low_stock_items:

            ttk.Label(
                self.low_stock_frame,
                text="No low-stock products found."
            ).pack(
                anchor="w"
            )

        else:

            for inventory in low_stock_items:

                ttk.Label(
                    self.low_stock_frame,
                    text=(
                        f"{inventory.product.name}   "
                        f"Stock: {inventory.quantity}"
                    )
                ).pack(
                    anchor="w",
                    pady=2
                )

        # -------------------------------------------------
        # OUT OF STOCK
        # -------------------------------------------------

        out_stock_items = self.store.out_of_stock()

        if not out_stock_items:

            ttk.Label(
                self.out_stock_frame,
                text="No out-of-stock products found."
            ).pack(
                anchor="w"
            )

        else:

            for inventory in out_stock_items:

                ttk.Label(
                    self.out_stock_frame,
                    text=inventory.product.name
                ).pack(
                    anchor="w",
                    pady=2
                )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    app = StoreApp()
    app.mainloop()

