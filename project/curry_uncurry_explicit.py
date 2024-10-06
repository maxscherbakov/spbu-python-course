from typing import Callable, Any


def curry_explicit(
    function: Callable[..., Any], arity: Any
) -> Callable[..., Any]:
    if not is_arity(arity):
        raise TypeError("Input must be a non-negative numeric.")

    def wrapper(*args: Any) -> Any:
        if len(args) == arity:
            return function(*args)
        else:
            return lambda *next_args: wrapper(*(args + next_args))

    return wrapper


def uncurry_explicit(
    function: Callable[..., Any], arity: Any
) -> Callable[..., Any]:
    if not is_arity(arity):
        raise TypeError("Input must be a non-negative numeric.")

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
    try:
        if obj >= 0:
            return True
        return False
    except TypeError:
        return False
