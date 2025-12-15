import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List

from src.utils import load_transactions


def test_load_transactions_valid_file() -> None:
    """Тест загрузки валидного JSON файла со списком транзакций."""
    # Создаем временный файл с данными
    transactions: List[Dict[str, Any]] = [
        {"id": 1, "amount": 100.0, "currency": "RUB"},
        {"id": 2, "amount": 50.0, "currency": "USD"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(transactions, f)
        temp_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_path)
        assert result == transactions
    finally:
        os.unlink(temp_path)


def test_load_transactions_file_not_found() -> None:
    """Тест обработки отсутствующего файла."""
    result: List[Dict[str, Any]] = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_invalid_json() -> None:
    """Тест обработки файла с невалидным JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{invalid json")
        temp_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_not_a_list() -> None:
    """Тест обработки JSON, который не является списком."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"key": "value"}, f)  # Отправляем словарь, а не список
        temp_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_with_path_object() -> None:
    """Тест с передачей объекта Path вместо строки."""
    transactions: List[Dict[str, Any]] = [{"id": 1, "amount": 100.0, "currency": "RUB"}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(transactions, f)
        temp_path: Path = Path(f.name)

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_path)
        assert result == transactions
    finally:
        os.unlink(str(temp_path))
