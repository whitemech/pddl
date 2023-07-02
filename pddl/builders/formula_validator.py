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

"""This module implements a validator class for PDDL formulas."""

import functools
from typing import AbstractSet, Collection, Mapping

from pddl.builders.base import _Context
from pddl.builders.constants_def import ConstantsDef
from pddl.builders.predicates_def import PredicatesDef
from pddl.builders.types_def import TypesDef
from pddl.custom_types import name as name_type
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import assert_
from pddl.logic import Predicate, Variable
from pddl.logic.base import (
    BinaryOp,
    Formula,
    QuantifiedCondition,
    UnaryOp,
)
from pddl.logic.predicates import DerivedPredicate, EqualTo
from pddl.logic.terms import Constant, Term, _print_tag_set
from pddl.requirements import Requirements


class FormulaValidator:
    """Implementation of a type checker for formulas instances."""

    def __init__(
        self,
        context: _Context,
        constants: ConstantsDef,
        available_predicates: PredicatesDef,
        available_derived_predicates: Collection[DerivedPredicate],
        variables: AbstractSet[Variable],
    ) -> None:
        """Initialize the formula validator."""
        self._context = context

        # build a mapping from predicate names to predicates
        d1 = {p.name: p for p in available_predicates}
        d2 = {dp.name: dp.predicate for dp in available_derived_predicates}
        assert_(d1.keys().isdisjoint(d2.keys()))
        d1.update(d2)
        self._available_predicates_by_name: Mapping[name_type, Predicate] = d1

        # allowed constants in the formula
        self._constants_by_name = {c.name: c for c in constants}

        # allowed variables in the formula: this set might change during the type checking
        # (e.g. when checking quantifiers)
        self._current_variables_set_by_name = {v.name: v for v in variables}

    def check_formula(self, formula: Formula):
        """Check types annotations of PDDL data structures."""
        self._check_formula(formula)

    def _check_variable_is_allowed(self, variable: Variable) -> None:
        """Check that the variable is allowed in the current scope."""
        if variable.name not in self._current_variables_set_by_name:
            raise PDDLValidationError(
                f"variable {variable} is not allowed in this scope"
            )

    def _check_constant_is_defined(self, constant: Constant) -> None:
        """Check that the constant is defined."""
        self._context.constants_def.check_constant_is_defined(constant)

    def _raise_not_implemented_error(self, obj: object) -> None:
        """Raise a NotImplementedError for the given object."""
        raise NotImplementedError(f"cannot check PDDL types of {type(obj)}")

    @functools.singledispatchmethod
    def _check_formula(self, obj: object) -> None:
        self._raise_not_implemented_error(obj)

    @_check_formula.register
    def _(self, term: Term) -> None:
        """Check types annotations of a PDDL term."""
        self._check_term(term)

    @_check_formula.register
    def _(self, constant: Constant) -> None:
        """Check types annotations of a PDDL constant."""
        self._check_term(constant)
        self._check_constant_is_defined(constant)

    @_check_formula.register
    def _(self, variable: Variable) -> None:
        """Check types annotations of a PDDL variable."""
        self._check_term(variable)
        self._check_variable_is_allowed(variable)

    @_check_formula.register
    def _(self, predicate: Predicate) -> None:
        """Check types annotations of a PDDL predicate."""
        # check that the predicate is available
        if predicate.name not in self._available_predicates_by_name:
            raise PDDLValidationError(
                f"predicate {predicate.name} is not available in the domain"
            )
        # check that the predicate has the correct number of arguments
        available_predicate = self._available_predicates_by_name[predicate.name]
        if len(predicate.arguments) != len(available_predicate.arguments):
            raise PDDLValidationError(
                f"predicate {predicate.name} has {len(available_predicate.arguments)} arguments, "
                f"but {len(predicate.arguments)} arguments were given"
            )

        # check that the predicate has the correct types
        for arg, available_arg in zip(
            predicate.arguments, available_predicate.arguments
        ):
            if not arg.type_tags.issubset(available_arg.type_tags):
                raise PDDLValidationError(
                    f"predicate {predicate.name} has argument {arg} with type tags {_print_tag_set(arg.type_tags)}, "
                    f"but argument {available_arg} has type tags {_print_tag_set(arg.type_tags)}, and there is no"
                )

        # check that the predicate has valid constants and variables
        for arg in predicate.arguments:
            self._check_formula(arg)

    @_check_formula.register
    def _(self, equal_to: EqualTo) -> None:
        """Check types annotations of a PDDL equal-to atomic formula."""
        self._check_formula(equal_to.left)
        self._check_formula(equal_to.right)

    @_check_formula.register
    def _(self, derived_predicate: DerivedPredicate) -> None:
        """Check types annotations of a PDDL derived predicate."""
        self._raise_not_implemented_error(derived_predicate)

    @_check_formula.register
    def _(self, formula: UnaryOp) -> None:
        """Check types annotations of a PDDL unary operator."""
        self._check_formula(formula.argument)

    @_check_formula.register
    def _(self, formula: BinaryOp) -> None:
        """Check types annotations of a PDDL binary operator."""
        for operand in formula.operands:
            self._check_formula(operand)

    @_check_formula.register
    def _(self, formula: TrueFormula) -> None:
        """Check types annotations of a PDDL true formula."""

    @_check_formula.register
    def _(self, formula: FalseFormula) -> None:
        """Check types annotations of a PDDL false formula."""

    @_check_formula.register
    def _(self, formula: QuantifiedCondition) -> None:
        """Check types annotations of a PDDL quantified condition."""
        # quantified condition can add new variables to the scope
        # check no variable is defined twice
        for v in formula.variables:
            if v.name in self._current_variables_set_by_name:
                raise PDDLValidationError(
                    f"in scope determined by {formula}, variable {v} is already defined"
                )
            self._check_term(v)

        # add new variables to the scope
        try:
            self._current_variables_set_by_name.update(
                {v.name: v for v in formula.variables}
            )
            self._check_formula(formula.condition)
        finally:
            for v in formula.variables:
                self._current_variables_set_by_name.pop(v.name)