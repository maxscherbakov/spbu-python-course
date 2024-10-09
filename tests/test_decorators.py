import pytest
from unittest.mock import patch, call
from project.decorators import cache_decorator, smart_args, Evaluated, Isolated
from typing import Any
import random


def test_cache_fibonacci() -> None:
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
        fibonacci(1000)
        fibonacci(996)


@patch("builtins.print")
def test_without_cache_function_with_non_cached_arguments(
    mocked_print: Any,
) -> None:
    # Checking that the function works without a cache
    p = cache_decorator(print)
    p(1, 2, 3)
    p(1, 2, 3)
    assert mocked_print.mock_calls == [call(1, 2, 3), call(1, 2, 3)]


@patch("builtins.print")
def test_cache_function_with_non_cached_arguments(mocked_print: Any) -> None:
    # The function is triggered only once
    p2 = cache_decorator(print, cache_size=2)
    p2(4, 5, 6)
    p2("Hello, World!")
    p2(4, 5, 6)
    p2("Hello, World!")
    assert mocked_print.mock_calls == [call(4, 5, 6), call("Hello, World!")]


def test_cache_built_in_functions() -> None:
    # Checking the operation of the built-in function after caching
    s = cache_decorator(sum, cache_size=3)
    assert s((1, 2, 3)) == 6

    # Checking the launch of a cached function from unhashable type: 'list'
    with pytest.raises(TypeError):
        s([1, 2, 3])


def test_without_cache_built_in_functions() -> None:
    # Checking the launch of a non-cached function from unhashable type: 'list'
    s = cache_decorator(sum)
    assert s([1, 2, 3]) == 6


def test_without_cache() -> None:
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


def test_combination_isolated_evaluated() -> None:
    # Checking that Evaluated cannot be called from Isolated and vice versa
    with pytest.raises(TypeError):
        Isolated(Evaluated(get_random_number))
        Evaluated(Isolated())


def test_only_kwargs_isolation() -> None:
    @smart_args
    def check_isolation(*, d: Any = Isolated()) -> Any:
        d["a"] = 0
        return d

    no_mutable = {"a": 10}
    # Checking that no_mutable has not changed during transmission via Isolated()
    assert check_isolation(d=no_mutable) == {"a": 0}
    assert no_mutable == {"a": 10}


def test_only_kwargs_evaluated() -> None:
    @smart_args
    def check_evaluation(
        *, x: int = get_random_number(), y: Any = Evaluated(get_random_number)
    ) -> Any:
        return x, y

    # Checking that Evaluated is triggered without passing an argument
    assert check_evaluation()[0] == check_evaluation()[0]
    assert check_evaluation(y=150)[1] == 150


def test_only_kwargs_isolated_evaluation() -> None:
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


def test_all_positional_arguments_defaulted() -> None:
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

    # Checking that Isolated can be positional parameters of a function
    no_mutable = {"a": 10}
    res1 = check_isolated_evaluation(no_mutable, x=no_mutable)
    assert res1[0] == {"a": 10, "b": 1}
    assert no_mutable == {"a": 10}
    assert 0 <= res1[1] < 100

    # Checking that Evaluated can be positional parameters of a function
    res2 = check_isolated_evaluation(no_mutable, 105, x=no_mutable)
    assert res2[1] == 105


def test_with_other_positional_arguments() -> None:
    @smart_args(position_args=True)
    def check_isolated_evaluation(
        flag: bool,
        z: int,
        a: Any = Isolated(),
        b: Any = Evaluated(get_random_number),
        c: int = 11,
        *,
        x: Any = Isolated(),
        y: Any = Evaluated(get_random_number)
    ) -> Any:
        x["a"] = 0
        a["b"] = 1
        return a, b, c, x, y, flag, z

    # Checking that Evaluated, Isolated and other args can be positional parameters of a function
    no_mutable = {"a": 10}
    res1 = check_isolated_evaluation(True, 7, no_mutable, x=no_mutable)
    assert res1[0] == {"a": 10, "b": 1}
    assert no_mutable == {"a": 10}
    assert 0 <= res1[1] < 100
    assert res1[-2] == True
    assert res1[-1] == 7
    assert res1[2] == 11
