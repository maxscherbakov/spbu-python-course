from random import randint
from typing import Any, Generator, List


def gen_rgba_vectors() -> Generator[List[List[int]], Any, None]:
    rgba_vectors = []
    while True:
        rgb = [randint(0, 255) for _ in range(3)]
        a = randint(0, 50) * 2
        rgba_vectors.append(rgb + [a])
        yield rgba_vectors


def get_i_element(
    generator: Generator[List[List[int]], Any, None], item_number
):
    rgba_vectors = next(generator)
    for _ in range(item_number - len(rgba_vectors)):
        rgba_vectors = next(generator)
    return rgba_vectors[item_number - 1]


def get_k_prime(
    item_number=1, generator: Generator[List[int], Any, None] = None
):
    if generator is None:
        return lambda gen: get_k_prime(item_number, gen)

    primes = next(generator)
    for _ in range(item_number - len(primes)):
        primes = next(generator)
    return primes[item_number - 1]


@get_k_prime()
def gen_primes():
    primes = []
    num = 2
    while True:
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
            yield num
        num += 1


generator = gen_primes()
for _ in range(2):
    print(next(generator))

g = gen_rgba_vectors()
g1 = g
f = get_i_element(g, 3)
f1 = get_i_element(g1, 3)
f2 = get_i_element(g1, 3)
print(f)
print(f1)
print(f2)
print(next(g))
