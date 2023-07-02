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

"""Base module for the PDDL definitions."""
import bisect
from typing import AbstractSet, Collection, Dict, List, Mapping, Optional, Sequence, Set

from pddl.custom_types import name as name_type
from pddl.custom_types import namelike, parse_type, to_names, to_types  # noqa: F401
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import find_cycle, transitive_closure
from pddl.parser.symbols import Symbols


class MutableTypesDef:
    """A class for representing and managing the types available in a PDDL Domain."""

    def __init__(self) -> None:
        """Initialize the Types object."""
        # the types dictionary is a mapping from a type to its parent type (if any)
        self._types: Dict[name_type, Optional[name_type]] = {}

        # the set of all types
        self._all_types: Set[name_type] = set()

        # the closure of the types dictionary
        self._types_closure: Dict[name_type, Set[name_type]] = {}

        # only for printing purposes
        self._sorted_all_types: List[name_type] = []

    @property
    def raw(self) -> Mapping[name_type, Optional[name_type]]:
        """Get the raw types dictionary."""
        return self._types

    @property
    def all_types(self) -> AbstractSet[name_type]:
        """Get all available types."""
        return self._all_types

    @property
    def sorted_all_types(self) -> Sequence[name_type]:
        """Get all available types (sorted for printing purposes)."""
        return self._sorted_all_types

    def are_types_available(self, type_tags: Collection[namelike]) -> bool:
        """Check whether all the types in type_tags are available."""
        return self._all_types.issuperset(type_tags)

    def is_subtype(self, type_a: name_type, type_b: name_type) -> bool:
        """Check if type_a is a subtype of type_b."""
        # check whether type_a and type_b are legal types
        error_msg = "type {0} is not in available types {1}"
        if type_a not in self._all_types:
            raise PDDLValidationError(
                error_msg.format(repr(type_a), self._sorted_all_types)
            )
        if type_b not in self._all_types:
            raise PDDLValidationError(
                error_msg.format(repr(type_b), self._sorted_all_types)
            )

        return type_a in self._types_closure.get(type_b, set())

    def _compute_types_closure(self) -> Mapping[name_type, Set[name_type]]:
        """Compute the closure of the types dictionary."""
        return transitive_closure(self._types)

    def add_type(self, child_type: namelike, parent_type: Optional[namelike] = None):
        """
        Add a new type to the types definitions.

        Before adding the new information, this method performs the following checks:
        - both the child type and the parent type are valid types
        - the child type is not already defined
        - the child type is not `object`
        - the introduction of the new type relation does not create a cycle
        """
        # the child type is a valid type
        child_type = parse_type(child_type)
        # the parent type (if any) is a valid type
        parent_type = parse_type(parent_type) if parent_type else None

        # the child type is not already defined
        self._check_type_already_defined(child_type)

        # the child type is not `object`
        self._check_child_type_is_not_object(child_type, parent_type)

        # the introduction of the new type relation does not create a cycle
        self._check_cycle_not_created(child_type, parent_type)

        # add the new type relation
        self._add_type(child_type, parent_type)

    def _check_type_already_defined(self, child_type: name_type) -> None:
        """Check that the child type is not already defined."""
        if child_type in self._types:
            raise PDDLValidationError(
                "type '" + str(child_type) + "' is already defined"
            )

    @classmethod
    def _check_child_type_is_not_object(
        cls, child_type: name_type, parent_type: Optional[name_type]
    ) -> None:
        """Check that the child type is not `object`."""
        if child_type == Symbols.OBJECT and parent_type is not None:
            raise PDDLValidationError(
                "the type `object` must not have supertypes, but got it is a subtype of '"
                + str(parent_type)
                + "'"
            )

    def _check_cycle_not_created(
        self, child_type: name_type, parent_type: Optional[name_type]
    ) -> None:
        """Check that the introduction of the new type relation does not create a cycle."""
        # the introduction of the new type relation does not create a cycle
        if parent_type is not None:
            # TODO make it more efficient (i.e. detect cycles incrementally)
            new_types_dict = self._types.copy()
            new_types_dict[child_type] = parent_type
            cycle = find_cycle(new_types_dict)
            if cycle:
                raise PDDLValidationError(
                    "the introduction of the new type relation '"
                    + str(child_type)
                    + " is a subtype of '"
                    + str(parent_type)
                    + "' creates a cycle: "
                    + " -> ".join(map(str, cycle))
                )

    def _add_type(self, child_type: name_type, parent_type: Optional[name_type] = None):
        """Add the new type relation."""
        self._types[child_type] = parent_type
        self._all_types.add(child_type)
        self._all_types.add(parent_type) if parent_type else None
        # TODO: avoid recomputing the closure, make it incremental
        self._types_closure = self._compute_types_closure()
        bisect.insort(self._sorted_all_types, child_type)


class TypesDef(MutableTypesDef):
    pass
