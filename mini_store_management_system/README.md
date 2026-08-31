# Mini Store Management System

A Python-based store management system designed to practice and demonstrate **Object-Oriented Programming (OOP)**, problem-solving, data validation, inventory management, order processing, JSON persistence, automated testing, reporting, and a Tkinter-based graphical user interface.

The project simulates the core operations of a small store while focusing on **problem decomposition, responsibility assignment, business-rule implementation, state management, data consistency, testing, and iterative refinement**.

---

## Features

### Product Management

- Add, update, find, and remove products
- Product ID validation
- Product price validation
- Product information display

### Customer Management

- Add, update, find, and remove customers
- Customer ID validation
- Customer information display
- Prevent removal of customers with existing orders

### Inventory Management

- Add inventory for registered products
- Check available stock
- Add, remove, and set stock quantities
- Validate stock operations
- Detect low-stock products
- Detect out-of-stock products

### Order Management

- Create orders for registered customers
- Add multiple products to an order
- Validate products and quantities
- Validate required stock before order creation
- Prevent orders with insufficient stock
- Calculate order totals
- Manage order states
- Prevent invalid order-state transitions
- Preserve historical product prices in existing orders

### Data Persistence

- JSON serialization and deserialization
- Save and load store data
- Preserve products, customers, inventory, and orders
- Preserve historical order prices
- Handle missing or invalid JSON data

### Reporting

- Total sales
- Total orders
- Completed orders
- Cancelled orders
- Pending orders
- Low-stock products
- Out-of-stock products

### Graphical User Interface

A Tkinter-based GUI provides separate sections for:

- Products
- Customers
- Inventory
- Orders
- Reports

The GUI uses the same business logic as the core application rather than duplicating store operations.

---

## Problem-Solving Approach

The project was developed by approaching the store management system as a software problem rather than starting directly with implementation.

The solution was built through a sequence of analysis, decomposition, design, implementation, testing, and refinement.

### 1. Problem Definition

The initial problem was to design a small store management system capable of handling products, customers, inventory, orders, and store operations while maintaining valid application state.

The system also needed to support persistence, reporting, testing, and user interaction.

### 2. Problem Decomposition

The overall problem was divided into smaller domains:

```text
Store Management System
│
├── Product Management
├── Customer Management
├── Inventory Management
├── Order Management
├── Persistence
├── Reporting
└── User Interface
```

Breaking the problem into separate areas made it possible to reason about each responsibility independently.

### 3. Responsibility Assignment

Responsibilities were assigned to separate classes and components:

```text
Product
    → Product information and validation

Customer
    → Customer information and validation

Inventory
    → Stock management

OrderItem
    → Product quantity and item price

Order
    → Order items, total, and state

Store
    → Coordination and business operations

StorePersistence
    → JSON serialization and persistence

UI
    → User interaction
```

This reduced unnecessary coupling and helped keep responsibilities separated.

### 4. Relationship Design

The relationships between entities were identified before implementing the corresponding operations.

```text
Customer
    ↓
  Order
    ↓
OrderItem
    ↓
 Product
```

and:

```text
Product
    ↓
Inventory
```

The `Store` coordinates these entities and their interactions.

### 5. Business Rules

Important business rules were identified and implemented explicitly.

Examples include:

- Products must pass validation before being added or updated.
- Customers must be valid before creating orders.
- Products in an order must exist in the store.
- Order quantities must be valid.
- Sufficient stock must exist before an order is created.
- Invalid order-state transitions must be rejected.
- Customers with existing orders cannot be removed.
- Historical order prices must remain independent of later product-price changes.

### 6. State Consistency

Operations that modify multiple parts of the system were designed around state consistency.

For order creation, the system validates the required information before modifying inventory or storing the order.

```text
Customer Validation
        ↓
Product Validation
        ↓
Quantity Validation
        ↓
Stock Validation
        ↓
Order Creation
        ↓
Inventory Update
        ↓
Store Order
```

When validation fails:

```text
Validation Failure
        ↓
Order Rejected
        ↓
Inventory Unchanged
        ↓
Order Not Added
```

This prevents failed operations from leaving the store in a partially modified state.

### 7. Implementation

After the requirements and design were established, the system was implemented using Python and Object-Oriented Programming principles.

The implementation was separated into business logic, persistence, user interface, and automated tests.

### 8. Testing and Refinement

The implementation was tested against valid operations, invalid inputs, failure scenarios, and edge cases.

Problems identified during implementation and testing were used to refine the system and improve its behavior and consistency.

The overall development process was:

```text
Problem
   ↓
Requirements
   ↓
Decomposition
   ↓
Responsibilities
   ↓
Relationships
   ↓
Business Rules
   ↓
Implementation
   ↓
Testing
   ↓
Refinement
```

---

## Architecture & Design

The system is organized around several cooperating components:

```text
Mini Store Management System
│
├── Product
├── Customer
├── Inventory
├── OrderItem
├── Order
├── Store
├── StorePersistence
├── UI
└── Tests
```

### Product

Represents a product available in the store.

Main information includes:

- Name
- ID
- Category
- Price
- Brand

The class is responsible for product information, validation, and product-level operations.

### Customer

Represents a customer who can create orders.

Main information includes:

- Name
- Email
- Phone number
- Address
- Customer ID

The class manages customer information and validation.

### Inventory

Manages stock associated with products.

Responsibilities include:

- Checking available stock
- Adding stock
- Removing stock
- Setting stock
- Validating stock operations
- Detecting low-stock products
- Detecting out-of-stock products

### OrderItem

Represents a product and its requested quantity within an order.

The item price is calculated as:

```text
item price = product price × quantity
```

### Order

Represents a customer's order.

Main attributes include:

- Customer
- Items
- Status

Supported states include:

```text
pending
completed
cancelled
```

The class is responsible for managing order items, calculating totals, and controlling valid state transitions.

### Store

Acts as the central coordinator of the application.

It maintains:

```text
products
customers
inventories
orders
```

The `Store` coordinates operations such as:

- Finding products
- Finding customers
- Finding inventory
- Adding products
- Adding customers
- Adding inventory
- Creating orders
- Adding orders
- Generating reports

### StorePersistence

Responsible for saving and restoring store data using JSON.

```text
Application
     ↓
Store
     ↓
StorePersistence
     ↓
JSON File
```

### Separation of Responsibilities

The system separates:

```text
Business Logic
      │
      ├── Store
      ├── Product
      ├── Customer
      ├── Inventory
      └── Order
           
Persistence
      │
      └── StorePersistence

Presentation
      │
      └── Tkinter UI

Verification
      │
      └── unittest
```

This makes the core business logic reusable independently of the graphical interface.

---

## Core Workflows

### Order Creation

A typical order workflow is:

```text
1. Customer is selected
        ↓
2. Products are selected
        ↓
3. Quantities are provided
        ↓
4. Customer is validated
        ↓
5. Products are validated
        ↓
6. Quantities are validated
        ↓
7. Required stock is validated
        ↓
8. Order is created
        ↓
9. Inventory is updated
        ↓
10. Order is added to Store
```

### Failed Order

If customer, product, quantity, or stock validation fails:

```text
Invalid Input / Insufficient Stock
        ↓
Order Rejected
        ↓
Inventory Unchanged
        ↓
No Order Created
```

This behavior helps maintain consistency between inventory and orders.

### Order State Management

Orders follow controlled state transitions.

For example:

```text
pending
   ├──→ completed
   └──→ cancelled
```

Invalid transitions are rejected.

### Historical Pricing

When an order is created, the order item preserves the applicable product price at the time of the transaction.

Therefore, changing a product's current price does not incorrectly change the value of an existing order.

```text
Product Price
      ↓
Order Creation
      ↓
Historical Order Item Price
      ↓
Existing Order Remains Consistent
```

---

## Data Persistence

Store data can be serialized and persisted using JSON.

The persistence layer stores and restores:

- Products
- Customers
- Inventory
- Orders
- Historical order prices

The application also handles missing or invalid JSON data during loading.

The general persistence flow is:

```text
Store State
    ↓
Serialization
    ↓
JSON File
    ↓
Deserialization
    ↓
Restored Store State
```

---

## Reporting

The system provides reports based on the current store state.

Available reports include:

- Total sales
- Total orders
- Completed orders
- Cancelled orders
- Pending orders
- Low-stock products
- Out-of-stock products

These reports demonstrate how application state can be transformed into useful business information.

---

## Testing

The project includes automated tests using Python's built-in `unittest` framework.

The tests cover:

- Product creation and validation
- Product updates
- Customer creation and validation
- Customer operations
- Inventory operations
- Stock validation
- Order item price calculation
- Order total calculation
- Order status management
- Order status transitions
- Successful order creation
- Failed order creation
- Invalid customer handling
- Invalid product handling
- Insufficient-stock scenarios
- Inventory consistency
- Duplicate products and customers
- JSON serialization and deserialization
- JSON persistence
- Store operations
- Reporting
- Edge cases and invalid inputs

The test suite focuses not only on successful operations but also on failure scenarios and state consistency.

---

## User Interface

The project includes a graphical user interface implemented with Python's `Tkinter`.

The UI provides access to the main store functionality while keeping presentation and business logic separated.

This allows the underlying store operations to be reused without depending on the graphical interface.

---

## Project Structure

The current project structure is:

```text
mini_store_management_system/
│
├── src/
│   ├── mini_store_management_system.py
│   ├── mini_store_management_system_sphinx.py
│   └── mini_store_management_system_ui.py
│
├── tests/
│   └── test_mini_store_management_system.py
│
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

### Source Files

**`src/mini_store_management_system.py`**

Main business-logic implementation.

**`src/mini_store_management_system_sphinx.py`**

Sphinx-documented version of the project using Sphinx-style docstrings.

**`src/mini_store_management_system_ui.py`**

Tkinter graphical user interface.

**`tests/test_mini_store_management_system.py`**

Automated test suite.

---

## Requirements

- Python 3.10+
- Tkinter for the graphical interface
- No external Python packages are required for the core application

The project primarily uses Python's standard library.

> On some Linux distributions, Tkinter may need to be installed separately.

---

## How to Run

### Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd python-learning/mini_store_management_system
```

### Run the Core Application

```bash
python src/mini_store_management_system.py
```

### Run the Graphical Interface

```bash
python src/mini_store_management_system_ui.py
```

### Run the Tests

```bash
python -m unittest discover -s tests -v
```

---

## Key Concepts Practiced

This project provided practical experience with:

- Python fundamentals
- Object-Oriented Programming
- Encapsulation
- Object relationships
- Responsibility assignment
- Problem decomposition
- Input validation
- Exception handling
- State management
- Business logic
- Collection management
- File handling
- JSON serialization
- JSON deserialization
- Data persistence
- Automated testing
- Edge-case testing
- GUI development with Tkinter
- Separation of business logic and UI
- Basic software architecture
- Git and GitHub workflow

---

## What This Project Demonstrates

This project demonstrates more than the implementation of a collection of Python classes.

It demonstrates an end-to-end approach to solving a software problem:

- Analyzing requirements before implementation
- Decomposing a larger problem into manageable components
- Assigning clear responsibilities to classes
- Designing relationships between objects
- Translating business rules into application logic
- Maintaining consistency across state-changing operations
- Handling invalid inputs and failure scenarios
- Persisting application state
- Testing both successful and unsuccessful behaviors
- Separating business logic from the user interface
- Refining the implementation based on testing and debugging

The project therefore serves as a practical example of **problem analysis, software design, implementation, testing, and iterative refinement**, rather than simply demonstrating Python syntax.

---

## Future Improvements

Possible extensions include:

- Database integration using SQLite or PostgreSQL
- Authentication and user roles
- Advanced product search and filtering
- Customer order history
- More detailed reporting
- Logging
- REST API
- FastAPI backend
- Web-based frontend
- CI/CD integration
- Database-backed persistence

These improvements could evolve the project from a learning-oriented store application into a more complete backend system.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.