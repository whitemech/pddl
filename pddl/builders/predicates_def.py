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

"""This module implements the PredicatesDef class to handle the predicate definitions of a PDDL domain."""
from typing import Dict, AbstractSet

from pddl.builders.base import _Context, _Definition
from pddl.builders.terms_list import TermsValidator
from pddl.custom_types import name as name_type
from pddl.logic import Variable
from pddl.logic.predicates import Predicate


class PredicatesDef(_Definition):
    """A set of predicates of a PDDL domain."""

    def __init__(self, context: _Context) -> None:
        """Initialize the PDDL predicates section validator."""
        super().__init__(context)
        self._predicates_by_name: Dict[name_type, Predicate] = {}

    def add_predicate_def(self, predicate_def: Predicate) -> None:
        """Add a predicate definition."""
        self._context.check_name_not_already_used(predicate_def.name, predicate_def)
        self._check_predicates_terms(predicate_def)

        self._predicates_by_name[predicate_def.name] = predicate_def
        self._context.add_used_name(predicate_def.name, predicate_def)

    @property
    def predicates(self) -> AbstractSet[Predicate]:
        """Get the predicates."""
        return frozenset(self._predicates_by_name.values())

    @property
    def predicate_names(self) -> AbstractSet[name_type]:
        """Get the predicates names."""
        return self._predicates_by_name.keys()

    def _check_predicates_terms(self, predicates_def: Predicate) -> None:
        """Check that the terms of the predicates are consistent."""
        validator = TermsValidator(must_be_instances_of=Variable)
        for term in predicates_def.terms:
            self._check_typing_requirement_for_term(term)
            self._context.check_types_are_available(term)
            validator.add_term(term)
