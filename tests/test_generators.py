from typing import Any, Dict, List

import pytest

from src.generators import filter_by_currency  # Импортируйте вашу функцию
from src.generators import card_number_generator, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"code": "USD", "name": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {"amount": "79114.93", "currency": {"code": "USD", "name": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {"amount": "43318.34", "currency": {"code": "RUB", "name": "руб."}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "operationAmount": {"amount": "100.00", "currency": {"code": "EUR", "name": "Euro"}},
            "description": "Покупка",
        },
        {"id": 123, "state": "CANCELED", "description": "Невалидная транзакция"},  # Транзакция без operationAmount
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd_transactions(self, sample_transactions: list[dict[str, Any]]) -> None:
        """Тест фильтрации USD транзакций."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        assert len(usd_transactions) == 2
        assert all(trans["operationAmount"]["currency"]["code"] == "USD" for trans in usd_transactions)
        assert usd_transactions[0]["id"] == 939719570
        assert usd_transactions[1]["id"] == 142264268

    def test_filter_rub_transactions(self, sample_transactions: list[dict[str, Any]]) -> None:
        """Тест фильтрации RUB транзакций."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        assert len(rub_transactions) == 1
        assert rub_transactions[0]["id"] == 873106923
        assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_eur_transactions(self, sample_transactions: list[dict[str, Any]]) -> None:
        """Тест фильтрации EUR транзакций."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

        assert len(eur_transactions) == 1
        assert eur_transactions[0]["id"] == 895315941


@pytest.fixture
def transaction_samples() -> list[dict[str, Any]]:
    """Фикстура с тестовыми транзакциями для описаний."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Оплата услуг"},
        {"id": 5},  # Транзакция без описания
        {"description": "Еще одна операция"},  # Транзакция без id
    ]


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_get_all_descriptions(self, transaction_samples: list[dict[str, Any]]) -> None:
        """Тест получения всех описаний."""
        descriptions = list(transaction_descriptions(transaction_samples))

        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Оплата услуг",
            "",  # Для транзакции без описания
            "Еще одна операция",
        ]

        assert descriptions == expected

    def test_generator_behavior(self, transaction_samples: list[dict[str, Any]]) -> None:
        """Тест поведения генератора."""
        gen = transaction_descriptions(transaction_samples)

        # Проверяем поочередное получение значений
        assert next(gen) == "Перевод организации"
        assert next(gen) == "Перевод со счета на счет"
        assert next(gen) == "Перевод с карты на карту"
        assert next(gen) == "Оплата услуг"
        assert next(gen) == ""  # Пустое описание
        assert next(gen) == "Еще одна операция"

        # Генератор должен завершиться
        with pytest.raises(StopIteration):
            next(gen)

    def test_empty_transactions_list(self) -> None:
        """Тест обработки пустого списка транзакций."""
        descriptions = list(transaction_descriptions([]))
        assert descriptions == []

    @pytest.mark.parametrize(
        "input_data,expected",
        [
            ([{"description": "Оп1"}], ["Оп1"]),
            ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
            ([{"desc": "Нет ключа"}], [""]),
            ([], []),
        ],
    )
    def test_parameterized_descriptions(self, input_data: List[Dict[str, Any]], expected: List[str]) -> None:
        """Параметризованный тест для различных входных данных."""
        result = list(transaction_descriptions(input_data))
        assert result == expected

    @pytest.mark.parametrize(
        "start,end,expected_count",
        [
            (1, 10, 10),
            (100, 100, 1),
            (9990, 10000, 11),
            (1, 1, 1),
        ],
    )
    def test_range_sizes(self, start: int, end: int, expected_count: int) -> None:
        """Параметризованный тест размеров диапазонов."""
        result = list(card_number_generator(start, end))
        assert len(result) == expected_count

    @pytest.mark.parametrize(
        "number,expected_format",
        [
            (1, "0000 0000 0000 0001"),
            (12, "0000 0000 0000 0012"),
            (123, "0000 0000 0000 0123"),
            (1234, "0000 0000 0000 1234"),
            (12345, "0000 0000 0001 2345"),
            (9999999999999999, "9999 9999 9999 9999"),
        ],
    )
    def test_parameterized_formatting(self, number: int, expected_format: int) -> None:
        """Параметризованный тест форматирования."""
        result = list(card_number_generator(number, number))
        assert result[0] == expected_format

    def test_progressive_generation(self) -> None:
        """Тест последовательной генерации."""
        gen = card_number_generator(9995, 10005)
        results = []

        for _ in range(11):  # 9995-10005 включительно = 11 чисел
            results.append(next(gen))

        # Проверяем несколько ключевых значений
        assert results[0] == "0000 0000 0000 9995"
        assert results[5] == "0000 0000 0001 0000"  # 10000
        assert results[10] == "0000 0000 0001 0005"  # 10005
