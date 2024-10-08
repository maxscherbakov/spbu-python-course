from typing import Callable, Any
from functools import wraps


def curry_explicit(
    function: Callable[..., Any], arity: Any
) -> Callable[..., Any]:
    """
    A function for currying an accepted function.
    """
    if not is_arity(arity):
        raise TypeError("Input must be a non-negative numeric.")

    @wraps(function)
    def wrapper(*args: Any) -> Any:
        if len(args) == arity:
            return function(*args)
        return lambda *next_args: wrapper(*(args + next_args))

    return wrapper


def uncurry_explicit(
    function: Callable[..., Any], arity: Any
) -> Callable[..., Any]:
    """
    A function for uncurrying an accepted function.
    """
    if not is_arity(arity):
        raise TypeError("Input must be a non-negative numeric.")

    @wraps(function)
    def wrapper(*args: Any) -> Any:
        if len(args) != arity:
            raise ValueError(
                "More parameters are passed than the arity of the function."
            )
        res = function
        for arg in args:
            res = res(arg)
        return res

    return wrapper


def is_arity(obj: Any) -> bool:
    """
    The function of checking the parameter passed to arity.
    """
    try:
        if obj >= 0:
            return True
        return False
    except TypeError:
        return False
