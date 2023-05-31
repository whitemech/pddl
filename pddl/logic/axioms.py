# -*- coding: utf-8 -*-
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

"""
Core module of the package.

It contains the class definitions to build and modify PDDL domains or problems.
"""
from typing import Optional, Sequence

from pddl.helpers.base import (
    _typed_parameters,
    ensure_sequence,
)
from pddl.logic.base import Formula
from pddl.logic.terms import Variable


class Axiom:
    """A class for the PDDL Axiom."""

    def __init__(
        self,
        vars: Sequence[Variable],
        context: Optional[Formula] = None,
        implies: Optional[Formula] = None,
    ):
        """
        Initialize the axiom.

        :param vars: the axiom parameters.
        :param context: the axiom context.
        :param implies: the axiom implications.
        """
        self._vars: Sequence[Variable] = ensure_sequence(vars)
        self._context = context
        self._implies = implies

    @property
    def vars(self) -> Sequence[Variable]:
        """Get the variables."""
        return self._vars

    @property
    def context(self) -> Optional[Formula]:
        """Get the context."""
        return self._context

    @property
    def implies(self) -> Optional[Formula]:
        """Get the implications."""
        return self._implies

    def __str__(self):
        """Get the string."""
        operator_str = "(:axiom\n"
        operator_str += f"    :vars ({_typed_parameters(self.vars)})\n"
        if self.context is not None:
            operator_str += f"    :context {str(self.context)}\n"
        if self.implies is not None:
            operator_str += f"    :implies {str(self.implies)}\n"
        operator_str += ")"
        return operator_str

    def __eq__(self, other):
        """Check equality between two Axioms."""
        return (
            isinstance(other, Axiom)
            and self.vars == other.vars
            and self.context == other.context
            and self.implies == other.implies
        )

    def __hash__(self):
        """Get the hash."""
        return hash((self.vars, self.context, self.implies))
