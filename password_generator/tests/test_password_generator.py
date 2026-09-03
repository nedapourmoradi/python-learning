"""Tests for the password generator."""

import pytest

import password_generator


def test_generate_rules_for_all_password_types():
    """Return correct rules for supported password types."""
    assert password_generator.generate_rules("pin") == {
        "number": True,
        "separator": "",
    }

    assert password_generator.generate_rules("random") == {
        "number": True,
        "uppercase": True,
        "symbol": True,
        "separator": "",
    }

    assert password_generator.generate_rules("memorable") == {
        "word": True,
        "word_length": 4,
        "separator": "-",
    }


@pytest.mark.parametrize(
    "password_type,length",
    [
        ("pin", 6),
        ("random", 10),
    ],
)
def test_validate_password_length_success(password_type, length):
    """Accept valid password lengths."""
    password_generator.validate_password_length(
        password_type,
        length,
    )


@pytest.mark.parametrize(
    "password_type,length",
    [
        ("pin", 0),
        ("random", 2),
        ("pin", password_generator.MAX_PASSWORD_LENGTH + 1),
        ("random", password_generator.MAX_PASSWORD_LENGTH + 1),
    ],
)
def test_validate_password_length_failure(password_type, length):
    """Reject invalid password lengths."""
    with pytest.raises(ValueError):
        password_generator.validate_password_length(
            password_type,
            length,
        )


def test_generate_pin_success():
    """Generate a numeric password with requested length."""
    rules = password_generator.generate_rules("pin")

    password = password_generator.generate_pin(
        rules,
        length=6,
    )

    assert len(password) == 6
    assert password.isdigit()


def test_generate_pin_failure():
    """Reject PIN generation without number rule."""
    rules = password_generator.generate_rules("pin")
    rules["number"] = False

    with pytest.raises(
        ValueError,
        match="PIN must contain numbers",
    ):
        password_generator.generate_pin(
            rules,
            length=6,
        )


def test_generate_random_password_success():
    """Generate password containing required characters."""
    rules = password_generator.generate_rules("random")

    password = password_generator.generate_random_password(
        rules,
        length=10,
    )

    assert len(password) == 10
    assert any(char.isdigit() for char in password)
    assert any(char.isupper() for char in password)
    assert any(
        char in password_generator.SYMBOLS
        for char in password
    )


def test_generate_random_password_failure():
    """Reject random password with insufficient length."""
    rules = password_generator.generate_rules("random")

    with pytest.raises(ValueError):
        password_generator.generate_random_password(
            rules,
            length=2,
        )


def test_generate_memorable_password_success(monkeypatch):
    """Generate memorable password from valid words."""
    rules = password_generator.generate_rules("memorable")

    monkeypatch.setattr(
        password_generator,
        "valid_words",
        [
            "blue",
            "calm",
            "kind",
        ],
    )

    password = password_generator.generate_memorable_password(
        rules,
        count=2,
    )

    words = password.split("-")

    assert "-" in password
    assert all(
        len(word) == rules["word_length"]
        for word in words
    )


def test_generate_memorable_password_failure():
    """Reject memorable password without enough words."""
    with pytest.raises(
        ValueError,
        match="Not enough unique items",
    ):
        password_generator.select_unique_random_items(
            ["blue"],
            count=2,
        )


@pytest.mark.parametrize(
    "password_type,password,count,length,expected",
    [
        ("pin", "1234", 0, 4, True),
        ("pin", "12a4", 0, 4, False),
        ("random", "Ab1@test", 0, 8, True),
        ("memorable", "blue-calm", 2, 0, True),
        ("memorable", "blue--calm", 2, 0, False),
    ],
)
def test_validate_password(
    password_type,
    password,
    count,
    length,
    expected,
):
    """Accept valid and reject invalid generated passwords."""
    rules = password_generator.generate_rules(
        password_type,
    )

    result = password_generator.validate_password(
        password,
        rules,
        password_type,
        count=count,
        length=length,
    )

    assert result is expected


@pytest.mark.parametrize(
    "password_type,kwargs,expected",
    [
        ("pin", {"length": 6}, "123456"),
        ("random", {"length": 10}, "Ab1@testxy"),
        ("memorable", {"count": 2}, "blue-calm"),
    ],
)
def test_generate_retry_success(
    monkeypatch,
    password_type,
    kwargs,
    expected,
):
    """Return a valid password before exhausting retry attempts."""
    generators = {
        "pin": "generate_pin",
        "random": "generate_random_password",
        "memorable": "generate_memorable_password",
    }

    monkeypatch.setattr(
        password_generator,
        generators[password_type],
        lambda *args, **kwargs: expected,
    )

    result = password_generator.generate_retry(
        password_type,
        password_generator.generate_rules(password_type),
        **kwargs,
    )

    assert result == expected


@pytest.mark.parametrize(
    "password_type,kwargs",
    [
        ("pin", {"length": 4}),
        ("random", {"length": 10}),
        ("memorable", {"count": 2}),
    ],
)
def test_generate_retry_reaches_max_attempts(
    monkeypatch,
    password_type,
    kwargs,
):
    """Raise error after all retry attempts fail."""
    generators = {
        "pin": "generate_pin",
        "random": "generate_random_password",
        "memorable": "generate_memorable_password",
    }

    monkeypatch.setattr(
        password_generator,
        generators[password_type],
        lambda *args, **kwargs: "invalid",
    )

    with pytest.raises(ValueError):
        password_generator.generate_retry(
            password_type,
            password_generator.generate_rules(password_type),
            max_attempts=3,
            **kwargs,
        )


def test_generate_retry_invalid_max_attempts():
    """Reject invalid maximum attempts."""
    with pytest.raises(
        ValueError,
        match="Max attempts must be a positive integer",
    ):
        password_generator.generate_retry(
            "pin",
            password_generator.generate_rules("pin"),
            length=4,
            max_attempts=0,
        )


def test_generate_retry_invalid_password_type():
    """Reject unsupported password type."""
    with pytest.raises(
        ValueError,
        match="Invalid password type",
    ):
        password_generator.generate_retry(
            "unknown",
            {},
            length=4,
        )


def test_get_positive_integer_retries(monkeypatch):
    """Retry input until a positive integer is entered."""
    values = iter(
        [
            "abc",
            "0",
            "5",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(values),
    )

    assert (
        password_generator.get_positive_integer(
            "Length: "
        )
        == 5
    )


def test_get_password_type_retries(monkeypatch):
    """Retry input until valid password type is entered."""
    values = iter(
        [
            "invalid",
            " RANDOM ",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(values),
    )

    assert password_generator.get_password_type() == "random"