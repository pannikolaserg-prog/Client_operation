from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import get_amount_in_rub


def test_get_amount_in_rub_rub() -> None:
    """Тест для транзакции в рублях (конвертация не требуется)."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "RUB"}
    result: float = get_amount_in_rub(transaction)
    assert result == 100.0
    assert isinstance(result, float)


def test_get_amount_in_rub_usd_with_mock() -> None:
    """Тест конвертации USD в RUB с моком API запроса."""
    # Подготовка тестовых данных
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "USD"}
    mock_rate: float = 92.5

    # Мокаем requests.get
    with patch("src.external_api.requests.get") as mock_get:
        # Настраиваем мок
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"rates": {"RUB": mock_rate}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызов тестируемой функции
        result: float = get_amount_in_rub(transaction)

        # Проверка результата
        expected: float = 100.0 * mock_rate
        assert result == expected

        # Проверка вызова API с правильными параметрами
        mock_get.assert_called_once()
        call_args: Any = mock_get.call_args
        assert call_args[1]["headers"]["apikey"] is not None
        assert call_args[1]["params"]["base"] == "USD"
        assert call_args[1]["params"]["symbols"] == "RUB"


def test_get_amount_in_rub_missing_api_key() -> None:
    """Тест обработки отсутствующего API ключа."""
    # Временно удаляем API ключ из окружения
    with patch("src.external_api.API_KEY", None):
        transaction: Dict[str, Any] = {"amount": 100.0, "currency": "USD"}

        with pytest.raises(ValueError, match="API ключ для конвертации валют не найден"):
            get_amount_in_rub(transaction)


def test_get_amount_in_rub_missing_required_keys() -> None:
    """Тест обработки транзакции без обязательных ключей."""
    transaction: Dict[str, Any] = {"id": 1}  # Нет amount и currency

    with pytest.raises(KeyError):
        get_amount_in_rub(transaction)


def test_get_amount_in_rub_invalid_amount_type() -> None:
    """Тест обработки некорректного типа суммы."""
    transaction: Dict[str, Any] = {"amount": "not_a_number", "currency": "RUB"}

    with pytest.raises(ValueError, match="Некорректное значение суммы"):
        get_amount_in_rub(transaction)


def test_get_amount_in_rub_other_currency() -> None:
    """Тест для валюты, отличной от USD/EUR/RUB (возврат без конвертации)."""
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "GBP"}
    result: float = get_amount_in_rub(transaction)
    assert result == 100.0
