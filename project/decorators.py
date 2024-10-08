from functools import wraps
from typing import Callable, Any, Dict
import inspect, copy


def cache_decorator(
    function: Any = None, *, cache_size: Any = None
) -> Callable[..., Any]:
    """
    Function Caching decorator.
    """
    if function is None:
        return lambda func: cache_decorator(func, cache_size=cache_size)

    cache: Dict[Any, Any] = {}

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not cache_size:
            return function(*args, **kwargs)
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            result = function(*args, **kwargs)
            if len(cache) == cache_size:
                cache.pop(next(iter(cache)))
            cache[key] = result
        return cache[key]

    return wrapper


class Evaluated:
    """
    Substitutes the default value calculated at the time of the call. Takes as an argument a function without arguments that returns something.
    """

    def __init__(self, func: Any) -> None:
        """
        Initializes a Evaluated object.
        """
        if isinstance(func, Isolated):
            raise TypeError("You cannot combine Evaluated with Isolated.")
        self.func = func

    def execute(self) -> Any:
        """
        Performs a function call.
        """
        return self.func()


class Isolated:
    """
    A dummy default value. The argument must be passed, but at the time of transmission it is copied (deep copy).
    """

    def __init__(self, value: Any = None):
        """
        Initializes a Isolated object.
        """
        if isinstance(value, Evaluated):
            raise TypeError("You cannot combine Isolated with Evaluated.")


def smart_args(
    function: Any = None, position_args: bool = False
) -> Callable[..., Any]:
    """
    Decorator for analyzing arguments of the Isolated and Evaluated types.
    """
    if function is None:
        return lambda func: smart_args(func, position_args=position_args)

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        argspec = inspect.getfullargspec(function)
        default_kwarg = argspec.kwonlydefaults
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
