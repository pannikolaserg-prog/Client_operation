def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует транзакции по статусу.

    Args:
        transactions: Список словарей с транзакциями
        state: Статус для фильтрации ("EXECUTED", "CANCELED", "PENDING")

    Returns:
        Список отфильтрованных транзакций
    """
    if not transactions:
        return []

    # Проверяем наличие поля 'state' (нижний регистр)
    if "state" in transactions[0]:
        key = "state"
    # Проверяем наличие поля 'STATE' (верхний регистр)
    elif "STATE" in transactions[0]:
        key = "STATE"
    else:
        # Если нет явного поля state, ищем в других полях
        return [t for t in transactions if str(t).upper().find(state.upper()) != -1]

    # Фильтруем с учетом регистра
    return [t for t in transactions if str(t.get(key, "")).upper() == state.upper()]


def sort_by_date(data: list, reverse: bool = True) -> list:
    """
    Сортирует список словарей по дате
    """

    if not data:
        return []

    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)


test_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

# Сортировка по убыванию (по умолчанию)
result1 = sort_by_date(test_data)
print(result1)  # Сначала 2019-07-03, затем 2018-09-12, потом 2018-06-30

# Сортировка по возрастанию
result2 = sort_by_date(test_data, reverse=False)
print(result2)  # Сначала 2018-06-30, затем 2018-09-12, потом 2019-07-03


test_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

# Фильтрация по умолчанию (EXECUTED)
result1 = filter_by_state(test_data)
print(result1)  # Выведет два EXECUTED словаря

# Фильтрация по CANCELED
result2 = filter_by_state(test_data, "CANCELED")
print(result2)  # Выведет один CANCELED словарь

test_data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

# Сортировка по убыванию (по умолчанию)
result1 = sort_by_date(test_data)
print(result1)  # Сначала 2019-07-03, затем 2018-09-12, потом 2018-06-30

# Сортировка по возрастанию
result2 = sort_by_date(test_data, reverse=False)
print(result2)  # Сначала 2018-06-30, затем 2018-09-12, потом 2019-07-03
