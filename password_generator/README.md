# Password Generator

A Python-based password generator that creates different types of passwords using predefined rules, validation logic, and retry mechanisms.

This project was developed to practice problem solving, modular design, input validation, error handling, documentation, and automated testing using Python.

---

## Project Overview

The purpose of this project is to generate passwords based on different user requirements while ensuring that generated passwords satisfy their defined rules.

The application supports three password generation strategies:

* PIN passwords
* Random passwords
* Memorable passwords

Each password type has its own generation logic and validation requirements.

---

# Features

## Supported Password Types

### PIN Password

Generates numeric passwords with a specified length.

Example:

```
123456
```

---

### Random Password

Generates passwords using required character categories:

* Numbers
* Uppercase letters
* Symbols

Example:

```
Ab1@testxy
```

---

### Memorable Password

Generates passwords by combining random words with a separator.

Example:

```
blue-calm
```

---

# Problem Solving Approach

The project was developed through an incremental problem-solving process.

## 1. Breaking Down the Problem

The password generation problem was divided into smaller responsibilities:

* Defining password rules
* Generating different password types
* Validating generated passwords
* Handling invalid inputs
* Retrying failed generations

This approach helped keep each part of the program focused on a specific task.

---

## 2. Designing Independent Components

Instead of creating one large password generation function, the logic was separated into smaller functions with clear responsibilities.

Examples:

| Responsibility               | Function                                        |
| ---------------------------- | ----------------------------------------------- |
| Define password requirements | `generate_rules()`                              |
| Generate PIN passwords       | `generate_pin()`                                |
| Generate random passwords    | `generate_random_password()`                    |
| Generate memorable passwords | `generate_memorable_password()`                 |
| Validate generated passwords | `validate_password()`                           |
| Retry failed generations     | `generate_retry()`                              |
| Handle user input            | `get_positive_integer()`, `get_password_type()` |
| Validate password length     | `validate_password_length()`                    |

---

# Design Approach

## Single Responsibility Principle

The project follows the idea of separating responsibilities by assigning each function a specific purpose.

For example:

* Password generation functions are responsible only for creating passwords.
* Validation functions are responsible only for checking generated results.
* Input functions are responsible only for collecting and validating user input.
* Retry logic is separated from generation logic.

This separation improves:

* Readability
* Maintainability
* Testability
* Future extensibility

---

# Project Structure

```
password_generator/

│
├── src/
│   └── password_generator.py
│
├── tests/
│   └── test_password_generator.py
│
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Technologies Used

* Python 3
* pytest

Python standard libraries:

* `secrets`
* `string`
* `collections.abc`

External dependency:

* `nltk`
* pytest (testing)
---

# How to Run

## Install Dependencies

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd password_generator
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Application

Run the main program:

```bash
python src/password_generator.py
```

The program will ask for:

1. Password type:

```
pin
random
memorable
```

2. Required length or number of words

The program validates the input and generates a password based on the selected rules.

---

# Testing

The project uses `pytest` for automated testing.

Run tests:

```bash
pytest
```

The test suite covers:

* Password rule generation
* Password length validation
* Successful password generation
* Invalid generation scenarios
* Password validation logic
* Retry mechanism
* Maximum retry handling
* User input validation

---

# Error Handling

The project includes validation and error handling for cases such as:

* Invalid password types
* Invalid password lengths
* Unsupported generation rules
* Failed password generation attempts
* Invalid user inputs

---

# Learning Outcomes

Through this project, I practiced:

* Breaking a problem into smaller software components
* Applying separation of responsibilities
* Writing reusable functions
* Designing validation logic
* Handling edge cases
* Writing automated tests with pytest
* Debugging through test failures
* Structuring a Python project using a professional repository layout

---

# Future Improvements

Possible future improvements:

* Add a command-line interface with arguments
* Add configurable password rules
* Improve password strength evaluation
* Add continuous integration workflow
* Add more advanced testing strategies

---

# Author

Neda Pourmoradi

Python Developer / Machine Learning Student
