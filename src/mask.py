def get_mask_card_number(number_card: str) -> str:
    """Функция принимает номер карты и возврщает его в замаскированном виде"""
    return f"{number_card[:4]} {number_card[4:6]}** **** {number_card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета (показывает последние 4 цифры)"""
    return f"**{account_number[-4:]}"


# ввод номеров карты и счета
card = "1234567890123456"
account = "40702810500000012345"


print(f"Карта: {get_mask_card_number(card)}")
print(f"Счет: {get_mask_account(account)}")
