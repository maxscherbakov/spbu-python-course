from project.curry_uncurry_explicit import curry_explicit, uncurry_explicit


class TestCurryDecorator:
    def test_curry_string_three(self) -> None:
        # Curry function lambda
        curry_string_three = curry_explicit(
            (lambda x, y, z: f"<{x}, {y}, {z}>"), 3
        )
        assert "<12, 13, 14>" == curry_string_three(12)(13)(14)

        # Uncurry function lambda
        uncurry_string_three = uncurry_explicit(curry_string_three, 3)
        assert uncurry_string_three(123, 145, 254) == "<123, 145, 254>"

    def test_curry_sum_four(self) -> None:
        # A function with initial arguments
        curry_sum_four = curry_explicit((lambda x, y, z, t: x + y + z + t), 4)(
            1
        )(2)
        assert curry_sum_four(3)(4) == 10

        uncurry_sum_four = uncurry_explicit(curry_sum_four, 2)
        assert uncurry_sum_four(3, 4) == 10
