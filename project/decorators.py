from functools import wraps
from typing import Callable, Any


def cache_decorator(max_results: Any = None) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache: dict[Any, Any] = {}

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not max_results:
                return func(*args, **kwargs)
            key = (args, frozenset(kwargs.items()))
            if key not in cache:
                result = func(*args, **kwargs)
                if len(cache) == max_results:
                    cache.pop(next(iter(cache)))
                cache[key] = result
            return cache[key]

        return wrapper

    return decorator
