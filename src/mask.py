import logging
import os
from datetime import datetime

# Создаем папку для логов, если её нет
os.makedirs('logs', exist_ok=True)

# Создаем отдельный объект логгера для модуля masks
logger = logging.getLogger('mask')  # Изменил имя на 'mask' для соответствия тестам
logger.setLevel(logging.DEBUG)

# Убираем существующие обработчики, чтобы избежать дублирования
if logger.hasHandlers():
    logger.handlers.clear()

# Настраиваем file_handler для логгера модуля masks
try:
    file_handler = logging.FileHandler(
        filename='logs/mask.log',
        encoding='utf-8',
        mode='a'
    )
    file_handler.setLevel(logging.DEBUG)

    # Настраиваем file_formatter для логгера модуля masks
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Устанавливаем форматер для логгера модуля masks
    file_handler.setFormatter(file_formatter)

    # Добавляем handler для логгера модуля masks
    logger.addHandler(file_handler)

    # Отключаем propagation, чтобы не дублировать логи в корневом логгере
    logger.propagate = False

except Exception as e:
    # Если не удалось создать файловый handler, создаем только консольный
    print(f"Warning: Could not create log file: {e}")


def get_mask_card_number(number_card: str) -> str:
    """Функция принимает номер карты и возвращает его в замаскированном виде"""
    # Удаляем пробелы из номера карты, если они есть
    number_card = str(number_card).replace(" ", "")

    if not number_card:
        logger.warning('Получена пустая строка номера карты')
        return "**** **** **** ****"

    if len(number_card) < 6:
        logger.info(f'Обрабатываем короткие номера карт: {number_card}')
        # Для очень коротких номеров (меньше 6 символов)
        first_part = number_card[:4].ljust(4, "*")
        second_part = "**" if len(number_card) <= 4 else number_card[4:6]
        last_part = number_card[-4:].rjust(4, "*") if len(number_card) < 4 else number_card[-4:]
        return f"{first_part} {second_part}** **** {last_part}"

    # Стандартная обработка для номеров от 6 символов и больше
    logger.info(f'Маскируем номер карты: {number_card}')
    return f"{number_card[:4]} {number_card[4:6]}** **** {number_card[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскирует номер счета (показывает последние 4 цифры)"""
    account_number = str(account_number).replace(" ", "")

    if not account_number:
        logger.warning('Получена пустая строка номера счета')
        return "**"

    if len(account_number) < 4:
        logger.warning(f'Номер счета слишком короткий: {account_number}')
        return f"**{account_number[-len(account_number):]}"

    logger.info(f'Маскируем номер счета: {account_number}')
    return f"**{account_number[-4:]}"


# Добавляем проверку для предотвращения логирования при импорте в тестах
if __name__ == "__main__":
    logger.info("Логгер модуля mask инициализирован")
else:
    # Тихо инициализируем логгер без записи в лог
    pass