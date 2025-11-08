def mask_account_card(text: str) -> str:
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



