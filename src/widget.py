from src.mask import get_mask_account, get_mask_card_number


def mask_account_card(bank_data: str) -> str:
    """
    Функция определяет тип банковских данных (карта или счет)
    и применяет соответствующую маскировку
    """
    # Разделяем входную строку на части
    parts = bank_data.split()

    # Извлекаем номер (последний элемент)
    number = parts[-1]

    # Извлекаем название (все кроме номера)
    name = " ".join(parts[:-1])

    # Определяем тип данных и применяем маскировку
    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        # Это карта (Visa, MasterCard, Maestro, Mir и т.д.)
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату через строковые операции
    """
    try:
        # Разделяем дату и время
        date_part = date_string.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        return "Некорректный формат даты"


# Примеры использования
if __name__ == "__main__":
    # Тестовые данные
    test_cases = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    for test in test_cases:
        result = mask_account_card(test)
        print(f"{test} -> {result}")

print(get_date("2023-12-25T10:30:00"))
print(get_date("2024-01-15T14:45:00"))

