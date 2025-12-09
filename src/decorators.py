import functools
from typing import Callable, Any


def log(filename: str = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Если задан, логи пишутся в файл, иначе - в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message.strip())

                return result

            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}: {str(e)}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(message)
                else:
                    print(message.strip())

                raise

        return wrapper

    return decorator


# Пример использования согласно условию
if __name__ == "__main__":
    @log(filename="mylog.txt")
    def my_function(x, y):
        return x + y


    # Успешное выполнение
    my_function(1, 2)


    # Функция с ошибкой
    @log()
    def divide(a, b):
        return a / b


    try:
        divide(10, 0)
    except:
        pass