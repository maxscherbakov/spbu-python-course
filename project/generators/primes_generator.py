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

    count = 0

    def wrapper(n: int) -> Any:
        nonlocal count

        if n <= count:
            raise IndexError(f"The index must be greater than {n}")

        for i, element in enumerate(gen, start=count):
            if i + 1 == n:
                count = n
                return element

    gen = function()
    return wrapper


@get_nth_prime
def primes_gen() -> Generator[int, None, None]:
    """
    Function returning the prime number generator.

    Returns:
        result (Generator[int, None, None]): the prime number generator.
    """

    primes: list[int] = []
    num = 2
    while True:
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
            yield num
        num += 1
