from functools import wraps
from typing import Callable, Any, Tuple
import inspect, copy, random


def cache_decorator(
    func: Any = None, *, max_results: Any = None
) -> Callable[..., Any]:
    if func is None:
        return lambda function: cache_decorator(
            function, max_results=max_results
        )
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


class Evaluated:
    def __init__(self, func: Any) -> None:
        if isinstance(func, Isolated):
            raise TypeError("You cannot combine Evaluated with Isolated.")
        self.func = func

    def execute(self) -> Any:
        return self.func()


class Isolated:
    def __init__(self, value: Any = None):
        if isinstance(value, Evaluated):
            raise TypeError("You cannot combine Isolated with Evaluated.")


def smart_args(
    function: Any = None, position_args: bool = False
) -> Callable[..., Any]:
    if function is None:
        return lambda func: smart_args(func, position_args=position_args)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        argspec = inspect.getfullargspec(function)
        default_kwarg: dict[str, Any] | None = argspec.kwonlydefaults
        if default_kwarg is not None:
            for key, value in default_kwarg.items():
                if key in kwargs:
                    if isinstance(value, Isolated):
                        kwargs[key] = copy.deepcopy(kwargs[key])
                elif isinstance(value, Evaluated):
                    kwargs[key] = value.execute()

        if position_args:
            default_args = argspec.defaults
            all_positional_args = argspec.args
            if default_args is not None and all_positional_args is not None:
                list_args = list()
                num_non_default_args = len(all_positional_args) - len(
                    default_args
                )
                for i, arg in enumerate(args):
                    if i < num_non_default_args or not isinstance(
                        default_args[i - num_non_default_args], Isolated
                    ):
                        list_args.append(arg)
                    else:
                        list_args.append(copy.deepcopy(arg))
                num_defined_default_args = len(args) - num_non_default_args
                for i in range(num_defined_default_args, len(default_args)):
                    if isinstance(default_args[i], Evaluated):
                        list_args.append(default_args[i].execute())
                    else:
                        list_args.append(default_args[i])
                return function(*list_args, **kwargs)
        return function(*args, **kwargs)

    return wrapper
