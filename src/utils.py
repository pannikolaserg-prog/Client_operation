import json
from pathlib import Path
from typing import Any, Dict, List, Union


def load_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с данными транзакций.
        Если файл не найден, пуст, или не содержит список, возвращает [].
    """
    # Приведение к Path для удобства
    path = Path(file_path) if isinstance(file_path, str) else file_path

    # Проверка существования файла
    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            # Загрузка данных из файла
            data: Union[List, Dict] = json.load(f)

        # Проверка типа данных
        if isinstance(data, list):
            return data
        else:
            # Если данные не являются списком
            return []
    except FileNotFoundError:
        # Файл не найден - возвращаем пустой список
        return []
    except (json.JSONDecodeError, OSError):
        # Обработка ошибок парсинга JSON или чтения файла
        return []
