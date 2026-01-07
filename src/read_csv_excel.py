import os
from typing import Any, Dict, List

import pandas as pd

# Пути к файлам
csv_file_path = os.path.join("data", "transactions.csv")
excel_file_path = os.path.join("data", "transactions_excel.xlsx")

import csv


def read_csv_file(filepath: str = "data/transactions.csv") -> list[dict]:
    """
    Читает CSV файл и возвращает список словарей с транзакциями.

    Args:
        filepath: Путь к CSV файлу

    Returns:
        Список словарей с транзакциями
    """
    transactions = []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            # Используем csv.DictReader для автоматического разделения полей
            csv_reader = csv.DictReader(file, delimiter=";")

            for row in csv_reader:
                # Преобразуем строку в словарь
                transaction = {}
                for key, value in row.items():
                    transaction[key.strip()] = value.strip() if value else ""
                transactions.append(transaction)

        print(f"CSV прочитан: {len(transactions)} записей")
        return transactions

    except FileNotFoundError:
        print(f"Файл {filepath} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def read_excel_file() -> List[Dict[str, Any]]:
    """
    Читает данные из Excel файла и возвращает список словарей с транзакциями.

    Returns:
        List[Dict[str, Any]]: Список транзакций, где каждая транзакция - словарь
    """
    try:
        # Читаем Excel в DataFrame
        df = pd.read_excel(excel_file_path)
        print(f"Excel прочитан: {len(df)} записей")

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: файл {excel_file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []


# Минимальная проверка
print("Минимальная проверка функций:")

csv_result = read_csv_file()
print(f"CSV: {'✓' if csv_result else '✗'} {len(csv_result)} записей")

excel_result = read_excel_file()
print(f"Excel: {'✓' if excel_result else '✗'} {len(excel_result)} записей")

print(f"\nИтого: {len(csv_result) + len(excel_result)} транзакций")
