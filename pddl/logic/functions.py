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

"""This class implements PDDL functions."""
import functools
from typing import Sequence

from pddl.custom_types import namelike, parse_function
from pddl.helpers.base import assert_
from pddl.helpers.cache_hash import cache_hash
from pddl.logic.base import Atomic, BinaryOpMetaclass
from pddl.logic.terms import Term
from pddl.parser.symbols import Symbols


@cache_hash
class FunctionExpression(Atomic):
    """A class for all the function expressions."""


@cache_hash
@functools.total_ordering
class NumericFunction(FunctionExpression):
    """A class for a numeric function."""

    def __init__(self, name: namelike, *terms: Term):
        """Initialize the function."""
        self._name = parse_function(name)
        self._terms = tuple(terms)

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    @property
    def terms(self) -> Sequence[Term]:
        """Get the terms."""
        return self._terms

    @property
    def arity(self) -> int:
        """Get the arity of the function."""
        return len(self.terms)

    def __call__(self, *terms: Term):
        """Replace terms."""
        assert_(len(terms) == self.arity, "Wrong number of terms.")
        assert_(
            all(t1.type_tags == t2.type_tags for t1, t2 in zip(self.terms, terms)),
            "Wrong types of replacements.",
        )
        return NumericFunction(self.name, *terms)

    def __str__(self) -> str:
        """Get the string."""
        if self.arity == 0:
            return f"({self.name})"
        else:
            return f"({self.name} {' '.join(map(str, self.terms))})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.name}, {', '.join(map(str, self.terms))})"

    def __eq__(self, other):
        """Override equal operator."""
        return (
            isinstance(other, NumericFunction)
            and self.name == other.name
            and self.terms == other.terms
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((self.name, self.terms))

    def __lt__(self, other):
        """Override less than operator."""
        if not isinstance(other, NumericFunction):
            return NotImplemented
        return (self.name, self.terms) < (other.name, other.terms)


@cache_hash
@functools.total_ordering
class NumericValue(FunctionExpression):
    """A class for a numeric value."""

    def __init__(self, value: float) -> None:
        """Init the numeric value object."""
        if (value == float(value)):
            self._value = int(value)
        else:
            self._value = float(value)

    @property
    def value(self) -> float:
        """Get the value."""
        return self._value

    def __eq__(self, other):
        """Compare with another object."""
        return isinstance(other, NumericValue) and self.value == other.value

    def __lt__(self, other):
        """Compare with another object."""
        if not isinstance(other, NumericValue):
            return NotImplemented
        return self.value < other.value

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash(self._value)

    def __str__(self) -> str:
        """Get the string representation."""
        return str(self._value)


class BinaryFunction(FunctionExpression):
    """A class for a numeric binary function."""

    SYMBOL: Symbols

    def __init__(self, *operands: FunctionExpression):
        """
        Init a binary operator.

        :param operands: the operands.
        """
        self._operands = operands

    @property
    def operands(self) -> Sequence[FunctionExpression]:
        """Get the operands."""
        return tuple(self._operands)

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({self.SYMBOL.value} {' '.join(map(str, self.operands))})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(self.operands)})"

    def __eq__(self, other):
        """Compare with another object."""
        return isinstance(other, type(self)) and self.operands == other.operands

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.operands))


class Metric(Atomic):
    """A class for the metric function in PDDL."""

    MINIMIZE = Symbols.MINIMIZE.value
    MAXIMIZE = Symbols.MAXIMIZE.value

    def __init__(self, expression: FunctionExpression, optimization: str = MINIMIZE):
        """
        Initialize the metric.

        :param expression: functions to minimize or maximize.
        :param optimization: whether to minimize or maximize the function.
        """
        self._expression = expression
        self._optimization = optimization
        self._validate()

    @property
    def expression(self) -> FunctionExpression:
        """Get the functions."""
        return self._expression

    @property
    def optimization(self) -> str:
        """Get the optimization."""
        return self._optimization

    def _validate(self):
        """Validate the metric."""
        assert_(
            self.optimization in {self.MAXIMIZE, self.MINIMIZE},
            "Optimization metric not recognized.",
        )

    def __str__(self) -> str:
        """Get the string representation."""
        return f"{self.optimization} {self.expression}"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.expression}, {self.optimization})"  # type: ignore

    def __eq__(self, other):
        """Override equal operator."""
        return (
            isinstance(other, Metric)
            and self.expression == other.expression
            and self.optimization == other.optimization
        )

    def __hash__(self):
        """Get the hash of a Metric."""
        return hash((self.expression, self.optimization))


class EqualTo(BinaryFunction, metaclass=BinaryOpMetaclass):
    """Equal to operator."""

    SYMBOL = Symbols.EQUAL


class LesserThan(BinaryFunction):
    """Lesser than operator."""

    SYMBOL = Symbols.LESSER


class LesserEqualThan(BinaryFunction):
    """Lesser or equal than operator."""

    SYMBOL = Symbols.LESSER_EQUAL


class GreaterThan(BinaryFunction):
    """Greater than operator."""

    SYMBOL = Symbols.GREATER


class GreaterEqualThan(BinaryFunction):
    """Greater or equal than operator."""

    SYMBOL = Symbols.GREATER_EQUAL


class Assign(BinaryFunction):
    """Assign operator."""

    SYMBOL = Symbols.ASSIGN

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Assign operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class ScaleUp(BinaryFunction):
    """Scale-Up operator."""

    SYMBOL = Symbols.SCALE_UP

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Scale-Up operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class ScaleDown(BinaryFunction):
    """Scale-Down operator."""

    SYMBOL = Symbols.SCALE_DOWN

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Scale-Down operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Increase(BinaryFunction):
    """Increase operator."""

    SYMBOL = Symbols.INCREASE

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Increase operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Decrease(BinaryFunction):
    """Decrease operator."""

    SYMBOL = Symbols.DECREASE

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Decrease operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Minus(BinaryFunction, metaclass=BinaryOpMetaclass):
    """Minus operator."""

    SYMBOL = Symbols.MINUS

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Minus operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Plus(BinaryFunction, metaclass=BinaryOpMetaclass):
    """Plus operator."""

    SYMBOL = Symbols.PLUS

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Plus operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Times(BinaryFunction, metaclass=BinaryOpMetaclass):
    """Times operator."""

    SYMBOL = Symbols.TIMES

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Times operator.

        :param operands: the operands.
        """
        super().__init__(*operands)


class Divide(BinaryFunction, metaclass=BinaryOpMetaclass):
    """Divide operator."""

    SYMBOL = Symbols.DIVIDE

    def __init__(self, *operands: FunctionExpression):
        """
        Initialize the Divide operator.

        :param operands: the operands.
        """
        super().__init__(*operands)
