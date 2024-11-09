from functools import wraps

def cache_decorator(func):
    """
    Декоратор, кэширующий результаты вызовов функции для определенных аргументов.

    Аргументы:
        func (Callable): Функция, которую требуется кэшировать.

    Возвращает:
        Callable: Обернутая функция с кэшированием результатов.
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Обертка для функции с кэшированием результатов.

        Аргументы:
            *args: Позиционные аргументы функции.
            **kwargs: Именованные аргументы функции.

        Возвращает:
            Результат вызова функции `func`.
        """
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper