from typing import Dict, Iterator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, 'USD')

    Returns:
        Итератор, который поочередно выдает транзакции с заданной валютой
    """
    for transaction in transactions:
        # Проверяем структуру транзакции и наличие валюты
        if isinstance(transaction, dict):
            # Получаем информацию о валюте из вложенной структуры
            operation_amount = transaction.get("operationAmount")
            if isinstance(operation_amount, dict):
                currency_info = operation_amount.get("currency")
                if isinstance(currency_info, dict):
                    # Проверяем, совпадает ли код валюты с искомым
                    if currency_info.get("code") == currency:
                        yield transaction


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
    },
]


# Создаем итератор
usd_transactions = filter_by_currency(transactions, "USD")

# Получаем две транзакции с помощью next()
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции по очереди.
    """
    for transaction in transactions:
        # Проверяем, что транзакция является словарем и содержит описание
        if isinstance(transaction, dict) and "description" in transaction:
            yield transaction["description"]
        else:
            # Если описания нет, возвращаем пустую строкю
            yield ""


# Тестовые данные
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]

# Использование функции
descriptions = transaction_descriptions(transactions)

# Получаем пять описаний
for _ in range(5):
    print(next(descriptions))


def card_number_generator(start: int, stop: int) -> Iterator [str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальный номер карты (от 1)
        end: Конечный номер карты (до 9999999999999999)

    Yields:
        Номера карт в заданном диапазоне в формате XXXX XXXX XXXX XXXX
    """
    for num in range(start, stop + 1):
        # Форматируем число как 16-значную строку с ведущими нулями
        formatted_num = f"{num:016d}"
        # Разбиваем на группы по 4 цифры
        card_number = f"{formatted_num[0:4]} {formatted_num[4:8]} {formatted_num[8:12]} {formatted_num[12:16]}"
        yield card_number


for card_number in card_number_generator(1, 5):
    print(card_number)
