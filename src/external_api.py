import json
import os
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY: Optional[str] = os.getenv("API_KEY")


def get_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма транзакции в рублях (float)
    """
    try:
        op: Dict[str, Any] = transaction["operationAmount"]
        amount: float = float(op["amount"])
        currency: str = op["currency"]["code"]

        if currency == "RUB":
            return amount

        if currency in ("USD", "EUR"):
            if API_KEY:
                try:
                    r: requests.Response = requests.get(
                        "https://api.apilayer.com/exchangerates_data/convert",
                        headers={"apikey": API_KEY},
                        params={"from": currency, "to": "RUB", "amount": amount},
                    )
                    if r.status_code == 200:
                        data: Dict[str, Any] = r.json()
                        if data.get("success"):
                            return data["result"]
                except:
                    pass
            return amount
        return amount
    except:
        return 0.0

try:
    with open("data/operations.json", "r", encoding="utf-8") as f:
        data: Any = json.load(f)

    print(f"Загружено {len(data)} транзакций")
    print("Конвертация сумм в рубли:")
    print("-" * 50)

    for i, item in enumerate(data[:10], 1):  # Первые 10 транзакций
        rub_amount: float = get_amount_in_rub(item)
        description: str = item.get("description", "Без описания")

        # Получаем исходные данные для отображения
        op_amount: Dict[str, Any] = item.get("operationAmount", {})
        original_amount: str = op_amount.get("amount", "0")
        currency: str = op_amount.get("currency", {}).get("code", "")

        print(f"{i}. {description}")
        print(f"   Исходная сумма: {original_amount} {currency}")
        print(f"   В рублях: {rub_amount:.2f} RUB")
        print()

except FileNotFoundError:
    print("Ошибка: Файл 'data/operations.json' не найден")
    print("Создайте папку 'data' и поместите туда файл operations.json")
except json.JSONDecodeError:
    print("Ошибка: Файл содержит некорректный JSON")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")