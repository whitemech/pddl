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

"""Test pddl.logic.predicates module."""
import pytest

from pddl.exceptions import PDDLValidationError
from pddl.logic import Predicate
from pddl.logic.predicates import EqualTo
from pddl.logic.terms import Constant, Variable


def test_ground_predicate_positive() -> None:
    """Test the is_ground property, positive case."""
    c1 = Constant("c1")
    assert Predicate("p", c1).is_ground


def test_ground_predicate_negative() -> None:
    """Test the is_ground property, negative case."""
    c1 = Constant("c1")
    v1 = Variable("v1")
    assert not Predicate("p", c1, v1).is_ground


def test_inconsistent_predicate_terms() -> None:
    """Test that terms of a predicate must have consistent typing."""
    with pytest.raises(
        PDDLValidationError,
        match=r"Term \?a occurred twice with different type tags: previous type tags \['t1', 't2'\], "
        r"new type tags \['t3', 't4'\]",
    ):
        a1, a2 = Variable("a", ["t1", "t2"]), Variable("a", ["t3", "t4"])
        Predicate("p", a1, a2)


def test_inconsistent_equal_to_terms() -> None:
    """Test that terms of a EqualTo atomic must have consistent typing."""
    with pytest.raises(
        PDDLValidationError,
        match=r"Term \?a occurred twice with different type tags: previous type tags \['t1', 't2'\], "
        r"new type tags \['t3', 't4'\]",
    ):
        a1, a2 = Variable("a", ["t1", "t2"]), Variable("a", ["t3", "t4"])
        EqualTo(a1, a2)
