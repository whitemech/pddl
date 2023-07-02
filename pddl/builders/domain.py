from typing import Optional, AbstractSet

from pddl.builders.base import BaseBuilder, _Context
from pddl.builders.constants_def import ConstantsDef
from pddl.builders.derived_predicates_def import DerivedPredicatesDef
from pddl.builders.predicates_def import PredicatesDef
from pddl.custom_types import namelike
from pddl.logic import Constant, Predicate
from pddl.requirements import Requirements


class DomainBuilder(BaseBuilder):
    """A builder for PDDL domains."""

    def __init__(self, name: str):
        """Initialize the domain builder."""
        self.__name = name
        self.__context = _Context()
        self.__constants_def: ConstantsDef = ConstantsDef(self.__context)
        self.__predicates_def: PredicatesDef = PredicatesDef(self.__context)
        self.__derived_predicates_def: DerivedPredicatesDef = DerivedPredicatesDef(self.__context)

    @property
    def requirements(self) -> AbstractSet[Requirements]:
        """Get the requirements."""
        return self.__context.requirements

    @property
    def has_typing(self) -> bool:
        """Check if the typing requirement is specified."""
        return self.__context.has_typing

    def add_requirement(self, requirement: Requirements) -> "DomainBuilder":
        """Add a requirement to the domain."""
        self.__context.add_requirement(requirement)
        return self

    def add_type(
        self, child_type: namelike, parent_type: Optional[namelike] = None
    ) -> "DomainBuilder":
        """Add a type to the domain."""
        self.__context.add_type(child_type, parent_type)
        return self

    def add_constant(self, constant: Constant) -> "DomainBuilder":
        """Add a constant to the domain."""
        self.__constants_def.add_constant(constant)
        return self

    def add_predicate_def(self, predicate_def: Predicate) -> "DomainBuilder":
        """
        Add a predicate definition to the domain.

        The predicate definition must be a predicate with only variables.
        """
        self.__predicates_def.add_predicate_def(predicate_def)
        return self

    def build(self) -> "T":
        pass

    # def build(self) -> Domain:
    #     """Build the domain."""
    #     return Domain(
    #         name=self.__name,
    #         requirements=self.__requirements,
    #         types=self.types,
    #         constants=self.__constants,
    #         predicates=self.predicates,
    #         functions=self.functions,
    #         actions=self.actions,
    #         axioms=self.axioms,
    #     )
