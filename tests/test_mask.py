import pytest

from src.mask import get_mask_account, get_mask_card_number


def test_mask_standard_card_number():
    """Тест маскирования стандартного номера карты (16 цифр)"""
    card_number = "1234567890123456"
    expected = "1234 56** **** 3456"
    assert get_mask_card_number(card_number) == expected


def test_mask_mastercard_number():
    """Тест маскирования номера Mastercard"""
    card_number = "5555555555554444"
    expected = "5555 55** **** 4444"
    assert get_mask_card_number(card_number) == expected


def test_mask_short_card_number():
    """Тест маскирования короткого номера карты (граничный случай)"""
    card_number = "1234567890"  # 10 цифр
    expected = "1234 56** **** 7890"
    assert get_mask_card_number(card_number) == expected


def test_very_long_card_number():
    """Тест маскирования очень длинного номера карты"""
    card_number = "123456789012345678901234567890"
    expected = "1234 56** **** 7890"
    assert get_mask_card_number(card_number) == expected


def test_empty_card_number():
    """Тест обработки пустой строки"""
    card_number = ""
    expected = " **** **** **** "
    assert get_mask_card_number(card_number) == expected


def test_mask_standard_account_number():
    """Тест маскирования стандартного номера счета (20 цифр)"""
    account_number = "12345678901234567890"
    expected = "**7890"
    assert get_mask_account(account_number) == expected


def test_mask_minimum_length_account():
    """Тест маскирования номера счета минимальной длины"""
    test_cases = [
        ("123", "**123"),  # 3 цифры
        ("12", "**12"),  # 2 цифры
        ("1", "**1"),  # 1 цифра
    ]

    for account_number, expected in test_cases:
        assert get_mask_account(account_number) == expected


def test_empty_account_number():
    """Тест обработки пустой строки"""
    account_number = ""
    expected = "**"
    assert get_mask_account(account_number) == expected


def test_very_long_account_number():
    """Тест маскирования очень длинного номера счета"""
    account_number = "1234567890123456789012345678901234567890"
    expected = "**7890"
    assert get_mask_account(account_number) == expected
