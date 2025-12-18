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
            return float(amount)

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
                            result: Any = data["result"]
                            return float(result) if result is not None else float(amount)
                except:
                    pass
            return float(amount)
        return float(amount)
    except:
        return 0.0