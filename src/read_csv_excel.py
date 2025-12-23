import os
from typing import Any, Dict, List

import pandas as pd

# Пути к файлам
csv_file_path = os.path.join("data", "transactions.csv")
excel_file_path = os.path.join("data", "transactions_excel.xlsx")


def read_csv_file() -> List[Dict[str, Any]]:
    """
    Читает данные из CSV файла и возвращает список словарей с транзакциями.

    Returns:
        List[Dict[str, Any]]: Список транзакций, где каждая транзакция - словарь
    """
    try:
        # Читаем CSV в DataFrame
        df = pd.read_csv(csv_file_path)
        print(f"CSV прочитан: {len(df)} записей")

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict(orient="records")
        return transactions

    except FileNotFoundError:
        print(f"Ошибка: файл {csv_file_path} не найден")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
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
