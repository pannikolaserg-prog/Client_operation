import os
import sys


# Добавляем путь к модулю для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Теперь импортируем функции из вашего модуля
from src.read_csv_excel import csv_file_path, excel_file_path, read_csv_file, read_excel_file

# Простые тесты функций
print("=" * 40)
print("ТЕСТИРОВАНИЕ ФУНКЦИЙ ЧТЕНИЯ")
print("=" * 40)

# Тест 1: Проверка существования файлов
print("\n📁 Тест 1: Проверка файлов")
print(f"CSV файл существует: {'✓' if os.path.exists(csv_file_path) else '✗'}")
print(f"Excel файл существует: {'✓' if os.path.exists(excel_file_path) else '✗'}")

# Тест 2: Чтение CSV
print("\n📄 Тест 2: Чтение CSV файла")
csv_data = read_csv_file()
print(f"Результат: список из {len(csv_data)} элементов")
print(f"Тип результата: {type(csv_data)}")

if csv_data:
    print(f"Тип элемента: {type(csv_data[0])}")
    print(f"Ключи в первой транзакции: {list(csv_data[0].keys())}")
    print(f"Пример первой транзакции:")
    for key, value in csv_data[0].items():
        print(f"  {key}: {value}")

# Тест 3: Чтение Excel
print("\n📊 Тест 3: Чтение Excel файла")
excel_data = read_excel_file()
print(f"Результат: список из {len(excel_data)} элементов")
print(f"Тип результата: {type(excel_data)}")

if excel_data:
    print(f"Тип элемента: {type(excel_data[0])}")
    print(f"Ключи в первой транзакции: {list(excel_data[0].keys())}")
    print(f"Пример первой транзакции:")
    for key, value in excel_data[0].items():
        print(f"  {key}: {value}")

# Тест 4: Общая статистика
print("\n📈 Тест 4: Общая статистика")
total_transactions = len(csv_data) + len(excel_data)
print(f"Всего транзакций: {total_transactions}")
print(f"Из CSV: {len(csv_data)}")
print(f"Из Excel: {len(excel_data)}")

# Тест 5: Проверка структуры
print("\n🔍 Тест 5: Проверка структуры данных")
if csv_data and excel_data:
    csv_keys = set(csv_data[0].keys())
    excel_keys = set(excel_data[0].keys())

    print(f"Ключи CSV: {csv_keys}")
    print(f"Ключи Excel: {excel_keys}")

    if csv_keys == excel_keys:
        print("✓ Структуры идентичны")
    else:
        print("⚠ Структуры различаются")
        print(f"Разница: {csv_keys.symmetric_difference(excel_keys)}")
else:
    print("Недостаточно данных для проверки")

print("\n" + "=" * 40)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 40)
