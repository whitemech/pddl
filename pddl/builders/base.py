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

"""This module includes the base classes for the PDDL builders."""

from abc import ABC, abstractmethod
from typing import AbstractSet, Generic, Type, TypeVar, Set, Optional, Dict, Callable

from pddl.builders.types_def import TypesDef, MutableTypesDef
from pddl.core import Domain, Problem
from pddl.custom_types import namelike
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import assert_
from pddl.logic.terms import Term
from pddl.requirements import Requirements

T = TypeVar("T", Domain, Problem)


class BaseBuilder(ABC, Generic[T]):
    """A base class for the PDDL builders."""

    @abstractmethod
    def build(self) -> T:
        """Build the PDDL object."""


class _NoDuplicateList(list):
    """A list that does not allow duplicates."""

    def __init__(
        self, item_name: str, exception_cls: Type[Exception] = PDDLValidationError
    ) -> None:
        """Initialize the list."""
        super().__init__()
        self.__item_name = item_name
        self.__exception_cls = exception_cls
        # this is for O(1) lookup
        self.__elements = set()

    def append(self, item) -> None:
        """Append an item to the list."""
        if item in self.__elements:
            raise PDDLValidationError(f"duplicate {self.__item_name}: '{item}'")
        super().append(item)
        self.__elements.add(item)

    def extend(self, iterable) -> None:
        """Extend the list with an iterable."""
        for item in iterable:
            self.append(item)

    def __contains__(self, item):
        """Check if the list contains an item."""
        return item in self.__elements

    def get_set(self) -> AbstractSet:
        """Get the set of elements."""
        return self.__elements


class _Context:
    """A context for the PDDL builders."""

    def __init__(self) -> None:
        """Initialize the context."""
        self.__requirements: _NoDuplicateList = _NoDuplicateList("requirement")
        self.__types_def: MutableTypesDef = MutableTypesDef()

        self.__used_names: Dict[namelike, object] = {}

    @property
    def requirements(self) -> AbstractSet[Requirements]:
        """Get the requirements."""
        return self.__requirements.get_set()

    @property
    def has_typing(self) -> bool:
        """Check if the typing requirement is specified."""
        return Requirements.TYPING in self.requirements

    @property
    def types_def(self) -> MutableTypesDef:
        """Get the types definition."""
        return self.__types_def

    def add_requirement(self, requirement: Requirements) -> None:
        """Add a requirement to the domain."""
        self.__requirements.append(requirement)

    def add_type(
        self, child_type: namelike, parent_type: Optional[namelike] = None
    ) -> None:
        """Add a type to the domain."""
        self.check_name_not_already_used(child_type, "type")
        self.check_name_not_already_used(parent_type, "type") if parent_type is not None else None
        self.check_typing_requirement_for_types(child_type, parent_type)

        self.__types_def.add_type(child_type, parent_type)

        self.add_used_name(child_type, "type")
        self.add_used_name(parent_type, "type") if parent_type is not None else None

    def add_used_name(self, name: namelike, obj: object) -> None:
        """Add a name to the used names."""
        self.__used_names[name] = obj

    def get_used_name(self, name: namelike) -> Optional[object]:
        """Add a name to the used names."""
        return self.__used_names.get(name)

    def check_typing_requirement_for_types(
        self, child_type: namelike, parent_type: Optional[namelike] = None
    ) -> None:
        """Check that the typing requirement is specified."""
        if not self.has_typing:
            raise PDDLValidationError(
                f"typing requirement is not specified, but the following types were used: {child_type}"
                + (f" -> {parent_type}" if parent_type else "")
            )

    def check_name_not_already_used(self, new_name: namelike, new_object: object) -> None:
        """Check that the name is not already used."""
        if new_name in self.__used_names:
            raise PDDLValidationError(
                f"name '{new_name}' of object '{new_object}' is already used for '{self.__used_names[new_name]}'"
            )

    def check_types_are_available(self, term: Term) -> None:
        """Check that the types of a term are available in the domain."""
        if not self.types_def.are_types_available(term.type_tags):
            raise PDDLValidationError(
                f"types {sorted(term.type_tags)} of term '{term}' are not in available types {self.types_def.sorted_all_types}"
            )


class _Definition:
    """Abstract class for a PDDL definition."""

    def __init__(
        self, context: _Context
    ) -> None:
        """Initialize the PDDL definition."""
        assert_(type(self) is not _Definition)
        self.__context = context

    @property
    def _context(self) -> _Context:
        """Get the context."""
        return self.__context

    @property
    def has_typing(self) -> bool:
        """Check if the typing requirement is specified."""
        return self.__context.has_typing

    def _check_typing_requirement_for_term(self, term: Term) -> None:
        """Check that the typing requirement is specified for a term."""
        if not self.has_typing and len(term.type_tags) > 0:
            raise PDDLValidationError(
                f"typing requirement is not specified, but the following types for term '{term}' were used: {term.type_tags}"
            )
