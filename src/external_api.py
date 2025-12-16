import os
from decimal import Decimal
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Конфигурация API
API_KEY: Optional[str] = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL: str = "https://api.apilayer.com/exchangerates_data/convert"


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Args:
        transaction: Словарь с данными транзакции.
            Ожидаемые ключи: 'amount' (число), 'currency' (str).

    Returns:
        Сумма в рублях как float.

    Raises:
        ValueError: Если валюта не поддерживается или API ключ отсутствует.
        ConnectionError: Если не удалось получить данные от API.
        KeyError: Если в транзакции отсутствуют необходимые ключи.
    """
    # Получаем данные из транзакции с проверкой ключей
    try:
        # Ищем сумму в разных возможных ключах
        amount_raw = transaction.get('amount') or transaction.get('sum') or transaction.get('value')
        if amount_raw is None:
            raise KeyError("Не найден ключ с суммой транзакции (проверьте 'amount', 'sum', 'value')")

        # Ищем валюту в разных возможных ключах
        currency_raw = transaction.get('currency') or transaction.get('currency_code') or transaction.get(
            'currencyName')
        if currency_raw is None:
            raise KeyError(
                "Не найден ключ с валютой транзакции (проверьте 'currency', 'currency_code', 'currencyName')")
    except KeyError as e:
        raise KeyError(f"В транзакции отсутствуют необходимые данные: {e}")

    # Преобразование к правильным типам
    try:
        # Преобразуем сумму к float, независимо от исходного типа
        if isinstance(amount_raw, (int, float, Decimal)):
            amount: float = float(amount_raw)
        else:
            # Пробуем преобразовать строку к числу
            amount = float(str(amount_raw).replace(',', '.'))
    except (ValueError, TypeError):
        raise ValueError(f"Некорректное значение суммы: {amount_raw}")

    # Приводим валюту к верхнему регистру и обрезаем пробелы
    currency: str = str(currency_raw).strip().upper()

    # Если валюта уже рубли
    if currency == 'RUB':
        return amount

    # Для USD и EUR делаем запрос к API
    if currency in ('USD', 'EUR'):
        if not API_KEY:
            raise ValueError("API ключ для конвертации валют не найден. Проверьте файл .env")

        # Параметры запроса для конвертации
        params: Dict[str, str] = {
            "from": currency,
            "to": "RUB",
            "amount": str(amount)
        }

        headers: Dict[str, str] = {"apikey": API_KEY}

        try:
            # Делаем запрос к API конвертации
            response: requests.Response = requests.get(
                BASE_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()  # Проверка HTTP ошибок

            data: Dict[str, Any] = response.json()

            # Проверяем структуру ответа API
            if not data.get("success", False):
                error_info = data.get("error", {}).get("info", "Неизвестная ошибка API")
                raise ValueError(f"API вернул ошибку: {error_info}")

            # Получаем конвертированную сумму
            result: Optional[float] = data.get("result")
            if result is None:
                raise ValueError("API не вернул результат конвертации")

            return float(result)

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к API: {e}")
        except ValueError as e:
            # Ошибка парсинга JSON или неверная структура ответа
            raise ValueError(f"Некорректный ответ от API: {e}")

    # Для других валют (не USD/EUR) возвращаем сумму как есть
    return amount