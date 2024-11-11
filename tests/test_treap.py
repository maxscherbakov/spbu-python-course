from project.treap import Treap
import pytest


@pytest.fixture
def some_treap():
    """Initializing the treap for tests."""
    treep = Treap()
    treep[0] = "1"
    treep[-1] = "2"
    treep[1] = "3"
    treep[-2] = "4"
    treep[-0.5] = "5"
    return treep


@pytest.mark.parametrize(
    "key,value",
    [
        (0, "1"),
        (-1, "2"),
        (1, "3"),
        (-2, "4"),
        (-0.5, "5"),
    ],
)
def test_getitem(some_treap, key, value):
    """Test that the value is returned by the key through square brackets."""
    assert some_treap[key] == value


@pytest.mark.parametrize(
    "key,value",
    [
        (-10, "A"),
        (10, "B"),
        (-20, "C"),
        (-5, "D"),
    ],
)
def test_setitem(some_treap, key, value):
    """Test that the values are correctly assigned by the key."""
    some_treap[key] = value
    assert some_treap[key] == value


def test_update_key():
    """Test is that when the value is set again, the previous one is replaced."""
    treep = Treap()
    treep[5] = "value1"
    treep[5] = "value2"
    assert treep[5] == "value2"
    assert len(treep) == 1


def test_delete(some_treap):
    """Test is that the elements are removed from the tree."""
    assert len(some_treap) == 5
    del some_treap[-0.5]
    assert len(some_treap) == 4

    with pytest.raises(KeyError):
        _ = some_treap[5]


def test_split(some_treap):
    """Test is that the keys are distributed correctly when splitting."""
    left, right = some_treap.split(some_treap.root, 1)
    treap_left = Treap(left)
    treap_right = Treap(right)
    assert all(node.key < 1 for node in treap_left)
    assert len(treap_left) == 4

    assert all(node.key >= 1 for node in treap_right)
    assert len(treap_right) == 1


def test_merge():
    """Test is that the keys are distributed correctly during the merge."""
    left_treap = Treap()
    right_treap = Treap()
    left_treap[-2] = "-2"
    left_treap[-1] = "-1"
    right_treap[2] = "2"
    right_treap[1] = "1"
    merged_root = Treap.merge(left_treap.root, right_treap.root)
    merged_treap = Treap(merged_root)
    assert [node.key for node in merged_treap] == [-2, -1, 1, 2]
    assert len(merged_treap) == 4


def test_in_operator(some_treap):
    """Test that the in operator works correctly."""
    assert 1 in some_treap
    assert 3 not in some_treap


def test_empty_treap():
    """Test is that an empty tree has zero nodes."""
    assert len(Treap()) == 0


def test_iteration(some_treap):
    """Test is that the iteration is working correctly."""
    assert list(node.key for node in some_treap) == [-2, -1, -0.5, 0, 1]


def test_reversed_iteration(some_treap):
    """Test is that the reversed iteration is working correctly."""
    assert list(node.key for node in reversed(some_treap)) == [
        1,
        0,
        -0.5,
        -1,
        -2,
    ]


def test_str_treap(some_treap):
    """Test is that the tree is correctly represented as a string."""
    expected_str = "Treap:\nKey: -2, Value: 4\nKey: -1, Value: 2\nKey: -0.5, Value: 5\nKey: 0, Value: 1\nKey: 1, Value: 3\n"
    assert str(some_treap) == expected_str
