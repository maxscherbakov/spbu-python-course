import pytest

from project.generators.primes_generator import primes_gen


@pytest.mark.parametrize("invalid_index", [-1, 0])
def test_invalid_index(invalid_index: int) -> None:
    """Test invalid indices raise IndexError in the decorated function."""
    with pytest.raises(IndexError):
        primes_gen(invalid_index)


@pytest.mark.parametrize(
    "index, expected_prime",
    [(1, 2), (3, 5), (500, 3571), (1000, 7919)],
)
def test_prime_gen_decorated(index: int, expected_prime: int) -> None:
    """Test the decorated primes_gen to verify nth prime."""
    assert primes_gen(index) == expected_prime


@pytest.mark.parametrize("invalid_index", [999, 1000])
def test_going_forward(invalid_index: int) -> None:
    """Checking that the generator is only going forward"""
    with pytest.raises(IndexError):
        primes_gen(invalid_index)
