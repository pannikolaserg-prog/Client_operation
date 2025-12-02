from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:

    @pytest.mark.parametrize(
        "input_data, state, expected_count",
        [
            # Проверка количества возвращаемых элементов
            (
                [
                    {"id": 1, "state": "EXECUTED"},
                    {"id": 2, "state": "PENDING"},
                    {"id": 3, "state": "EXECUTED"},
                    {"id": 4, "state": "CANCELED"},
                ],
                "EXECUTED",
                2,
            ),
            ([{"id": 1, "state": "PENDING"}, {"id": 2, "state": "PENDING"}], "PENDING", 2),
            ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}], "PENDING", 0),
        ],
    )
    def test_filter_by_state_count(self, input_data: list[dict[str, Any]], state: str, expected_count: int) -> None:
        """Тестирование количества возвращаемых элементов"""
        result = filter_by_state(input_data, state)
        assert len(result) == expected_count

    def test_filter_by_state_immutability(self) -> None:
        """Тест на неизменяемость исходных данных"""
        original_data = [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}]
        original_data_copy = original_data.copy()

        result = filter_by_state(original_data, "EXECUTED")

        # Проверяем, что исходные данные не изменились
        assert original_data == original_data_copy
        # Проверяем, что результат - новый список
        assert result is not original_data

    @pytest.mark.parametrize(
        "input_data, state",
        [
            # Словари без ключа 'state'
            ([{"id": 1, "description": "test"}, {"id": 2, "state": "EXECUTED"}], "EXECUTED"),
            # Словари с None значениями
            ([{"id": 1, "state": None}, {"id": 2, "state": "EXECUTED"}], "EXECUTED"),
            # Словари с разными типами данных в state
            ([{"id": 1, "state": 123}, {"id": 2, "state": "EXECUTED"}], "EXECUTED"),
        ],
    )
    def test_filter_by_state_edge_cases(self, input_data: list[dict[str, Any]], state: str) -> None:
        """Тестирование граничных случаев"""
        result = filter_by_state(input_data, state)
        # Проверяем, что возвращается только элемент с state="EXECUTED"
        assert len(result) == 1
        assert result[0]["id"] == 2
        assert result[0]["state"] == "EXECUTED"


class TestSortByDate:

    @pytest.fixture
    def sample_data(self) -> list[dict[str, Any]]:
        """Фикстура с тестовыми данными"""
        return [
            {"id": 1, "date": "2023-10-01T12:00:00", "amount": 100},
            {"id": 2, "date": "2023-09-15T08:30:00", "amount": 200},
            {"id": 3, "date": "2023-11-20T15:45:00", "amount": 300},
            {"id": 4, "date": "2023-08-05T10:00:00", "amount": 400},
        ]

    @pytest.mark.parametrize(
        "reverse, expected_order",
        [
            # Сортировка по убыванию (новые сначала)
            (True, [3, 1, 2, 4]),  # 2023-11-20, 2023-10-01, 2023-09-15, 2023-08-05
            # Сортировка по возрастанию (старые сначала)
            (False, [4, 2, 1, 3]),  # 2023-08-05, 2023-09-15, 2023-10-01, 2023-11-20
        ],
    )
    def test_sort_by_date_basic(
        self, sample_data: list[dict[str, Any]], reverse: bool, expected_order: list[int]
    ) -> None:
        """Тестирование базовой сортировки по дате"""
        result = sort_by_date(sample_data, reverse=reverse)

        # Проверяем порядок элементов по id
        result_ids = [item["id"] for item in result]
        assert result_ids == expected_order

    @pytest.mark.parametrize(
        "input_data, reverse, expected",
        [
            # Пустой список
            ([], True, []),
            ([], False, []),
            # Один элемент
            ([{"id": 1, "date": "2023-10-01T12:00:00"}], True, [1]),
            ([{"id": 1, "date": "2023-10-01T12:00:00"}], False, [1]),
            # Два элемента
            ([{"id": 1, "date": "2023-10-01T12:00:00"}, {"id": 2, "date": "2023-09-01T12:00:00"}], True, [1, 2]),
            ([{"id": 1, "date": "2023-10-01T12:00:00"}, {"id": 2, "date": "2023-09-01T12:00:00"}], False, [2, 1]),
        ],
    )
    def test_sort_by_date_edge_cases(
        self, input_data: list[dict[str, Any]], reverse: bool, expected: list[int]
    ) -> None:
        """Тестирование граничных случаев"""
        result = sort_by_date(input_data, reverse=reverse)
        result_ids = [item["id"] for item in result]
        assert result_ids == expected

    def test_sort_by_date_default_parameter(self, sample_data: list[dict[str, Any]]) -> None:
        """Тестирование значения по умолчанию для reverse (True)"""
        result_default = sort_by_date(sample_data)
        result_explicit = sort_by_date(sample_data, reverse=True)

        # Должны быть идентичны
        assert result_default == result_explicit

    @pytest.mark.parametrize(
        "invalid_data",
        [
            # Словари с некорректными датами
            [{"id": 1, "date": "invalid-date"}],
            [{"id": 1, "date": "2023/10/01"}],  # Нестандартный формат
            [{"id": 1, "date": 12345}],  # Число вместо строки
            [{"id": 1, "date": None}],  # None вместо строки
        ],
    )
    def test_sort_by_date_invalid_dates(self, invalid_data: list[dict[str, Any]]) -> None:
        """Тестирование сортировки с некорректными датами"""
        # Функция должна отработать без ошибок, но сортировка может быть непредсказуемой
        result = sort_by_date(invalid_data, reverse=True)
        assert len(result) == len(invalid_data)
        # Проверяем, что все элементы присутствуют
        assert all(item in result for item in invalid_data)
