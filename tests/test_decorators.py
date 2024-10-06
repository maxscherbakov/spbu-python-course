import pytest
from project.decorators import cache_decorator


class TestCacheDecorator:
    def test_cache_fibonacci(self) -> None:
        @cache_decorator(max_results=3)
        def fibonacci(n: int) -> int:
            if n < 2:
                return n
            result: int = fibonacci(n - 1) + fibonacci(n - 2)
            return result

        for i in range(0, 1000):
            fibonacci(i)

        with pytest.raises(RecursionError):
            fibonacci(996)
