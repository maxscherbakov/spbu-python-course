import pytest
from project.decorators import cache_decorator, smart_args, Evaluated, Isolated
from typing import Any
import random


class TestCacheDecorator:
    def test_cache_fibonacci(self) -> None:
        @cache_decorator(cache_size=3)
        def fibonacci(n: int) -> int:
            if n < 2:
                return n
            result: int = fibonacci(n - 1) + fibonacci(n - 2)
            return result

        # Calling the fibonacci function to check the caching of results
        for i in range(0, 1000):
            fibonacci(i)

        fibonacci(999)
        fibonacci(998)
        fibonacci(997)
        # Checking for RecursionError when calling fibonacci with an uncached number
        with pytest.raises(RecursionError):
            fibonacci(996)

    def test_without_cache(self) -> None:
        @cache_decorator
        def fibonacci(n: int) -> int:
            if n < 2:
                return n
            result: int = fibonacci(n - 1) + fibonacci(n - 2)
            return result

        # Checking for RecursionError when calling fibonacci without cache
        with pytest.raises(RecursionError):
            fibonacci(900)


def get_random_number() -> int:
    return random.randint(0, 100)


class TestIsolatedEvaluated:
    def test_combination_isolated_evaluated(self) -> None:
        # Checking that Evaluated cannot be called from Isolated and vice versa
        with pytest.raises(TypeError):
            Isolated(Evaluated(get_random_number))
            Evaluated(Isolated())


class TestSmartArgs:
    def test_only_kwargs_isolation(self) -> None:
        @smart_args
        def check_isolation(*, d: Any = Isolated()) -> Any:
            d["a"] = 0
            return d

        no_mutable = {"a": 10}
        # Checking that no_mutable has not changed during transmission via Isolated()
        assert check_isolation(d=no_mutable) == {"a": 0}
        assert no_mutable == {"a": 10}

    def test_only_kwargs_evaluated(self) -> None:
        @smart_args
        def check_evaluation(
            *,
            x: int = get_random_number(),
            y: Any = Evaluated(get_random_number)
        ) -> Any:
            return x, y

        # Checking that Evaluated is triggered without passing an argument
        assert check_evaluation()[0] == check_evaluation()[0]
        assert check_evaluation()[1] != check_evaluation()[1]
        assert check_evaluation(y=150)[1] == 150

    def test_only_kwargs_isolated_evaluation(self) -> None:
        @smart_args
        def check_isolated_evaluation(
            *, x: Any = Isolated(), y: Any = Evaluated(get_random_number)
        ) -> Any:
            x["a"] = 0
            return x, y

        # Checking that Evaluated and Isolated can be parameters of the same function
        no_mutable = {"a": 10}
        res1 = check_isolated_evaluation(x=no_mutable)
        res2 = check_isolated_evaluation(x=no_mutable, y=150)

        assert res1[0] == {"a": 0}
        assert no_mutable == {"a": 10}
        assert res2[1] == 150

    def test_with_position_args(self) -> None:
        @smart_args(position_args=True)
        def check_isolated_evaluation(
            a: Any = Isolated(),
            b: Any = Evaluated(get_random_number),
            *,
            x: Any = Isolated(),
            y: Any = Evaluated(get_random_number)
        ) -> Any:
            x["a"] = 0
            a["b"] = 1
            return a, b, x, y

        # Checking that Evaluated and Isolated can be positional parameters of a function
        no_mutable = {"a": 10}
        res1 = check_isolated_evaluation(no_mutable, x=no_mutable)
        res2 = check_isolated_evaluation(no_mutable, 105, x=no_mutable)
        assert res1[0] == {"a": 10, "b": 1}
        assert no_mutable == {"a": 10}
        assert 0 <= res1[1] < 100
        assert res2[1] == 105
