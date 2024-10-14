from typing import Any, Generator, Callable


def get_nth_element(
    func: Callable[[], Generator[Any, None, None]]
) -> Callable[..., Any]:
    def wrapper(n: int) -> Any:
        if n <= 0:
            raise IndexError("The index must be greater than 0")

        gen = func()
        for i, element in enumerate(gen, start=1):
            if i == n:
                return element

        raise IndexError(f"Generator does not have {n} elements.")

    return wrapper


@get_nth_element
def gen_primes() -> Generator[int, None, None]:
    primes = []
    num = 2
    while True:
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
            yield num
        num += 1
