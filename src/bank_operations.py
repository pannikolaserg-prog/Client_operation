import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует список банковских операций по наличию строки в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в поле 'description'

    Returns:
        Отфильтрованный список словарей
    """
    if not data or not search:
        return []

    result = []
    # Используем re.escape для экранирования специальных символов и re.IGNORECASE для регистронезависимого поиска
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        # Проверяем наличие поля 'description' и соответствие шаблону
        if "description" in operation and operation["description"]:
            if pattern.search(operation["description"]):
                result.append(operation)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список названий категорий для поиска в поле 'description'

    Returns:
        Словарь с количеством операций по каждой категории
    """
    if not data or not categories:
        return {}

    # Используем Counter для подсчета
    counter = Counter()

    for operation in data:
        if "description" in operation and operation["description"]:
            description = operation["description"].lower()

            for category in categories:
                # Проверяем, содержится ли категория в описании (регистронезависимо)
                if category.lower() in description:
                    counter[category] += 1

    return dict(counter)
