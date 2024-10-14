import pytest
from project.generators.rgba_generator import get_nth_rgba_vec


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, (0, 0, 0, 0)),
        (1, (0, 0, 0, 2)),
        (50, (0, 0, 1, 0)),
        (256 * 50, (0, 1, 0, 0)),
        (256 * 256 * 50, (1, 0, 0, 0)),
    ],
)
def test_get_nth_rgba_vec(
    index: int, expected: tuple[int, int, int, int]
) -> None:
    result = get_nth_rgba_vec(index)
    assert result == expected


@pytest.mark.parametrize("invalid_index", [-1])
def test_invalid_index(invalid_index: int) -> None:
    with pytest.raises(IndexError):
        get_nth_rgba_vec(invalid_index)
