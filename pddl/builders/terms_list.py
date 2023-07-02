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

"""Module for validator of terms lists."""
from typing import Collection, Dict, List, Optional, Sequence, Type, Union

from pddl.custom_types import name as name_type
from pddl.exceptions import PDDLValidationError
from pddl.helpers.base import check
from pddl.logic.terms import Constant, Term, Variable, _print_tag_set


class TermsValidator:
    """Class for validator of terms."""

    def __init__(
        self,
        must_be_instances_of: Optional[Union[Type[Constant], Type[Variable]]] = None,
        no_duplicates: bool = False,
    ):
        """Initialize the validator."""

        # if none, then we don't care if constant or variable
        self._allowed_superclass = must_be_instances_of
        self._no_duplicates = no_duplicates

        # a dictionary from name to Term, for fast lookup
        self._seen: Dict[name_type, Term] = {}

        # the full list of terms
        self._terms: List[Term] = []

    @property
    def terms(self) -> Sequence[Term]:
        """Get the terms."""
        return self._terms

    @classmethod
    def check_terms(cls, terms: Collection[Term]):
        """Check that there are no duplicates."""
        TermsValidator().add_terms(terms)

    def _check_already_seen_term(self, term: Term):
        """Check whether a term has been already seen earlier in the terms list."""
        if self._no_duplicates and term.name in self._seen:
            same_name_but_different_type = type(term) is not type(  # noqa: E721
                self._seen[term.name]
            )
            check(
                same_name_but_different_type,
                f"Term '{term}' occurred twice in the same list of terms",
                exception_cls=PDDLValidationError,
            )

    def _check_same_term_has_same_type_tags(self, term: Term) -> None:
        """
        Check if the term has already been seen and, if so, that it has the same type tags.

        This is an auxiliary method to simplify the implementation of '_check_terms_consistency_iterator'.
        """
        if term.name in self._seen:
            expected_type_tags = self._seen[term.name].type_tags
            actual_type_tags = set(term.type_tags)
            check(
                expected_type_tags == actual_type_tags,
                f"Term {term} occurred twice with different type tags: "
                f"previous type tags {_print_tag_set(expected_type_tags)}, "
                f"new type tags {_print_tag_set(actual_type_tags)}",
                exception_cls=PDDLValidationError,
            )

    @classmethod
    def _check_term_type(
        cls,
        term: Term,
        term_type: Optional[Union[Type[Constant], Type[Variable]]] = None,
    ):
        """Check that the term is of the specified type."""
        if term_type is not None:
            check(
                isinstance(term, term_type),
                f"expected '{term}' being of type {term_type.__name__}; got {term.__class__.__name__} instead",
                exception_cls=PDDLValidationError,
            )

    def add_terms(self, terms: Collection[Term]) -> None:
        """Perform consistency checks and add a list of terms."""
        for term in terms:
            self.add_term(term)

    def check_term(self, term: Term) -> None:
        """
        Perform consistency checks against a single term.

        In particular:
        - if no_duplicates=Term there cannot be terms with the same name (variable or constant);
        - terms with the same name must be of the same term type (variable or constant);
        - terms with the same name must have the same type tags.
        """
        self._check_already_seen_term(term)
        self._check_same_term_has_same_type_tags(term)
        self._check_term_type(term, term_type=self._allowed_superclass)

    @classmethod
    def _terms_to_string(cls, terms: Collection[Term]) -> str:
        """Convert terms to string for error messages."""
        return "terms ['" + "', '".join(map(str, terms)) + "']"

    def add_term(self, term: Term) -> None:
        """Add a single term."""
        self.check_term(term)
        self._seen[term.name] = term
        self._terms.append(term)
