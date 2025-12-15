import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Args:
        transaction: Словарь с данными транзакции.
            Ожидаемые ключи: 'amount' (float), 'currency' (str).

    Returns:
        Сумма в рублях как float.

    Raises:
        ValueError: Если валюта не поддерживается или API ключ отсутствует.
        ConnectionError: Если не удалось получить данные от API.
        KeyError: Если в транзакции отсутствуют необходимые ключи.
    """
    try:
        amount_raw: Any = transaction["amount"]
        currency_raw: Any = transaction["currency"]
    except KeyError as e:
        raise KeyError(f"В транзакции отсутствует обязательный ключ: {e}")

    # Преобразование к правильным типам
    try:
        amount: float = float(amount_raw)
    except (ValueError, TypeError):
        raise ValueError(f"Некорректное значение суммы: {amount_raw}")

    currency: str = str(currency_raw).upper()

    # Если валюта уже рубли
    if currency == "RUB":
        return amount

    # Для USD и EUR делаем запрос к API
    if currency in ("USD", "EUR"):
        if not API_KEY:
            raise ValueError("API ключ для конвертации валют не найден. Проверьте файл .env")

        # Заголовки с API ключом
        headers: Dict[str, str] = {"apikey": API_KEY}
        params: Dict[str, str] = {"base": currency, "symbols": "RUB"}

        try:
            # Делаем запрос к API
            response: requests.Response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()  # Проверка HTTP ошибок

            data: Dict[str, Any] = response.json()
            # Предполагаемая структура ответа: {"rates": {"RUB": 92.5}}
            rates: Dict[str, float] = data.get("rates", {})
            rate: Optional[float] = rates.get("RUB")

            if rate is None:
                raise ValueError(f"Не удалось получить курс для {currency}")

            return amount * rate
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к API: {e}")
        except ValueError as e:
            # Ошибка парсинга JSON
            raise ValueError(f"Некорректный ответ от API: {e}")

    # Для других валют (не USD/EUR) пока просто возвращаем сумму
    # В будущем можно добавить поддержку других валют
    return amount
