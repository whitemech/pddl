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

"""This module implements the ConstantsDef class to handle the constants of a PDDL domain."""
from typing import AbstractSet, Sequence, cast

from pddl.builders.base import _Definition, _Context
from pddl.builders.terms_list import TermsValidator
from pddl.logic import Constant


class ConstantsDef(_Definition):
    """A set of constants of a PDDL domain."""

    def __init__(self, context: _Context) -> None:
        """Initialize the PDDL constants section validator."""
        super().__init__(context)
        self._terms_validator = TermsValidator(
            no_duplicates=True, must_be_instances_of=Constant
        )

    def add_constant(self, constant: Constant) -> None:
        """Add a constant."""
        self._check_typing_requirement_for_term(constant)
        self._context.check_types_are_available(constant)
        self._terms_validator.add_term(constant)

    @property
    def constants(self) -> AbstractSet[Constant]:
        """Get the constants."""
        return frozenset(cast(Sequence[Constant], self._terms_validator.terms))
