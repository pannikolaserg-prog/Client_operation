import pytest

from src.mask import get_mask_account, get_mask_card_number


def test_mask_standard_card_number() -> None:
    """Тест маскирования стандартного номера карты (16 цифр)"""
    card_number: str = "1234567890123456"
    expected: str = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected


def test_mask_mastercard_number() -> None:
    """Тест маскирования номера Mastercard"""
    card_number: str = "5555555555554444"
    expected: str = "5555 55** **** 4444"
    assert get_mask_card_number(card_number) == expected


def test_mask_short_card_number() -> None:
    """Тест маскирования короткого номера карты (граничный случай)"""
    card_number: str = "1234567890"  # 10 цифр
    expected: str = "1234 56** **** 7890"
    assert get_mask_card_number(card_number) == expected


def test_very_long_card_number() -> None:
    """Тест маскирования очень длинного номера карты"""
    card_number: str = "123456789012345678901234567890"
    expected: str = "1234 56** **** 7890"
    assert get_mask_card_number(card_number) == expected


def test_empty_card_number() -> None:
    """Тест обработки пустой строки"""
    card_number: str = ""
    expected: str = " **** **** **** "
    assert get_mask_card_number(card_number) == expected


def test_mask_standard_account_number() -> None:
    """Тест маскирования стандартного номера счета (20 цифр)"""
    account_number: str = "12345678901234567890"
    expected: str = "**7890"
    assert get_mask_account(account_number) == expected


def test_mask_minimum_length_account() -> None:
    """Тест маскирования номера счета минимальной длины"""
    test_cases: list[tuple[str, str]] = [
        ("123", "**123"),  # 3 цифры
        ("12", "**12"),  # 2 цифры
        ("1", "**1"),  # 1 цифра
    ]

    for account_number, expected in test_cases:
        assert get_mask_account(account_number) == expected


def test_empty_account_number() -> None:
    """Тест обработки пустой строки"""
    account_number: str = ""
    expected: str = "**"
    assert get_mask_account(account_number) == expected


def test_very_long_account_number() -> None:
    """Тест маскирования очень длинного номера счета"""
    account_number: str = "1234567890123456789012345678901234567890"
    expected: str = "**7890"
    assert get_mask_account(account_number) == expected
