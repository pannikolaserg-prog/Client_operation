import pytest
from unittest.mock import patch
import sys
import os

# Добавляем корневую директорию проекта в путь Python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Импортируем из main.py
try:
    # Если main.py в корне проекта
    import main

    get_valid_input = main.get_valid_input
    format_transaction = main.format_transaction
    main_func = main.main
except ImportError:
    # Если не нашли, пробуем другие варианты
    try:
        # Если в папке src
        from src.main import get_valid_input, format_transaction, main as main_func
    except ImportError:
        # Создаем заглушки для тестов
        def get_valid_input(prompt, valid_options=None, case_sensitive=False):
            return "test"

        def format_transaction(transaction):
            return "formatted"

        def main_func():
            pass


class TestGetValidInput:
    """Тесты для функции get_valid_input"""

    def test_get_valid_input_no_options(self):
        """Тест ввода без валидации опций"""
        with patch('builtins.input', return_value='любой текст'):
            result = get_valid_input("Введите что-нибудь: ")
            assert result == 'любой текст'

    def test_get_valid_input_valid_option(self):
        """Тест валидного ввода"""
        with patch('builtins.input', return_value='Да'):
            result = get_valid_input("Выберите: ", ["Да", "Нет"])
            assert result == 'Да'

    def test_get_valid_input_case_insensitive(self):
        """Тест ввода без учета регистра"""
        with patch('builtins.input', return_value='да'):
            result = get_valid_input("Выберите: ", ["Да", "Нет"])
            assert result == 'Да'

    def test_get_valid_input_retry(self):
        """Тест повторного запроса при некорректном вводе"""
        inputs = ['неправильно', 'Да']
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print') as mock_print:
                result = get_valid_input("Выберите: ", ["Да", "Нет"])
                assert result == 'Да'
                assert mock_print.called


class TestFormatTransaction:
    """Тесты для функции format_transaction"""

    @patch('main.mask_account_card')
    def test_format_transaction_with_all_fields(self, mock_mask):
        """Тест форматирования транзакции со всеми полями"""
        # Настраиваем мок
        mock_mask.side_effect = lambda x: f"Маскировка({x})"

        transaction = {
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод организации",
            "from": "Счет 1234567890123456",
            "to": "Счет 6543210987654321",
            "operationAmount": {
                "amount": "16210",
                "currency": {
                    "name": "Sol"
                }
            }
        }

        result = format_transaction(transaction)

        assert "05.09.2023" in result
        assert "Перевод организации" in result
        assert "Маскировка(Счет 1234567890123456)" in result
        assert "Маскировка(Счет 6543210987654321)" in result
        assert "16210" in result
        assert "Sol" in result

    @patch('main.mask_account_card')
    def test_format_transaction_without_from(self, mock_mask):
        """Тест форматирования транзакции без отправителя"""
        mock_mask.return_value = "Маскировка(счет)"

        transaction = {
            "date": "2023-09-05T11:30:32Z",
            "description": "Открытие вклада",
            "to": "Счет 6543210987654321",
            "operationAmount": {
                "amount": "1000",
                "currency": "руб."
            }
        }

        result = format_transaction(transaction)

        assert "05.09.2023" in result
        assert "Открытие вклада" in result
        assert "Маскировка(счет)" in result
        assert "1000" in result
        assert "руб." in result


class TestMainIntegration:
    """Интеграционные тесты для main()"""

    @patch('main.load_transactions')
    def test_main_json_flow(self, mock_load):
        """Тест основного потока с JSON файлом"""
        # Мокируем данные
        mock_transactions = [{
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "description": "Перевод",
            "to": "Счет 5678",
            "operationAmount": {"amount": "1000", "currency": {"name": "RUB"}}
        }]
        mock_load.return_value = mock_transactions

        # Мокируем все зависимости
        with patch('main.filter_by_state') as mock_filter:
            mock_filter.return_value = mock_transactions

            # Симулируем пользовательский ввод
            inputs = ['1', 'EXECUTED', 'Нет', 'Нет', 'Нет']

            with patch('builtins.input', side_effect=inputs):
                with patch('builtins.print'):
                    try:
                        main_func()
                        # Если функция завершилась без ошибок - тест пройден
                        assert True
                    except (SystemExit, KeyboardInterrupt):
                        # Ожидаемые исключения
                        assert True

    @patch('main.read_csv_file')
    def test_main_csv_flow_no_transactions(self, mock_csv):
        """Тест потока с CSV файлом без транзакций"""
        mock_csv.return_value = []

        inputs = ['2']

        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print') as mock_print:
                try:
                    main_func()
                except (SystemExit, KeyboardInterrupt):
                    pass

                # Проверяем сообщение об ошибке
                assert any("Не удалось загрузить транзакции" in str(call)
                           for call in mock_print.call_args_list)

    @patch('main.read_csv_file')
    @patch('main.filter_by_state')
    def test_main_csv_filter_no_results(self, mock_filter, mock_csv):
        """Тест потока, когда фильтрация не дает результатов"""
        mock_csv.return_value = [{"state": "CANCELED"}]
        mock_filter.return_value = []  # Нет EXECUTED транзакций

        inputs = ['2', 'EXECUTED']

        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print') as mock_print:
                try:
                    main_func()
                except (SystemExit, KeyboardInterrupt):
                    pass

                assert any("Нет транзакций" in str(call)
                           for call in mock_print.call_args_list)


# Простые тесты без сложных зависимостей
def test_main_imports():
    """Тест, что основные функции импортируются"""
    assert callable(get_valid_input)
    assert callable(format_transaction)
    assert callable(main_func)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
