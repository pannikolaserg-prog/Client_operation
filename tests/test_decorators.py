from src.decorators import log
import os
import tempfile
import pytest
from typing import Callable, Any, Generator, TextIO, Tuple, Dict, List
import functools
from _pytest.capture import CaptureFixture, CaptureResult
from _pytest.monkeypatch import MonkeyPatch


# Тестируемые функции с аннотациями типов
@log()
def successful_function(a: int, b: int) -> int:
    """Тестовая функция, которая всегда выполняется успешно"""
    return a + b


@log()
def failing_function(a: int, b: int) -> None:
    """Тестовая функция, которая всегда вызывает исключение"""
    raise ValueError("Test error")


@log()
def function_with_default_args(a: int, b: int = 10) -> int:
    """Тестовая функция с аргументами по умолчанию"""
    return a + b


@log()
def zero_args_function() -> int:
    """Тестовая функция с нулевыми аргументами"""
    return 42


@log()
def documented_function(x: int, y: int) -> int:
    """Тестовая функция с документацией"""
    return x + y


@log()
def unicode_function(text: str, number: int) -> str:
    """Тестовая функция с юникод-аргументами"""
    return f"{text}-{number}"


@log()
def complex_args_function(lst: List[int], dct: Dict[str, int]) -> int:
    """Тестовая функция со сложными аргументами"""
    return sum(lst) + sum(dct.values())


@log()
def none_return_function(x: int) -> None:
    """Тестовая функция, возвращающая None"""
    _ = x  # Используем аргумент, чтобы избежать предупреждения


# Fixtures с аннотациями типов
@pytest.fixture
def temp_log_file() -> Generator[str, None, None]:
    """Фикстура для создания временного лог-файла"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as tmp_file:
        tmp_filename: str = tmp_file.name

    try:
        yield tmp_filename
    finally:
        if os.path.exists(tmp_filename):
            os.unlink(tmp_filename)


# Тесты для вывода в консоль
def test_log_successful_execution_console(capsys: CaptureFixture[str]) -> None:
    """Тест успешного выполнения функции с выводом в консоль"""
    result: int = successful_function(3, 4)

    # Проверяем возвращаемое значение
    assert result == 7

    # Проверяем вывод в консоль
    captured: CaptureResult[str] = capsys.readouterr()
    assert "successful_function ok" in captured.out
    assert "error" not in captured.out


def test_log_failing_execution_console(capsys: CaptureFixture[str]) -> None:
    """Тест выполнения функции с ошибкой с выводом в консоль"""
    with pytest.raises(ValueError):
        failing_function(3, 4)

    # Проверяем вывод в консоль
    captured: CaptureResult[str] = capsys.readouterr()
    assert "failing_function error" in captured.out
    assert "ValueError" in captured.out
    assert "Test error" in captured.out
    assert "(3, 4)" in captured.out


def test_log_with_default_args_console(capsys: CaptureFixture[str]) -> None:
    """Тест функции с аргументами по умолчанию"""
    result: int = function_with_default_args(5)

    # Проверяем возвращаемое значение
    assert result == 15

    # Проверяем вывод в консоль
    captured: CaptureResult[str] = capsys.readouterr()
    assert "function_with_default_args ok" in captured.out


def test_log_failing_execution_file(temp_log_file: str) -> None:
    """Тест выполнения функции с ошибкой с записью в файл"""

    # Определяем функцию с декоратором для этого теста
    @log(filename=temp_log_file)
    def temp_failing_function(x: int, y: int) -> None:
        raise TypeError("File test error")

    # Вызываем функцию и проверяем, что исключение пробрасывается
    with pytest.raises(TypeError):
        temp_failing_function(5, 6)

    # Проверяем содержимое файла
    with open(temp_log_file, "r", encoding="utf-8") as f:
        content: str = f.read()

    assert "temp_failing_function error" in content
    assert "TypeError" in content
    assert "File test error" in content
    assert "(5, 6)" in content


def test_log_empty_args(temp_log_file: str) -> None:
    """Тест функции без аргументов"""

    @log(filename=temp_log_file)
    def no_args_function() -> str:
        return "success"

    result: str = no_args_function()
    assert result == "success"

    with open(temp_log_file, "r", encoding="utf-8") as f:
        content: str = f.read()

    assert "no_args_function ok" in content


def test_log_with_zero_args(capsys: CaptureFixture[str]) -> None:
    """Тест функции с нулевыми аргументами"""
    result: int = zero_args_function()
    assert result == 42

    captured: CaptureResult[str] = capsys.readouterr()
    assert "zero_args_function ok" in captured.out


def test_log_function_metadata() -> None:
    """Тест сохранения метаданных функции"""
    # Проверяем, что декоратор сохраняет метаданные
    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "Тестовая функция с документацией"


def test_log_with_none_filename(capsys: CaptureFixture[str]) -> None:
    """Тест явного указания None в качестве имени файла"""

    @log(filename=None)
    def explicit_none_function(x: int) -> int:
        return x * 3

    result: int = explicit_none_function(4)
    assert result == 12

    captured: CaptureResult[str] = capsys.readouterr()
    assert "explicit_none_function ok" in captured.out


def test_log_with_unicode_arguments(capsys: CaptureFixture[str]) -> None:
    """Тест функции с юникод-аргументами"""
    result: str = unicode_function("тест", 123)
    assert result == "тест-123"

    captured: CaptureResult[str] = capsys.readouterr()
    assert "unicode_function ok" in captured.out


def test_log_with_complex_arguments(capsys: CaptureFixture[str]) -> None:
    """Тест функции со сложными аргументами"""
    result: int = complex_args_function([1, 2, 3], {"a": 4, "b": 5})
    assert result == 15

    captured: CaptureResult[str] = capsys.readouterr()
    assert "complex_args_function ok" in captured.out


def test_log_return_none(capsys: CaptureFixture[str]) -> None:
    """Тест функции, возвращающей None"""
    result: None = none_return_function(5)
    assert result is None

    captured: CaptureResult[str] = capsys.readouterr()
    assert "none_return_function ok" in captured.out


class CustomError(Exception):
    """Пользовательское исключение для тестирования"""

    pass


def test_log_with_empty_string_filename(capsys: CaptureFixture[str]) -> None:
    """Тест с пустой строкой в качестве имени файла"""

    @log(filename="")
    def empty_filename_function(x: int) -> int:
        return x * 2

    # При пустом имени файла вывод должен идти в консоль
    result: int = empty_filename_function(3)
    assert result == 6

    captured: CaptureResult[str] = capsys.readouterr()
    assert "empty_filename_function ok" in captured.out


def test_log_with_special_characters_in_filename(temp_log_file: str) -> None:
    """Тест с специальными символами в имени файла"""
    # Создаем файл с "нестандартным" именем
    special_file = temp_log_file.replace(".txt", "_тест.txt")

    @log(filename=special_file)
    def special_filename_function(x: int) -> int:
        return x * 3

    try:
        result: int = special_filename_function(4)
        assert result == 12

        with open(special_file, "r", encoding="utf-8") as f:
            content: str = f.read()

        assert "special_filename_function ok" in content
    finally:
        if os.path.exists(special_file):
            os.unlink(special_file)


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v", "--tb=short"])
