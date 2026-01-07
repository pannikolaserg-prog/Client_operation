import sys

# Импортируем функции
from src.bank_operations import process_bank_search, process_bank_operations
from src.utils import load_transactions
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.read_csv_excel import read_csv_file, read_excel_file
from src.widget import mask_account_card


def get_valid_input(prompt: str, valid_options: list[str] = None, case_sensitive: bool = False) -> str:
    """Получает валидный ввод от пользователя."""
    while True:
        user_input = input(prompt).strip()

        if not valid_options:
            return user_input

        if case_sensitive:
            if user_input in valid_options:
                return user_input
        else:
            lower_options = [opt.lower() for opt in valid_options]
            if user_input.lower() in lower_options:
                # Возвращаем оригинальный вариант из valid_options
                idx = lower_options.index(user_input.lower())
                return valid_options[idx]

        print(f"Некорректный ввод. Пожалуйста, выберите из: {', '.join(valid_options)}")


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода."""
    result = []

    # Дата
    date_str = transaction.get("date", "")
    if date_str:
        if "T" in date_str:
            date_part = date_str.split("T")[0]
            parts = date_part.split("-")
            if len(parts) == 3:
                result.append(f"{parts[2]}.{parts[1]}.{parts[0]}")
            else:
                result.append(date_part)
        else:
            result.append(date_str)

    # Описание
    description = transaction.get("description", "")
    if description:
        result.append(description)

    # От кого и кому
    from_acc = transaction.get("from", "")
    to_acc = transaction.get("to", "")

    if from_acc and to_acc:
        result.append(f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}")
    elif to_acc:
        result.append(f"{mask_account_card(to_acc)}")

    # Сумма
    op_amount = transaction.get("operationAmount", {})
    if isinstance(op_amount, dict):
        amount = op_amount.get("amount", "")
        currency_info = op_amount.get("currency", {})
        if isinstance(currency_info, dict):
            currency = currency_info.get("name", "руб.")
        else:
            currency = str(currency_info)
    else:
        amount = ""
        currency = "руб."

    if amount:
        result.append(f"Сумма: {amount} {currency}")

    return "\n".join(result)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор типа файла
    choice = get_valid_input("\nВаш выбор (1-3): ", ["1", "2", "3"])

    file_types = {
        "1": ("JSON", "data/operations.json"),
        "2": ("CSV", "data/transactions.csv"),
        "3": ("XLSX", "data/transactions_excel.xlsx")
    }

    file_type, filepath = file_types[choice]
    print(f"\nДля обработки выбран {file_type}-файл.")

    # Загрузка данных с использованием соответствующих функций
    if choice == "1":
        transactions = load_transactions(filepath)
    elif choice == "2":
        # Используем read_csv_file
        # Если функция принимает путь к файлу, передаем его
        try:
            transactions = read_csv_file(filepath)
        except TypeError:
            # Если функция не принимает аргументов
            transactions = read_csv_file()
    else:  # choice == "3"
        # Используем read_excel_file
        try:
            transactions = read_excel_file(filepath)
        except TypeError:
            # Если функция не принимает аргументов
            transactions = read_excel_file()

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершена.")
        return

    print(f"Загружено {len(transactions)} транзакций.")

    print("\n=== ОТЛАДОЧНАЯ ИНФОРМАЦИЯ ===")
    if transactions and len(transactions) > 0:
        first_tx = transactions[0]
        print(f"Тип первого элемента: {type(first_tx)}")
        print("Все ключи первой транзакции:")
        for key, value in first_tx.items():
            print(f"  '{key}': {value}")

        # Проверяем валюту
        print("\nПоиск полей, связанных с валютой:")
        for key in first_tx.keys():
            if 'curr' in key.lower() or 'валют' in key.lower():
                print(f"  Найдено поле: '{key}' = {first_tx[key]}")

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Введите статус, по которому необходимо выполнить фильтрацию: ").strip()

        if status_input.upper() in valid_statuses:
            filtered_transactions = filter_by_state(transactions, status_input)
            print(f'Операции отфильтрованы по статусу "{status_input.upper()}"')
            break
        else:
            print(f'Статус операции "{status_input}" недоступен.')

    if not filtered_transactions:
        print("Нет транзакций с выбранным статусом.")
        return

    print(f"Найдено {len(filtered_transactions)} транзакций.")

    # Дополнительная фильтрация
    current_transactions = filtered_transactions.copy()

    # Сортировка по дате
    sort_choice = get_valid_input("\nОтсортировать операции по дате? (Да/Нет): ", ["Да", "Нет"])

    if sort_choice == "Да":
        order_choice = get_valid_input("Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ",
                                       ["по возрастанию", "по убыванию"])

        reverse_sort = (order_choice == "по убыванию")
        current_transactions = sort_by_date(current_transactions, reverse_sort)
        print(f"Операции отсортированы {order_choice}.")

    # Фильтрация по валюте
    rub_choice = get_valid_input("\nВыводить только рублевые транзакции? (Да/Нет): ", ["Да", "Нет"])

    if rub_choice == "Да":
        # Сначала проверяем структуру данных
        if current_transactions and isinstance(current_transactions[0], dict):
            # Проверяем, есть ли поле currency_code в первой транзакции
            first_transaction = current_transactions[0]

            # Если есть прямое поле currency_code
            if "currency_code" in first_transaction:
                # Фильтруем по полю currency_code
                filtered = [t for t in current_transactions if t.get("currency_code") == "RUB"]
                current_transactions = filtered
            # Если currency_code вложено в operationAmount
            elif "operationAmount" in first_transaction and isinstance(first_transaction["operationAmount"], dict):
                if "currency_code" in first_transaction["operationAmount"]:
                    filtered = [t for t in current_transactions
                                if t.get("operationAmount", {}).get("currency_code") == "RUB"]
                    current_transactions = filtered
            else:
                # Используем стандартную функцию
                current_transactions = list(filter_by_currency(current_transactions, 'RUB'))

        print("Отображаются только рублевые транзакции.")

    # Поиск по описанию
    search_choice = get_valid_input("\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ",
                                    ["Да", "Нет"])

    if search_choice == "Да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            current_transactions = process_bank_search(current_transactions, search_word)
            print(f"Применен фильтр по слову '{search_word}'.")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not current_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(current_transactions)}\n")

    for transaction in current_transactions:
        print(format_transaction(transaction))
        print()  # Пустая строка между транзакциями

    # Дополнительная статистика (используем process_bank_operations)
    print("=" * 50)
    print("Дополнительная статистика:")
    print("=" * 50)

    # Автоматическое определение категорий из описаний
    all_descriptions = [t.get('description', '') for t in current_transactions if t.get('description')]

    # Создаем список потенциальных категорий
    potential_categories = []
    for desc in all_descriptions:
        # Разбиваем описание на слова и берем первое слово как потенциальную категорию
        words = desc.split()
        if words:
            potential_categories.append(words[0].lower())

    # Берем наиболее частые слова как категории
    from collections import Counter
    common_categories = [cat for cat, count in Counter(potential_categories).most_common(5)]

    if common_categories:
        stats = process_bank_operations(current_transactions, common_categories)
        if stats:
            print("\nКоличество операций по типам:")
            for category, count in stats.items():
                print(f"  {category.capitalize()}: {count}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        sys.exit(1)
