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

"""Implementation of the PDDL domain parser."""
import sys
from typing import Dict, Set

from lark import Lark, ParseError, Transformer

from pddl.core import Action, Domain, Requirements
from pddl.exceptions import PDDLMissingRequirementError
from pddl.helpers.base import assert_, safe_get, safe_index
from pddl.logic.base import (
    And,
    ExistsCondition,
    FalseFormula,
    ForallCondition,
    Imply,
    Not,
    OneOf,
    Or,
)
from pddl.logic.effects import AndEffect, Forall, When
from pddl.logic.predicates import DerivedPredicate, EqualTo, Predicate
from pddl.logic.terms import Constant, Variable
from pddl.logic.axioms import Axiom
from pddl.parser import DOMAIN_GRAMMAR_FILE, PARSERS_DIRECTORY
from pddl.parser.symbols import Symbols


class DomainTransformer(Transformer):
    """Domain Transformer."""

    def __init__(self, *args, **kwargs):
        """Initialize the domain transformer."""
        super().__init__(*args, **kwargs)

        self._constants_by_name: Dict[str, Constant] = {}
        self._predicates_by_name: Dict[str, Predicate] = {}
        self._current_parameters_by_name: Dict[str, Variable] = {}
        self._requirements: Set[str] = set()
        self._extended_requirements: Set[str] = set()

    def start(self, args):
        """Entry point."""
        return args[0]

    def domain(self, args):
        """Process the 'domain' rule."""
        args = [arg for arg in args if arg is not None]
        kwargs = {}
        actions = []
        axioms = []
        derived_predicates = []
        for arg in args[2:-1]:
            if isinstance(arg, Action):
                actions.append(arg)
            elif isinstance(arg, Axiom):
                axioms.append(arg)
            elif isinstance(arg, DerivedPredicate):
                derived_predicates.append(arg)
            else:
                assert_(isinstance(arg, dict))
                kwargs.update(arg)
        kwargs.update(actions=actions, axioms=axioms, derived_predicates=derived_predicates)
        return Domain(**kwargs)

    def domain_def(self, args):
        """Process the 'domain_def' rule."""
        return dict(name=args[2])

    def requirements(self, args):
        """Process the 'requirements' rule."""
        self._requirements = {Requirements(r[1:]) for r in args[2:-1]}

        self._extended_requirements = set(self._requirements)
        if Requirements.STRIPS in self._requirements:
            self._extended_requirements.update(Requirements.strips_requirements())

        return dict(requirements=self._requirements)

    def types(self, args):
        """Parse the 'types' rule."""
        if not bool({Requirements.TYPING} & self._extended_requirements):
            raise PDDLMissingRequirementError(Requirements.TYPING)
        return dict(types=list(args[2].keys()))

    def constants(self, args):
        """Process the 'constant_def' rule."""
        self._constants_by_name = {
            name: Constant(name, type_tags) for name, type_tags in args[2].items()
        }
        return dict(constants=list(self._constants_by_name.values()))

    def predicates(self, args):
        """Process the 'predicates' rule."""
        predicates = args[2:-1]
        self._predicates_by_name = {p.name: p for p in predicates}
        return dict(predicates=predicates)

    def action_def(self, args):
        """Process the 'action_def' rule."""
        name = args[2]
        variables = args[4]

        # process action body
        _children = args[5].children
        action_body = {
            _children[i][1:]: _children[i + 1] for i in range(0, len(_children), 2)
        }
        return Action(name, variables, **action_body)

    def derived_predicates(self, args):
        """Process the 'derived_predicates' rule."""
        predicate = args[2]
        condition = args[3]
        return DerivedPredicate(predicate, condition)

    def action_parameters(self, args):
        """Process the 'action_parameters' rule."""
        self._current_parameters_by_name = {
            name: Variable(name, tags) for name, tags in args[1].items()
        }
        return list(self._current_parameters_by_name.values())
    
    def axiom_def(self, args):
        """Process the 'action_def' rule."""
        if not ({Requirements.DOMAIN_AXIOMS} & self._extended_requirements):
            raise PDDLMissingRequirementError(Requirements.DOMAIN_AXIOMS)

        _, _axiom, _vars, vars, children, _ = args

        # process action body
        _children = children.children
        body = {
            _children[i][1:]: _children[i + 1] for i in range(0, len(_children), 2)
        }
        return Axiom(vars, **body)

    def axiom_vars(self, args):
        """Process the 'axiom_vars' rule."""
        self._current_parameters_by_name = {
            name: Variable(name, tags) for name, tags in args[1].items()
        }
        return list(self._current_parameters_by_name.values())

    def emptyor_pregd(self, args):
        """Process the 'emptyor_pregd' rule."""
        if len(args) == 2:
            return FalseFormula()
        else:
            assert_(len(args) == 1)
            return args[0]

    def gd_not(self, args):
        """Process the 'gd' not rule."""
        if not bool(
            {Requirements.NEG_PRECONDITION, Requirements.ADL}
            & self._extended_requirements
        ):
            # raise PDDLMissingRequirementError(Requirements.NEG_PRECONDITION)
            # TODO temporary change; remove
            pass
        return Not(args[2])

    def gd_and(self, args):
        """Process the 'gd_and' rule."""
        operands = args[2:-1]
        return And(*operands)

    def gd_or(self, args):
        """Process the 'gd' or rule."""
        if not bool(
            {Requirements.DIS_PRECONDITION, Requirements.ADL}
            & self._extended_requirements
        ):
            raise PDDLMissingRequirementError(Requirements.DIS_PRECONDITION)
        operands = args[2:-1]
        return Or(*operands)

    def gd_imply(self, args):
        """Process the 'gd' imply rule."""
        if not bool(
            {Requirements.DIS_PRECONDITION, Requirements.ADL}
            & self._extended_requirements
        ):
            raise PDDLMissingRequirementError(Requirements.DIS_PRECONDITION)
        return Imply(args[2], args[3])

    def gd_quantifiers(self, args):
        """Process the 'gd' quantifiers rule."""
        req, cond_class = {
            Symbols.FORALL.value: (
                Requirements.UNIVERSAL_PRECONDITION,
                ForallCondition,
            ),
            Symbols.EXISTS.value: (
                Requirements.EXISTENTIAL_PRECONDITION,
                ExistsCondition,
            ),
        }[args[1]]
        if not bool(
            {req, Requirements.QUANTIFIED_PRECONDITION, Requirements.ADL}
            & self._extended_requirements
        ):
            raise PDDLMissingRequirementError(req)
        variables = [Variable(name, tags) for name, tags in args[3].items()]
        condition = args[5]
        return cond_class(cond=condition, variables=variables)

    def gd(self, args):
        """Process the 'gd' rule."""
        if len(args) == 1:
            return args[0]
        elif args[1] == Symbols.NOT.value:
            return self.gd_not(args)
        elif args[1] == Symbols.AND.value:
            return self.gd_and(args)
        elif args[1] == Symbols.OR.value:
            return self.gd_or(args)
        elif args[1] == Symbols.IMPLY.value:
            return self.gd_imply(args)
        elif args[1] in [Symbols.FORALL.value, Symbols.EXISTS.value]:
            return self.gd_quantifiers(args)

    def emptyor_effect(self, args):
        """Process the 'emptyor_effect' rule."""
        if len(args) == 2:
            return FalseFormula()
        else:
            return args[0]

    def effect(self, args):
        """Process the 'effect' rule."""
        if len(args) == 1:
            return args[0]
        if args[1] == Symbols.AND.value:
            return AndEffect(*args[2:-1])
        raise ValueError("case not recognized")

    def c_effect(self, args):
        """Process the 'c_effect' rule."""
        if len(args) == 1:
            return args[0]
        if args[1] == Symbols.FORALL.value:
            variables = [Variable(name, tags) for name, tags in args[3].items()]
            return Forall(effect=args[-2], variables=variables)
        if args[1] == Symbols.WHEN.value:
            return When(args[2], args[3])
        if args[1] == Symbols.ONEOF.value:
            if not bool({Requirements.NON_DETERMINISTIC} & self._extended_requirements):
                raise PDDLMissingRequirementError(Requirements.NON_DETERMINISTIC)
            return OneOf(*args[2:-1])
        raise ValueError()

    def p_effect(self, args):
        """Process the 'p_effect' rule."""
        if len(args) == 1:
            return args[0]
        else:
            return Not(args[2])

    def cond_effect(self, args):
        """Process the 'cond_effect' rule."""
        if len(args) >= 3 and args[1] == Symbols.AND.value:
            p_effects = args[2:-1]
            return And(*p_effects)
        assert_(len(args) == 1)
        return args[0]

    def atomic_formula_term(self, args):
        """Process the 'atomic_formula_term' rule."""

        def constant_or_variable(t):
            # Case where the term is a free variable (bug) or comes from a parent quantifier
            if (
                not isinstance(t, Constant)
                and t not in self._current_parameters_by_name
            ):
                return Variable(str(t), {})
            return t if isinstance(t, Constant) else self._current_parameters_by_name[t]

        if args[1] == Symbols.EQUAL.value:
            if not bool({Requirements.EQUALITY} & self._extended_requirements):
                raise PDDLMissingRequirementError(Requirements.EQUALITY)
            left = constant_or_variable(args[2])
            right = constant_or_variable(args[3])
            return EqualTo(left, right)
        else:
            name = args[1]
            terms = list(map(constant_or_variable, args[2:-1]))
            return Predicate(name, *terms)

    def constant(self, args):
        """Process the 'constant' rule."""
        assert_(len(args) == 1, "Unexpected parsing error.")
        constant = self._constants_by_name.get(args[0], None)
        if constant is None:
            raise ParseError(f"Constant '{args[0]}' not defined.")
        return constant

    def atomic_formula_skeleton(self, args):
        """Process the 'atomic_formula_skeleton' rule."""
        name = args[1]
        variable_data: Dict[str, Set[str]] = args[2]
        variables = [Variable(name, tags) for name, tags in variable_data.items()]
        return Predicate(name, *variables)

    def typed_list_name(self, args):
        """
        Process the 'typed_list_name' rule.

        Return a dictionary with as keys the names and as value a set of types for each name.

        :param args: the argument of this grammar rule
        :return: a typed list (name)
        """
        return self._typed_list_x(args)

    def typed_list_variable(self, args):
        """
        Process the 'typed_list_variable' rule.

        Return a dictionary with as keys the terms and as value a set of types for each name.

        :param args: the argument of this grammar rule
        :return: a typed list (variable)
        """
        return self._typed_list_x(args)

    def _typed_list_x(self, args):
        """Process generic 'typed_list_x' rules."""
        type_sep_index = safe_index(args, Symbols.TYPE_SEP.value)
        if type_sep_index is not None:
            objs = args[:type_sep_index]
            type_obj = args[type_sep_index + 1]
            typed_list_dict = dict()
            other_typed_list_dict = safe_get(args, type_sep_index + 2, default=dict())
            for obj in objs:
                typed_list_dict.setdefault(obj, set()).add(str(type_obj))
            return {**typed_list_dict, **other_typed_list_dict}
        elif len(args) > 0:
            return {obj: set() for obj in args}
        else:
            return {}

    def type_def(self, args):
        """Parse the 'type_def' rule."""
        if len(args) == 1:
            return args[0]
        else:
            return args[1:-1]


_domain_parser_lark = DOMAIN_GRAMMAR_FILE.read_text()


class DomainParser:
    """PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = DomainTransformer()
        self._parser = Lark(
            _domain_parser_lark, parser="lalr", import_paths=[PARSERS_DIRECTORY]
        )

    def __call__(self, text):
        """Call."""
        sys.tracebacklimit = 0  # noqa
        tree = self._parser.parse(text)
        sys.tracebacklimit = None  # noqa
        formula = self._transformer.transform(tree)
        return formula
