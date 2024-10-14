import pytest

from project.generators.primes_generator import gen_primes


@pytest.mark.parametrize(
    "index, expected_prime",
    [(1, 2), (500, 3571), (1000, 7919)],
)
def test_prime_gen_decorated(index: int, expected_prime: int) -> None:
    assert gen_primes(index) == expected_prime


@pytest.mark.parametrize("invalid_index", [-1, 0])
def test_invalid_index(invalid_index: int) -> None:
    with pytest.raises(IndexError):
        gen_primes(invalid_index)
