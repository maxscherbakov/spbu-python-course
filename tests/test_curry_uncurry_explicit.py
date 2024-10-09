import pytest
from project.curry_uncurry_explicit import curry_explicit, uncurry_explicit


def test_curry_string_three() -> None:
    # Curry function lambda
    curry_string_three = curry_explicit(
        (lambda x, y, z: f"<{x}, {y}, {z}>"), 3
    )
    assert "<12, 13, 14>" == curry_string_three(12)(13)(14)

    # Uncurry function lambda
    uncurry_string_three = uncurry_explicit(curry_string_three, 3)
    assert uncurry_string_three(123, 145, 254) == "<123, 145, 254>"


def test_curry_sum_four() -> None:
    # A function with initial arguments
    curry_sum_four = curry_explicit((lambda x, y, z, t: x + y + z + t), 4)(1)(
        2
    )
    assert curry_sum_four(3)(4) == 10

    uncurry_sum_four = uncurry_explicit(curry_sum_four, 2)
    assert uncurry_sum_four(3, 4) == 10


def test_currying_built_in_function_pow() -> None:
    assert curry_explicit(print, 2)(1)(2) is None

    s = curry_explicit(pow, 3)
    assert s(2)(2)(3) == 1

    s2 = uncurry_explicit(s, 3)
    assert s2(2, 4, 1000) == 16


def test_currying_built_in_function_print() -> None:
    assert curry_explicit(print, 2)(1, 2) is None
    assert uncurry_explicit(curry_explicit(print, 4)(12), 3)(1, 2, 3) is None
    with pytest.raises(TypeError):
        curry_explicit(print, 2)(1)(2)(3, 4, 5)
