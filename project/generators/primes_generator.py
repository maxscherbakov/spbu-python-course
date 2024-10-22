import math
from typing import Any, Generator, Callable


def get_nth_prime(
    function: Callable[[], Generator[Any, None, None]]
) -> Callable[..., Any]:
    """
    The decorator returns a function that returns the nth element of the generator.

    Args:
        function (Callable[[], Generator[Any, None, None]]): function returning the prime number generator.

    Returns:
        result (Callable[..., Any]): a function that accepts n and returns the nth prime number.
    """

    gen = function()
    num = next(gen)
    count = 1

    def wrapper(n: int) -> Any:
        nonlocal count, num

        if n < count:
            raise IndexError(
                f"The index must be greater than or equal to {count}"
            )
        if n == count:
            return num

        for i, element in enumerate(gen, start=count):
            if i + 1 == n:
                count = n
                num = element
                return element

    return wrapper


@get_nth_prime
def primes_gen() -> Generator[int, None, None]:
    """
    Function returning the prime number generator.

    Returns:
        result (Generator[int, None, None]): the prime number generator.
    """

    num = 2
    while True:
        is_prime = True
        limit = math.isqrt(num)

        for divisor in range(2, limit + 1):
            if num % divisor == 0:
                is_prime = False
                break

        if is_prime:
            yield num

        num += 1
