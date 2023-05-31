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

"""This module contains tests for PDDL axioms."""

from pddl.core import Axiom


class TestAxiomSimpleInitialization:
    """Test simple axiom initialization."""

    def setup(self):
        """Set up the tests."""
        self.axiom = Axiom([])

    def test_vars(self):
        """Test the parameters getter."""
        assert self.axiom.vars == tuple()

    def test_context(self):
        """Test the precondition getter."""
        assert self.axiom.context is None

    def test_implies(self):
        """Test the implies getter."""
        assert self.axiom.implies is None
