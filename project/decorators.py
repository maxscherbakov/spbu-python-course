from functools import wraps
from typing import Callable, Any, Dict
import inspect, copy


def cache_decorator(
    function: Any = None, *, cache_size: int = 0
) -> Callable[..., Any]:
    """
    Function Caching decorator.

    Args:
        function (Callable[..., Any]: the function to implement caching for.
        cache_size (int): the number of recent results for the cache.

    Returns:
        result (Callable[..., Any]: a function that supports caching.
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
        Initializes Evaluated object.
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
        Initializes Isolated object.
        """
        if isinstance(value, Evaluated):
            raise TypeError("You cannot combine Isolated with Evaluated.")


def smart_args(
    function: Any = None, position_args: bool = False
) -> Callable[..., Any]:
    """
    Decorator for analyzing arguments of the Isolated and Evaluated types.

    Args:
        function (Callable[..., Any]: a function that should support Isolated and Evaluated as default arguments.
        position_args (bool): a parameter that determines whether positional arguments need to be supported.

    Returns:
        result (Callable[..., Any]: a function that supports Isolated and Evaluated as default arguments.
    """
    if function is None:
        return lambda func: smart_args(func, position_args=position_args)

    argspec = inspect.getfullargspec(function)
    default_kwarg = argspec.kwonlydefaults
    default_args = argspec.defaults
    all_positional_args = argspec.args

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if default_kwarg is not None:
            for key, value in default_kwarg.items():
                if key in kwargs:
                    if isinstance(value, Isolated):
                        kwargs[key] = copy.deepcopy(kwargs[key])
                elif isinstance(value, Evaluated):
                    kwargs[key] = value.execute()

        if (
            position_args
            and default_args is not None
            and all_positional_args is not None
        ):
            list_args = list()
            num_non_default_args = len(all_positional_args) - len(default_args)
            for i in range(0, len(all_positional_args)):
                if i < len(args):
                    if i < num_non_default_args or not isinstance(
                        default_args[i - num_non_default_args], Isolated
                    ):
                        list_args.append(args[i])
                    else:
                        list_args.append(copy.deepcopy(args[i]))
                else:
                    if isinstance(
                        default_args[i - num_non_default_args], Evaluated
                    ):
                        list_args.append(
                            default_args[i - num_non_default_args].execute()
                        )
                    else:
                        list_args.append(
                            default_args[i - num_non_default_args]
                        )
            return function(*list_args, **kwargs)
        return function(*args, **kwargs)

    return wrapper
