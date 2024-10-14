from typing import Generator
from itertools import product


def get_rgba_gen() -> Generator[tuple[int, int, int, int], None, None]:
    """
    A function that returns a generator of 4-dimensional rgba vectors.

    Returns:
        result (Generator[tuple[int, int, int, int], None, None]): generator of 4-dimensional rgba vectors.
    """
    return (
        (r, g, b, a * 2)
        for r, g, b in product(range(256), repeat=3)
        for a in range(0, 50)
    )


def get_nth_rgba_vec(n: int) -> tuple[int, int, int, int]:
    """
    A function that returns the nth element of a set of 4-dimensional rgba vectors.

    Args:
        n (int): the element number of the vector set.

    Returns:
        result (tuple[int, int, int, int]): the vector is at the nth position in the set.
    """
    if n < 0:
        raise IndexError("`n` must be non-negative")

    gen = get_rgba_gen()

    for i, val in enumerate(gen):
        if i == n:
            return val

    raise IndexError(f"Generator does not have {n} elements.")
