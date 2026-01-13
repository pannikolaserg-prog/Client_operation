def get_mask_card_number(number_card: str) -> str:
    """Функция принимает номер карты и возвращает его в замаскированном виде"""
    if not number_card:
        return " **** **** **** "

    # Для очень коротких номеров (меньше 6 символов)
    if len(number_card) < 6:
        first_part = number_card[:4].ljust(4, "*")
        second_part = "**" if len(number_card) <= 4 else number_card[4:6]
        last_part = number_card[-4:].rjust(4, "*") if len(number_card) < 4 else number_card[-4:]
        return f"{first_part} {second_part}** **** {last_part}"

    # Стандартная обработка для номеров от 6 символов и больше
    return f"{number_card[:4]} {number_card[4:6]}** **** {number_card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета (показывает последние 4 цифры)"""
    return f"**{account_number[-4:]}"


# ввод номеров карты и счета
card = "1234567890123456"
account = "40702810500000012345"
