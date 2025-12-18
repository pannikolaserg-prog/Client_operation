import unittest
from unittest.mock import patch, Mock
import json
import os
import sys

# Добавляем путь к src для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.external_api import get_amount_in_rub


class TestGetAmountInRub(unittest.TestCase):
    """Тесты для функции get_amount_in_rub"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.transaction_rub = {
            "id": 1,
            "operationAmount": {"amount": "1000.50", "currency": {"code": "RUB", "name": "руб."}},
            "description": "Тестовая транзакция в рублях",
        }

        self.transaction_usd = {
            "id": 2,
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}},
            "description": "Тестовая транзакция в долларах",
        }

        self.transaction_eur = {
            "id": 3,
            "operationAmount": {"amount": "50.00", "currency": {"code": "EUR", "name": "EUR"}},
            "description": "Тестовая транзакция в евро",
        }

        self.invalid_transaction = {"id": 4, "description": "Транзакция без суммы"}

    def test_get_amount_in_rub_rub(self):
        """Тест конвертации RUB -> RUB (должна вернуть ту же сумму)"""
        result = get_amount_in_rub(self.transaction_rub)
        self.assertEqual(result, 1000.50)
        self.assertIsInstance(result, float)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_get_amount_in_rub_usd_success(self, mock_get):
        """Тест успешной конвертации USD -> RUB через API"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": 9050.0}  # 100 USD * 90.50
        mock_get.return_value = mock_response

        result = get_amount_in_rub(self.transaction_usd)

        self.assertEqual(result, 9050.0)
        self.assertIsInstance(result, float)

        # Проверяем, что запрос был сделан с правильными параметрами
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_api_key"},
            params={"from": "USD", "to": "RUB", "amount": 100.0},
        )

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_get_amount_in_rub_eur_success(self, mock_get):
        """Тест успешной конвертации EUR -> RUB через API"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": 4950.0}  # 50 EUR * 99.0
        mock_get.return_value = mock_response

        result = get_amount_in_rub(self.transaction_eur)

        self.assertEqual(result, 4950.0)
        self.assertIsInstance(result, float)

        # Проверяем параметры запроса
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers={"apikey": "test_api_key"},
            params={"from": "EUR", "to": "RUB", "amount": 50.0},
        )

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_get_amount_in_rub_api_error(self, mock_get):
        """Тест когда API возвращает ошибку"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_get.return_value = mock_response

        result = get_amount_in_rub(self.transaction_usd)

        # При ошибке API должна вернуться исходная сумма
        self.assertEqual(result, 100.0)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_get_amount_in_rub_network_error(self, mock_get):
        """Тест сетевой ошибки при запросе к API"""
        mock_get.side_effect = Exception("Network error")

        result = get_amount_in_rub(self.transaction_usd)

        # При сетевой ошибке должна вернуться исходная сумма
        self.assertEqual(result, 100.0)

    @patch("src.external_api.API_KEY", None)
    def test_get_amount_in_rub_no_api_key(self):
        """Тест когда нет API ключа"""
        result = get_amount_in_rub(self.transaction_usd)

        # Без API ключа должна вернуться исходная сумма
        self.assertEqual(result, 100.0)

    def test_get_amount_in_rub_invalid_transaction(self):
        """Тест обработки некорректной транзакции"""
        result = get_amount_in_rub(self.invalid_transaction)

        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_get_amount_in_rub_invalid_amount_format(self):
        """Тест обработки некорректного формата суммы"""
        transaction = {"operationAmount": {"amount": "not_a_number", "currency": {"code": "USD"}}}

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 0.0)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_get_amount_in_rub_missing_result_field(self, mock_get):
        """Тест когда API не возвращает поле result"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True
            # Нет поля result
        }
        mock_get.return_value = mock_response

        result = get_amount_in_rub(self.transaction_usd)

        # Должна вернуться исходная сумма
        self.assertEqual(result, 100.0)

    def test_get_amount_in_rub_other_currency(self):
        """Тест для других валют (не USD/EUR)"""
        transaction_gbp = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}

        result = get_amount_in_rub(transaction_gbp)

        # Для других валют должна вернуться исходная сумма
        self.assertEqual(result, 100.0)


class TestMockRequestsLibrary(unittest.TestCase):
    """Тесты для мокирования библиотеки requests"""

    @patch("src.external_api.requests")
    @patch("src.external_api.API_KEY", "test_api_key")
    def test_requests_library_mocked(self, mock_requests):
        """Тест мокирования всей библиотеки requests"""
        # Настраиваем мок
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "result": 9000.0}
        mock_requests.get.return_value = mock_response

        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

        result = get_amount_in_rub(transaction)

        self.assertEqual(result, 9000.0)
        mock_requests.get.assert_called_once()

    @patch("src.external_api.requests.get")
    @patch.dict(os.environ, {"API_KEY": "test_key_from_env"})
    def test_api_key_from_environment(self, mock_get):
        """Тест получения API ключа из переменных окружения"""
        # Перезагружаем модуль, чтобы обновить API_KEY
        import importlib
        import src.external_api

        importlib.reload(src.external_api)

        # Проверяем, что API_KEY установлен
        self.assertEqual(src.external_api.API_KEY, "test_key_from_env")

        # Сбрасываем переменные окружения
        del os.environ["API_KEY"]


if __name__ == "__main__":
    unittest.main()
