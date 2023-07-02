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

"""This module defines validation functions for PDDL data structures."""

import functools
from collections.abc import Iterable
from typing import AbstractSet, Collection, Optional, Tuple

from pddl.action import Action
from pddl.custom_types import name as name_type
from pddl.custom_types import namelike, to_names, to_types  # noqa: F401
from pddl.definitions.types_def import TypesDef
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import check, ensure_set
from pddl.logic import Predicate
from pddl.logic.base import BinaryOp, QuantifiedCondition, UnaryOp
from pddl.logic.effects import AndEffect, Forall, When
from pddl.logic.predicates import DerivedPredicate, EqualTo
from pddl.logic.terms import Term
from pddl.requirements import Requirements


def validate(condition: bool, message: str = "") -> None:
    """
    Validate a condition regarding PDDL.

    If the condition is not satisfied, a PDDLValidationError is raised.
    """
    check(condition, message, PDDLValidationError)


def _find_inconsistencies_in_typed_terms(
    terms: Optional[Collection[Term]], all_types: AbstractSet[name_type]
) -> Optional[Tuple[Term, name_type]]:
    """
    Check that the terms in input all have legal types according to the list of available types.

    :param terms: the terms to check
    :param all_types: all available types
    :return: the type tag that raised the error, None otherwise
    """
    if terms is None:
        return None
    for term in terms:
        for type_tag in sorted(term.type_tags):
            if type_tag is not None and type_tag not in all_types:
                return term, type_tag
    return None


def _check_types_in_has_terms_objects(
    has_terms_objects: Optional[Collection[Predicate]],
    all_types: AbstractSet[name_type],
) -> None:
    """Check that the terms in the set of predicates all have legal types."""
    if has_terms_objects is None:
        return

    for has_terms in has_terms_objects:
        check_result = _find_inconsistencies_in_typed_terms(has_terms.terms, all_types)
        if check_result is not None:
            term, type_tag = check_result
            raise PDDLValidationError(
                f"type {repr(type_tag)} of term {repr(term)} in atomic expression "
                f"{repr(has_terms)} is not in available types {sorted(all_types)}"
            )


class TypeChecker:
    """Implementation of a type checker for domains and problems."""

    def __init__(
        self, types: TypesDef, requirements: Optional[AbstractSet[Requirements]] = None
    ) -> None:
        """Initialize the type checker."""
        self._types = types
        self._requirements = ensure_set(requirements)

    @property
    def has_typing(self) -> bool:
        """Check if the typing requirement is specified."""
        return Requirements.TYPING in self._requirements

    def _check_typing_requirement(self, type_tags: Collection[name_type]) -> None:
        """Check that the typing requirement is specified."""
        if not self.has_typing and len(type_tags) > 0:
            raise PDDLValidationError(
                f"typing requirement is not specified, but the following types were used: {type_tags}"
            )

    def _check_types_are_available(
        self, type_tags: Collection[name_type], what: str
    ) -> None:
        """Check that the types are available in the domain."""
        if not self._types.all_types.issuperset(type_tags):
            raise PDDLValidationError(
                f"types {sorted(type_tags)} of {what} are not in available types {sorted(self._types.all_types)}"
            )

    @functools.singledispatchmethod  # type: ignore
    def check_type(self, obj: object):
        """Check types annotations of PDDL data structures."""
        raise NotImplementedError(f"cannot check PDDL types of {type(obj)}")

    @check_type.register
    def _(self, objects: Iterable) -> None:
        """Check the types of collections of objects."""
        for obj in objects:
            self.check_type(obj)

    @check_type.register
    def _(self, term: Term) -> None:
        """Check types annotations of a PDDL term."""
        self._check_typing_requirement(term.type_tags)
        self._check_types_are_available(term.type_tags, f"term {repr(term)}")

    @check_type.register
    def _(self, predicate: Predicate) -> None:
        """Check types annotations of a PDDL predicate."""
        self.check_type(predicate.terms)

    @check_type.register
    def _(self, equal_to: EqualTo) -> None:
        """Check types annotations of a PDDL equal-to atomic formula."""
        self.check_type(equal_to.left)
        self.check_type(equal_to.right)

    @check_type.register
    def _(self, derived_predicate: DerivedPredicate) -> None:
        """Check types annotations of a PDDL derived predicate."""
        self.check_type(derived_predicate.predicate)
        self.check_type(derived_predicate.condition)

    @check_type.register
    def _(self, formula: UnaryOp) -> None:
        """Check types annotations of a PDDL unary operator."""
        self.check_type(formula.argument)

    @check_type.register
    def _(self, formula: BinaryOp) -> None:
        """Check types annotations of a PDDL binary operator."""
        self.check_type(formula.operands)

    @check_type.register
    def _(self, formula: QuantifiedCondition) -> None:
        """Check types annotations of a PDDL quantified condition."""
        self.check_type(formula.variables)
        self.check_type(formula.condition)

    @check_type.register
    def _(self, effect: AndEffect) -> None:
        """Check types annotations of a PDDL and-effect."""
        self.check_type(effect.operands)

    @check_type.register
    def _(self, effect: When) -> None:
        """Check types annotations of a PDDL when-effect."""
        self.check_type(effect.condition)
        self.check_type(effect.effect)

    @check_type.register
    def _(self, effect: Forall) -> None:
        """Check types annotations of a PDDL forall-effect."""
        self.check_type(effect.variables)
        self.check_type(effect.effect)

    @check_type.register
    def _(self, action: Action) -> None:
        """Check types annotations of a PDDL term."""
        self.check_type(action.parameters)
        self.check_type(action.precondition)
        self.check_type(action.effect)
