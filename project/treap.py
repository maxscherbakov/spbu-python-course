import random
from collections.abc import MutableMapping
from typing import Tuple, Generator, Any


class TreapNode:
    """A node in the treap. Stores key, priority, and value data."""

    def __init__(self, key: Any, value: Any):
        self.value: Any = value
        self.key: Any = key
        self.priority = random.random()
        self.left: TreapNode | None = None
        self.right: TreapNode | None = None


def count_nodes(node: TreapNode | None) -> int:
    """A function for counting the number of child nodes."""
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1

    res = 1
    res += count_nodes(node.left) + count_nodes(node.right)
    return res


class Treap(MutableMapping):
    """
    The class of the treap. Stores the main vertex and the number of nodes.
    This class implements a mutable mapping, as defined by the `collections.abc.MutableMapping` class.


    Methods:
    -------
    `__getitem__(key: Any) -> Any`:
        Getting a vertex by key through square brackets.

    `_get(node: TreapNode | None, key: Any) -> Any`:
        Recursive search for the node value.

    `__setitem__(self, key: Any, value: Any)`:
        Adding or reassigning the node value.

    `_set(current_node: TreapNode | None, node: TreapNode | None) -> TreapNode`:
        Recursive reassignment of node values.

    `__delitem__(key: Any)`:
        Removing a node from the treap.

    `_del(node: TreapNode, key: Any) -> TreapNode`:
        Recursively reassigning child nodes when deleted.

    `split(node: TreapNode | None, key: Any) -> Tuple[TreapNode | None, TreapNode | None]`:
        Splitting a treap into two.

    `merge(left: TreapNode | None, right: TreapNode | None) -> TreapNode:`:
        Merging two treap into one.

    ` __iter__() -> Generator[Any, None, None]`:
        Direct iteration through the treap.

    `_iter_gen(node: TreapNode | None) -> Generator[Any, None, None]`:
        A generator for direct iteration through the treap.

    ` __reversed__() -> Generator[Any, None, None]`:
        Reverse iteration through the treap.

    `_reversed_gen(node: TreapNode | None) -> Generator[Any, None, None]`:
        A generator for reverse iteration through the treap.

    '__contains__(key: Any) -> bool':
        Checking contains the key is enabled in the treap. Operator in.

    '__len__() -> int':
        Returns the number of nodes in the treap.

    'print_treap()':
        Output information about the treap to the console.

    '_rotate_right(node: TreapNode) -> TreapNode':
        A static method for rotating the tree to the right.

    '_rotate_right(node: TreapNode) -> TreapNode':
        A static method for rotating the tree to the left.

    """

    def __init__(self, root: TreapNode | None = None):
        """Initializes a Treap object."""
        self.root = root
        self._count_nodes = count_nodes(root)

    def __getitem__(self, key: Any) -> Any:
        """
        Getting a vertex by key through square brackets.

        Args:
            key (Any): the key of the node to be retrieved.

        Returns:
            result (Any): the value of the desired node.
        """
        return self._get(self.root, key)

    def _get(self, node: TreapNode | None, key: Any) -> Any:
        """
        Recursive search for the node value.

        Args:
            node (TreapNode | None): the current crawl node.
            key (Any): the key of the node to be retrieved.

        Returns:
            result (Any): the value of the desired node.
        """
        if node is None:
            raise KeyError(f"Key {key} not found.")
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        else:
            return node.value

    def __setitem__(self, key: Any, value: Any):
        """
        Adding or reassigning the node value.

        Args:
            key (Any): the key of the node to add.
            value (Any): the value of the node to add.
        """
        self.root = self._set(self.root, TreapNode(key, value))

    def _set(
        self, current_node: TreapNode | None, node: TreapNode
    ) -> TreapNode:
        """
        Recursive reassignment of node values.

        Args:
            current_node (TreapNode | None): the current crawl node.
            node (TreapNode | None): the node to add.

        Returns:
            result (TreadNode): child node
        """
        if current_node is None:
            self._count_nodes += 1
            return node

        if node.key < current_node.key:
            current_node.left = self._set(current_node.left, node)
            if current_node.left.priority > current_node.priority:
                current_node = self._rotate_right(current_node)
        elif node.key > current_node.key:
            current_node.right = self._set(current_node.right, node)
            if current_node.right.priority > current_node.priority:
                current_node = self._rotate_left(current_node)
        else:
            current_node.value = node.value

        return current_node

    def __delitem__(self, key: Any):
        """
        Removing a node from the treap.

        Args:
            key (Any): the key of the node to delete.
        """
        self.root = self._del(self.root, key)
        self._count_nodes -= 1

    def _del(self, node: TreapNode | None, key: Any) -> TreapNode | None:
        """
        Recursively reassigning child nodes when deleted.

        Args:
            node (TreapNode): the current crawl node.
            key (Any): the key of the node to delete.

        Returns:
            result (TreapNode): child node.
        """
        if node is None:
            raise KeyError(f"Key {key} not found.")

        if key < node.key:
            node.left = self._del(node.left, key)
        elif key > node.key:
            node.right = self._del(node.right, key)
        else:
            return self.merge(node.left, node.right)

        return node

    @staticmethod
    def split(
        node: TreapNode | None, key: Any
    ) -> Tuple[TreapNode | None, TreapNode | None]:
        """
        Splitting a treap into two.

        Args:
            node (TreapNode | None): the current crawl node.
            key (Any): the key of the node to split by

        Returns:
            result (Tuple[TreapNode | None, TreapNode | None]): two root nodes of a split treap.
        """
        if node is None:
            return None, None
        if node.key < key:
            left, right = Treap.split(node.right, key)
            node.right = left
            return node, right
        else:
            left, right = Treap.split(node.left, key)
            node.left = right
            return left, node

    @staticmethod
    def merge(
        left: TreapNode | None, right: TreapNode | None
    ) -> TreapNode | None:
        """
        Merging two treap into one.

        Args:
            left (TreapNode | None): the left node for merging.
            right (TreapNode | None): the right node for merging.

        Returns:
            result (TreapNode): root node after merging.
        """
        if left is None:
            return right
        if right is None:
            return left

        if left.priority > right.priority:
            left.right = Treap.merge(left.right, right)
            return left
        else:
            right.left = Treap.merge(left, right.left)
            return right

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Direct iteration through the treap.

        Returns:
            result (Generator[Any, None, None]): a generator for direct iteration.
        """
        yield from self._iter_gen(self.root)

    def _iter_gen(self, node: TreapNode | None) -> Generator[Any, None, None]:
        """
        A generator for direct iteration through the treap.

        Args:
            node (TreapNode | None): the current crawl node.

        Returns:
            result (Generator[Any, None, None]): a generator for direct iteration.
        """
        if node is not None:
            yield from self._iter_gen(node.left)
            yield node
            yield from self._iter_gen(node.right)

    def __reversed__(self) -> Generator[Any, None, None]:
        """
        Reverse iteration through the treap.

        Returns:
            result (Generator[Any, None, None]): a generator for reverse iteration.
        """
        yield from self._reversed_gen(self.root)

    def _reversed_gen(
        self, node: TreapNode | None
    ) -> Generator[Any, None, None]:
        """
        A generator for reverse iteration through the treap.

        Args:
            node (TreapNode | None): the current crawl node.

        Returns:
            result (Generator[Any, None, None]): a generator for reverse iteration.
        """
        if node is not None:
            yield from self._reversed_gen(node.right)
            yield node
            yield from self._reversed_gen(node.left)

    def __contains__(self, key: Any) -> bool:
        """
        Checking contains the key is enabled in the treap. Operator in.

        Args:
            key (Any): the key to check for contains in the treap.

        Returns:
            result (bool): is the key included in the treap.
        """
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        """Returns the number of nodes in the treap."""
        return self._count_nodes

    def print_treap(self):
        """Output information about the treap to the console."""
        print("Treap:")
        for node in self:
            print(f"Key: {node.key}, Value: {node.value}")

    @staticmethod
    def _rotate_right(node: TreapNode) -> TreapNode:
        """
        A static method for rotating the tree to the right.

        Args:
            node (TreapNode): the vertex relative to which you want to make a rotation.

        Returns:
            result (TreapNode): new root node.
        """
        if node.left is None:
            raise ValueError("Node must have a left child for rotation.")
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    @staticmethod
    def _rotate_left(node: TreapNode) -> TreapNode:
        """
        A static method for rotating the tree to the left.

        Args:
            node (TreapNode): the vertex relative to which you want to make a rotation.

        Returns:
            result (TreapNode): new root node.
        """
        if node.right is None:
            raise ValueError("Node must have a right child for rotation.")
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root
