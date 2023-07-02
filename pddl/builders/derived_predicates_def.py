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

"""This module implements the DerivedPredicatesDef class to handle derivate predicate definitions of a PDDL domain."""
from typing import AbstractSet, Set

from pddl.builders.base import _Definition, _Context
from pddl.logic.predicates import DerivedPredicate


class DerivedPredicatesDef(_Definition):
    """A set of derived predicates of a PDDL domain."""

    def __init__(
        self,
        context: _Context,
    ) -> None:
        """Initialize the PDDL constants section validator."""
        super().__init__(context)

        self._derived_predicates: Set[DerivedPredicate] = set()
        self._check_consistency()

    @property
    def derived_predicates(self) -> AbstractSet[DerivedPredicate]:
        """Get the predicates."""
        return self._derived_predicates

    def _check_consistency(self) -> None:
        """Check consistency of the derived predicates definition."""

        seen_predicates_by_name: Dict[name_type, Predicate] = {
            p.name: p for p in self._predicates_def.predicates
        }
        for dp in self._derived_predicates:
            self._check_derived_predicate(dp, seen_predicates_by_name)

    def _check_derived_predicate(
        self, dp: DerivedPredicate, seen: Dict[name_type, Predicate]
    ) -> None:
        if dp.predicate.name in seen:
            other_p = seen[dp.predicate.name]
            raise PDDLValidationError(
                f"the name of derived predicate {dp} has been already used by {other_p}"
            )
        seen[dp.predicate.name] = dp.predicate
        TermsChecker(self._requirements, self._types, check_repetitions=False).check(
            dp.predicate.terms
        )
        variables = {t for t in dp.predicate.terms}
        FormulaChecker(
            self._requirements,
            self._types,
            self._constants_def.constants,
            variables,
            self._predicates_def.predicates,
            self._derived_predicates,
        ).check_formula(dp.condition)