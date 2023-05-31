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

"""This module contains the definition to deal with symbols."""
from enum import Enum
from typing import Set

OpSymbol = str
OpRequirement = str


class Symbols(Enum):
    """A set of symbols that can be used in PDDL."""

    DEFINE = "define"
    DOMAIN = "domain"
    PROBLEM = "problem"
    AND = "and"
    OR = "or"
    NOT = "not"
    IMPLY = "imply"
    ONEOF = "oneof"
    FORALL = "forall"
    EXISTS = "exists"
    WHEN = "when"
    DERIVED = ":derived"
    DOMAIN_P = ":domain"
    OBJECTS = ":objects"
    INIT = ":init"
    GOAL = ":goal"
    REQUIREMENTS = ":requirements"
    CONSTANTS = ":constants"
    TYPES = ":types"
    PREDICATES = ":predicates"
    ACTION = ":action"
    PARAMETERS = ":parameters"
    PRECONDITION = ":precondition"
    EFFECT = ":effect"
    AXIOM = ":axiom"
    VARS = ":vars"
    CONTEXT = ":context"
    IMPLIES = ":implies"
    ROUND_BRACKET_LEFT = "("
    ROUND_BRACKET_RIGHT = ")"
    TYPE_SEP = "-"
    EQUAL = "="


ALL_SYMBOLS: Set[str] = {v.value for v in Symbols}


class RequirementSymbols(Enum):
    """A set of requirements that can be used in PDDL."""

    STRIPS = ":strips"
    TYPING = ":typing"
    NEG_PRECONDITION = ":negative-preconditions"
    DIS_PRECONDITION = ":disjunctive-preconditions"
    UNIVERSAL_PRECONDITION = ":universal-preconditions"
    EXISTENTIAL_PRECONDITION = ":existential-preconditions"
    QUANTIFIED_PRECONDITION = ":quantified-preconditions"
    EQUALITY = ":equality"
    CONDITIONAL_EFFECTS = ":conditional-effects"
    ADL = ":adl"
    DERIVED_PREDICATES = ":derived-predicates"
    NON_DETERMINISTIC = ":non-deterministic"
    DOMAIN_AXIOMS = ":domain-axioms"

    def strip(self) -> str:
        """Strip the leading colon."""
        return self.value[1:]


ALL_REQUIREMENTS: Set[str] = {v.value for v in RequirementSymbols}
