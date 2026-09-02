import secrets
import string
from collections.abc import Sequence

from nltk.corpus import words


def select_random_items(items: Sequence, count: int) -> list:
    selected_items = []

    for _ in range(count):
        selected_items.append(secrets.choice(items))

    return selected_items

def select_unique_random_items(items: Sequence, count: int) -> list:
    if count > len(items):
        raise ValueError("Not enough unique items available!")

    return secrets.SystemRandom().sample(items, count)


def generate_rules(password_type):
    if password_type == "pin":
        rules = {
        "number" : True,
        "separator" : "",
        }
        

    elif password_type == "random":
        rules = {
        "number": True,
        "uppercase": True,
        "symbol": True,
        "separator": "",
        }
    elif password_type =="memorable":
        rules = {
            "word" : True,
            "word_length" : 4,
            "separator" : "-",
        }

    else:
        raise ValueError("Invalid password type")

    return rules

def generate_pin(rules, length: int = 4) -> str:
    if not rules["number"]:
        raise ValueError("PIN must contain numbers!")

    return "".join(select_random_items(string.digits, length))


SYMBOLS = "!@#$%^&*"
MAX_PASSWORD_LENGTH = 50    

def generate_random_password(rules, length: int = 8) -> str:
    items = string.digits + string.ascii_letters + SYMBOLS

    required_count = 0
    password_chars = []

    if rules["number"]:
        required_count += 1
        password_chars.append(secrets.choice(string.digits))

    if rules["uppercase"]:
        required_count += 1
        password_chars.append(secrets.choice(string.ascii_uppercase))

    if rules["symbol"]:
        required_count += 1
        password_chars.append(secrets.choice(SYMBOLS))

    if length < required_count:
        raise ValueError("The length is too low!")

    remaining = length - len(password_chars)

    for _ in range(remaining):
        password_chars.append(secrets.choice(items))
    

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


word_list = words.words()
rules = generate_rules("memorable")

valid_words = [
    word.lower()
    for word in word_list
    if len(word) == rules["word_length"] and word.isalpha()
]

def generate_memorable_password(rules, count: int) -> str:
    selected_words = select_unique_random_items(valid_words, count)

    if not rules["word"]:
        raise ValueError("Password must contain words!")

    return rules["separator"].join(selected_words)


def validate_password(
    password: str, 
    rules: dict, 
    password_type: str, 
    count: int, 
    length: int
) -> bool:

    if password_type == "pin":
        if rules["number"] and not all(char in string.digits for char in password):
            return False

        if len(password) != length:
            return False
        
    elif password_type == "random":
        if rules["number"] and not any(char in string.digits for char in password):
            return False
        
        if rules["uppercase"] and not any(char in string.ascii_uppercase for char in password):
            return False

        if rules["symbol"] and not any(char in SYMBOLS for char in password):
            return False

        if len(password) != length:
            return False

        if rules["separator"] and rules["separator"] in password:
            return False

    elif password_type == "memorable":
        separator = rules["separator"]

        if separator not in password:
            return False

        if password.startswith(separator) or password.endswith(separator):
            return False

        if separator * 2 in password:
            return False

        words = password.split(separator)
    
        if len(words) != count:
            return False
        
        if rules["word"]:
            for word in words:
                if not word.isalpha():
                    return False
               
                if len(word) != rules["word_length"]:
                    return False

    return True


def generate_retry(
    password_type: str,
    rules: dict,
    length: int = 0, 
    count: int = 0,
    max_attempts: int = 50
):

    if not isinstance(max_attempts, int) or max_attempts <= 0:
        raise ValueError("Max attempts must be a positive integer.")

    if password_type == "pin":
        for _ in range(max_attempts):
            password = generate_pin(rules, length)

            if validate_password(
                password,
                rules,
                "pin",
                count=0,
                length=length
            ):
                return password

        raise ValueError("Failed to generate a valid PIN!")

    elif password_type == "random":
        for _ in range(max_attempts):
            password = generate_random_password(rules, length)

            if validate_password(
                password,
                rules,
                "random",
                count=0,
                length=length
            ):
                return password

        raise ValueError("Failed to generate a valid Random Password!")

    elif password_type == "memorable":

        if not isinstance(count, int) or count <= 0:
            raise ValueError("Count must be a positive integer.")

        for _ in range(max_attempts):
            password = generate_memorable_password(rules, count)

            if validate_password(
                password,
                rules,
                "memorable",
                count=count,
                length=0
            ):
                return password

        raise ValueError("Failed to generate a valid Memorable Password!")

    else:
        raise ValueError("Invalid password type!")


def get_positive_integer(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Please enter a positive integer.")

        except ValueError:
            print("Please enter a valid integer.")

    

def validate_password_length(
    password_type: str,
    length: int
) -> None:

    if length > MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length cannot exceed {MAX_PASSWORD_LENGTH}."
        )

    if password_type == "pin":
        if length < 1:
            raise ValueError(
                "PIN length must be at least 1."
            )

    elif password_type == "random" and length < 3:
        raise ValueError(
            "Random password length must be at least 3."
        )

def get_password_type() -> str:
    while True:
        password_type = input(
            "Enter password type (pin, random, memorable): "
        ).strip().lower()

        if password_type in ["pin", "random", "memorable"]:
            return password_type

        print("Invalid password type. Please try again.")




if __name__ == "__main__":

    password_type = get_password_type()

    if password_type in ("pin", "random"):

        while True:
            length = get_positive_integer(
            "Enter your preferred password length: "
                    )
            try:
                validate_password_length(password_type, length)
                break

            except ValueError as error:
                print(error)

        rules = generate_rules(password_type)

        result = generate_retry(
            password_type,
            rules,
            length=length
        )

    elif password_type == "memorable":

        count = get_positive_integer(
            "Enter your preferred words count: "
        )

        rules = generate_rules(password_type)

        result = generate_retry(
            password_type,
            rules,
            count=count
        )
    else:
        raise ValueError("Invalid password type")

    print(result)
