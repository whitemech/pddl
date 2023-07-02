#
# Copyright 2021-2023 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""Helper functions."""

import re
from pathlib import Path
from typing import (
    AbstractSet,
    Any,
    Callable,
    Collection,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
)

_Node = TypeVar("_Node")


def _get_current_path() -> Path:
    """Get the path to the file where the function is called."""
    import inspect
    import os

    return Path(os.path.dirname(inspect.getfile(inspect.currentframe()))).parent  # type: ignore


def assert_(condition: bool, message: str = "") -> None:
    """
    User-defined assert.

    This function is useful to avoid the use of the built-in assert statement, which is removed
        when the code is compiled in optimized mode. For more information, see
        https://bandit.readthedocs.io/en/1.7.5/plugins/b101_assert_used.html
    """
    check(condition, message=message, exception_cls=AssertionError)


def check(
    condition: bool, message: str = "", exception_cls: Type[Exception] = AssertionError
) -> None:
    """Check a condition, and if false, raise exception."""
    if not condition:
        raise exception_cls(message)


def ensure(arg: Optional[Any], default: Any):
    """Ensure an object is not None, or return a default."""
    return arg if arg is not None else default


def ensure_set(arg: Optional[Collection], immutable: bool = True) -> AbstractSet:
    """
    Ensure the argument is a set.

    :param arg: the set, or None.
    :param immutable: whether the collection should be immutable.
    :return: the same set, or an empty set if the arg was None.
    """
    op = frozenset if immutable else set
    return op(arg) if arg is not None else op()


def check_no_duplicates(arg: Optional[Collection]) -> Optional[Collection]:
    """Check that the argument is a set."""
    if arg is None:
        return None
    if isinstance(arg, AbstractSet):
        return arg
    seen = set()
    for x in arg:
        if x in seen:
            raise ValueError(
                f"duplicate element in collection {list(map(str, arg))}: '{str(x)}'"
            )
        seen.add(x)
    return arg


def ensure_sequence(arg: Optional[Sequence], immutable: bool = True) -> Sequence:
    """
    Ensure the argument is a sequence.

    :param arg: the list, or None.
    :param immutable: whether the collection should be immutable.
    :return: the same list, or an empty list if the arg was None.
    """
    op: Type = tuple if immutable else list
    return op(arg) if arg is not None else op()


def safe_index(seq: Sequence, *args, **kwargs):
    """Find element, safe."""
    try:
        return seq.index(*args, **kwargs)
    except ValueError:
        return None


def safe_get(seq: Sequence, index: int, default=None):
    """Get element at index, safe."""
    return seq[index] if index < len(seq) else default


def find(seq: Sequence, condition: Callable[[Any], bool]) -> int:
    """
    Find the index of the first element that satisfies a condition.

    :param seq: the sequence.
    :param condition: the condition.
    :return: the index, or -1 if no element satisfies the condition.
    """
    return next((i for i, x in enumerate(seq) if condition(x)), -1)


def _typed_parameters(parameters) -> str:
    """Return a list of parameters along with types if available."""
    result = ""
    for p in parameters:
        if p.type_tags:
            result += f"?{p.name} - {' '.join(map(str, p.type_tags))} "
        else:
            result += str(p) + " "
    return result.strip()


class RegexConstrainedString(str):
    """
    A string that is constrained by a regex.

    The default behaviour is to match anything.
    Subclass this class and change the 'REGEX' class
    attribute to implement a different behaviour.
    """

    REGEX = re.compile(".*", flags=re.DOTALL)

    def __new__(cls, value, *args, **kwargs):
        """Instantiate a new object."""
        if type(value) == cls:
            return value
        else:
            inst = super(RegexConstrainedString, cls).__new__(cls, value)
            return inst

    def __init__(self, *_, **__):
        """Initialize a regex constrained string."""
        super().__init__()
        if not self.REGEX.fullmatch(self):
            self._handle_no_match()

    def _handle_no_match(self):
        raise ValueError(
            "Value '{data}' does not match the regular expression {regex}".format(
                data=self, regex=self.REGEX
            )
        )


def find_cycle(
    graph: Dict[_Node, Optional[AbstractSet[_Node]]]
) -> Optional[Sequence[_Node]]:
    """Check whether a graph (represented as a dictionary-based adjacency list) has a cycle."""
    visited: Set = set()
    stack: List = []

    for node in graph:
        if node not in visited:
            stack.append((node, []))

            while stack:
                current, path = stack.pop()
                if current in path:
                    return path

                visited.add(current)
                neighbors = graph.get(current)
                if neighbors is not None:
                    for neighbor in neighbors:
                        stack.append((neighbor, path + [current]))

    return None


def transitive_closure(graph: Dict[_Node, Optional[_Node]]) -> Dict[_Node, Set[_Node]]:
    """Compute the transitive closure of a directed graph.

    The input graph is represented as a dictionary where the keys are the nodes
    and the values are lists of successor nodes or None if a node has no successors.
    The function returns a dictionary where the keys are the nodes and the
    values are sets of nodes that are reachable from the key node.
    :param graph: The input graph.
    :return: The transitive closure of the graph.
    """

    def dfs(node: _Node) -> None:
        """
        Perform a depth-first search (DFS) from a given node.

        This helper function is used to explore all the nodes reachable from
        the node. It iterates over each successor of the node, and if the
        successor is not already in the set of nodes reachable from the start
        node, it adds it and recursively explores its successors.
        :param node: The node from which to start the DFS.
        """
        successor = graph.get(node)
        if successor is not None and successor not in closure[node]:
            closure[node].add(successor)
            dfs(successor)

    # Initialize the closure dictionary with empty sets for each node
    # This includes nodes that are only in the values of the input graph
    closure: Dict = {
        node: set()
        for node in (graph.keys())
        | {v: set() for v in (graph.values() or set()) if v is not None}
    }

    # Perform a DFS from each node
    for node in closure:
        dfs(node)

    return closure
