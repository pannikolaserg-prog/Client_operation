import os
import sys
import unittest
from decimal import Decimal
from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock, patch

import requests  # Добавьте этот импорт

# Добавляем путь к модулю
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.external_api import get_amount_in_rub


class TestGetAmountInRub(unittest.TestCase):
    """Тесты для функции get_amount_in_rub"""

    def setUp(self) -> None:
        """Настройка перед каждым тестом"""
        self.mock_api_key: str = "test_api_key_123"
        self.original_env: Dict[str, str] = dict(os.environ)

    def tearDown(self) -> None:
        """Очистка после каждого теста"""
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch("src.external_api.requests.get")
    def test_successful_usd_conversion(self, mock_requests_get: MagicMock) -> None:
        """Тест успешной конвертации USD в RUB"""
        # Настройка моков
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 7500.50}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        # Установка API ключа
        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля для применения нового API ключа
        import importlib

        import src.external_api  # Импортируем модуль

        importlib.reload(src.external_api)  # Перезагружаем модуль

        # Импортируем функцию после перезагрузки
        from src.external_api import get_amount_in_rub

        # Создание тестовой транзакции
        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        # Вызов функции
        result: float = get_amount_in_rub(transaction)

        # Проверки
        self.assertEqual(result, 7500.50)
        mock_requests_get.assert_called_once()

        # Проверка параметров вызова
        call_args: Any = mock_requests_get.call_args
        self.assertEqual(call_args[1]["headers"]["apikey"], self.mock_api_key)
        self.assertEqual(call_args[1]["params"]["from"], "USD")
        self.assertEqual(call_args[1]["params"]["to"], "RUB")
        self.assertEqual(call_args[1]["params"]["amount"], "100.0")

    @patch("src.external_api.requests.get")
    def test_successful_eur_conversion(self, mock_requests_get: MagicMock) -> None:
        """Тест успешной конвертации EUR в RUB"""
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 8500.75}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "EUR"}

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 8500.75)

    def test_rub_transaction_no_conversion(self) -> None:
        """Тест транзакции в рублях (без конвертации)"""
        transaction: Dict[str, Any] = {"amount": 1000.50, "currency": "RUB"}

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 1000.50)

    @patch("src.external_api.requests.get")
    def test_api_returns_error(self, mock_requests_get: MagicMock) -> None:
        """Тест, когда API возвращает ошибку"""
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ValueError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("API вернул ошибку", str(context.exception))

    @patch("src.external_api.requests.get")
    def test_api_connection_error(self, mock_requests_get: MagicMock) -> None:
        """Тест ошибки соединения с API"""
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ConnectionError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Ошибка при запросе к API", str(context.exception))

    @patch("src.external_api.requests.get")
    def test_api_timeout_error(self, mock_requests_get: MagicMock) -> None:
        """Тест ошибки таймаута при запросе к API"""
        mock_requests_get.side_effect = requests.exceptions.Timeout("Request timeout")

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ConnectionError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Ошибка при запросе к API", str(context.exception))

    def test_missing_api_key(self) -> None:
        """Тест отсутствия API ключа"""
        # Удаляем API ключ из окружения
        if "EXCHANGE_RATE_API_KEY" in os.environ:
            del os.environ["EXCHANGE_RATE_API_KEY"]

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ValueError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("API ключ для конвертации валют не найден", str(context.exception))

    def test_missing_amount_key(self) -> None:
        """Тест отсутствия ключа суммы"""
        transaction: Dict[str, Any] = {"currency": "RUB"}

        with self.assertRaises(KeyError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Не найден ключ с суммой транзакции", str(context.exception))

    def test_missing_currency_key(self) -> None:
        """Тест отсутствия ключа валюты"""
        transaction: Dict[str, Any] = {"amount": 1000.50}

        with self.assertRaises(KeyError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Не найден ключ с валютой транзакции", str(context.exception))

    def test_invalid_amount_value(self) -> None:
        """Тест некорректного значения суммы"""
        transaction: Dict[str, Any] = {"amount": "not a number", "currency": "RUB"}

        with self.assertRaises(ValueError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Некорректное значение суммы", str(context.exception))

    def test_amount_with_comma_decimal(self) -> None:
        """Тест суммы с запятой в качестве разделителя"""
        transaction: Dict[str, Any] = {"amount": "1000,50", "currency": "RUB"}

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 1000.50)

    def test_decimal_amount(self) -> None:
        """Тест суммы типа Decimal"""
        transaction: Dict[str, Any] = {"amount": Decimal("1234.56"), "currency": "RUB"}

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 1234.56)

    def test_int_amount(self) -> None:
        """Тест целочисленной суммы"""
        transaction: Dict[str, Any] = {"amount": 1000, "currency": "RUB"}

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 1000.00)

    def test_currency_case_insensitive(self) -> None:
        """Тест нечувствительности к регистру валюты"""
        test_cases: List[Dict[str, Any]] = [
            {"amount": 100, "currency": "rub", "expected": 100.00},
            {"amount": 100, "currency": "Rub", "expected": 100.00},
            {"amount": 100, "currency": "RUB", "expected": 100.00},
            {"amount": 100, "currency": " usd ", "expected": None},  # Будет вызывать API
            {"amount": 100, "currency": "eur", "expected": None},  # Будет вызывать API
        ]

        for test_case in test_cases:
            transaction: Dict[str, Any] = {"amount": test_case["amount"], "currency": test_case["currency"]}

            if test_case["expected"] is not None:
                result: float = get_amount_in_rub(transaction)
                self.assertEqual(result, test_case["expected"])

    def test_other_currency_no_conversion(self) -> None:
        """Тест других валют (не USD/EUR/RUB)"""
        transaction: Dict[str, Any] = {"amount": 1000.50, "currency": "GBP"}  # Британский фунт

        result: float = get_amount_in_rub(transaction)
        self.assertEqual(result, 1000.50)

    @patch("src.external_api.requests.get")
    def test_api_response_missing_result(self, mock_requests_get: MagicMock) -> None:
        """Тест случая, когда API не возвращает результат"""
        mock_response: MagicMock = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            # "result" отсутствует
        }
        mock_response.raise_for_status.return_value = None
        mock_requests_get.return_value = mock_response

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ValueError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("API не вернул результат конвертации", str(context.exception))

    @patch("src.external_api.requests.get")
    def test_http_error(self, mock_requests_get: MagicMock) -> None:
        """Тест HTTP ошибки от API"""
        mock_response: MagicMock = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_requests_get.return_value = mock_response

        os.environ["EXCHANGE_RATE_API_KEY"] = self.mock_api_key

        # Перезагрузка модуля
        import importlib

        import src.external_api

        importlib.reload(src.external_api)
        from src.external_api import get_amount_in_rub

        transaction: Dict[str, Any] = {"amount": 100.00, "currency": "USD"}

        with self.assertRaises(ConnectionError) as context:
            get_amount_in_rub(transaction)

        self.assertIn("Ошибка при запросе к API", str(context.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
