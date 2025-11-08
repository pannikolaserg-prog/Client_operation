def mask_account_card(text):
    """
    Маскирует номер карты или счета в строке
    """
    if "Счет" in text:
        # Обработка счета
        parts = text.split()
        if len(parts) >= 2 and len(parts[-1]) >= 4:
            account_number = parts[-1]
            masked_account = "**" + account_number[-4:]
            return " ".join(parts[:-1] + [masked_account])

    # Обработка банковской карты
    parts = text.split()
    card_number = None

    # Ищем номер карты (последняя последовательность цифр)
    for part in reversed(parts):
        if part.isdigit() and len(part) >= 13:  # минимальная длина номера карты
            card_number = part
            break

    if card_number:
        # Убираем исходный номер
        masked_parts = [p for p in parts if p != card_number]

        # Форматируем замаскированный номер
        if len(card_number) == 16:
            masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        else:
            # Для других длин - общая маска
            masked_number = f"{card_number[:4]} ** **** {card_number[-4:]}"

        return " ".join(masked_parts + [masked_number])

    return text  # если не нашли что маскировать


# Тестирование
print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361

print(mask_account_card("Счет 73654108430135874305"))
# Счет **4305

print(mask_account_card("MasterCard Gold 5500000000000004"))
# MasterCard Gold 5500 00** **** 0004
