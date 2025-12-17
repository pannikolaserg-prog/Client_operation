import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Union

# Создаем папку для логов, если её нет
os.makedirs('logs', exist_ok=True)

# Создаем отдельный объект логгера для модуля utils
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)

# Убираем существующие обработчики, чтобы избежать дублирования
if logger.hasHandlers():
    logger.handlers.clear()

# Настраиваем file_handler для логгера модуля utils
try:
    file_handler = logging.FileHandler(
        filename='logs/utils.log',
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)

    # Настраиваем file_formatter для логгера модуля utils
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Устанавливаем форматер для логгера модуля utils
    file_handler.setFormatter(file_formatter)

    # Добавляем handler для логгера модуля utils
    logger.addHandler(file_handler)

    # Отключаем propagation, чтобы не дублировать логи в корневом логгере
    logger.propagate = False

except Exception as e:
    # Если не удалось создать файловый handler, создаем только консольный
    print(f"Warning: Could not create log file: {e}")


def load_transactions(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с данными транзакций.
        Если файл не найден, пуст, или не содержит список, возвращает [].
    """
    # Логирование начала выполнения функции
    logger.debug(f"Начало загрузки транзакций из файла: {file_path}")

    try:
        # Приведение к Path для удобства
        path = Path(file_path) if isinstance(file_path, str) else file_path

        # Проверка существования файла
        if not path.exists():
            logger.error(f"Файл не найден: {path.absolute()}")
            return []

        # Проверка размера файла
        file_size = path.stat().st_size
        logger.debug(f"Размер файла: {file_size} байт")

        if file_size == 0:
            logger.warning(f"Файл пуст: {path.absolute()}")
            return []

        with open(path, "r", encoding="utf-8") as f:
            # Загрузка данных из файла
            data: Union[List, Dict] = json.load(f)

        # Логирование успешного парсинга
        logger.info(f"Успешно загружены данные из файла: {path.absolute()}")

        # Проверка типа данных
        if isinstance(data, list):
            return data
        else:
            # Если данные не являются списком
            logger.error(f"Данные в файле не являются списком. Тип данных: {type(data)}")
            return []
    except FileNotFoundError as e:
        # Файл не найден
        logger.error(f"Файл не найден: {str(e)}")
        return []
    except (json.JSONDecodeError, OSError) as e:
        # Обработка ошибок парсинга JSON или чтения файла
        logger.error(f"Ошибка при чтении файла {file_path}: {str(e)}")
        return []
    except Exception as e:
        # Обработка любых других ошибок
        logger.error(f"Непредвиденная ошибка при загрузке транзакций: {str(e)}")
        return []


# Добавляем проверку для предотвращения логирования при импорте в тестах
if __name__ == "__main__":
    logger.info("Логгер модуля utils инициализирован")
else:
    # Тихо инициализируем логгер без записи в лог
    pass