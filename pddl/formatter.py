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

"""Formatting utilities for PDDL domains and problems."""
from textwrap import indent
from typing import Callable, Collection, Dict, List, Mapping, Optional

from pddl.core import Domain, Problem
from pddl.custom_types import name
from pddl.logic.terms import Constant


def _remove_empty_lines(s: str) -> str:
    """Remove empty lines from string."""
    return "\n".join(filter(str.strip, s.splitlines()))


def _sort_and_print_collection(
    prefix,
    collection: Collection,
    postfix,
    to_string: Callable = str,
    is_mandatory: bool = False,
):
    if len(collection) > 0:
        return prefix + " ".join(sorted(map(to_string, collection))) + postfix
    elif is_mandatory:
        return prefix + postfix
    return ""


def _print_types_with_parents(
    prefix: str,
    types_dict: Mapping[name, Optional[name]],
    postfix: str,
    to_string: Callable = str,
):
    """Print the type dictionary of a PDDL domain."""
    name_by_type: Dict[Optional[name], List[name]] = {}
    for type_name, parent_type in types_dict.items():
        name_by_type.setdefault(parent_type, []).append(type_name)
    return _print_typed_lists(prefix, name_by_type, postfix, to_string)


def _print_constants(
    prefix, constants: Collection[Constant], postfix, to_string: Callable = str
):
    """Print constants in a PDDL domain."""
    term_by_type_tags: Dict[Optional[name], List[name]] = {}
    for c in constants:
        term_by_type_tags.setdefault(c.type_tag, []).append(c.name)

    return _print_typed_lists(prefix, term_by_type_tags, postfix, to_string)


def _print_predicates_with_types(predicates: Collection):
    result = ""
    for p in sorted(predicates):
        if p.arity == 0:
            result += f"({p.name})"
        else:
            result += f"({p.name}"
            for t in p.terms:
                if len(t.type_tags) > 1:
                    result += f" ?{t.name} - (either {' '.join(sorted(t.type_tags))})"
                else:
                    result += (
                        f" ?{t.name} - {sorted(t.type_tags)[0]}"
                        if t.type_tags
                        else f" ?{t.name}"
                    )
            result += ") "
        result += " "
    return result.strip()


def _print_typed_lists(
    prefix,
    names_by_type: Dict[Optional[name], List[name]],
    postfix,
    to_string: Callable = str,
):
    """Print typed lists."""
    result = prefix + " "

    # names with no type will be printed at the end
    names_with_none_types = names_by_type.pop(None, [])

    # print typed constants, first sorted by type, then by constant name
    for type_tag, typed_names in sorted(
        names_by_type.items(), key=lambda type_and_name: type_and_name[0]  # type: ignore
    ):
        result += (
            " ".join(sorted(to_string(n) for n in typed_names)) + " - " + type_tag + " "  # type: ignore
        )

    if len(names_with_none_types) == 0:
        return result.strip() + postfix

    # print constants with no type
    result += " ".join(sorted(to_string(n) for n in names_with_none_types))

    if result == prefix + " ":
        result = result[:-1]
    result += postfix

    return result


def domain_to_string(domain: Domain) -> str:
    """Print a PDDL domain object."""
    result = f"(define (domain {domain.name})"
    body = ""
    indentation = " " * 4
    body += _sort_and_print_collection("(:requirements ", domain.requirements, ")\n")
    body += _print_types_with_parents("(:types", domain.types, ")\n")
    body += _print_constants("(:constants", domain.constants, ")\n")
    body += f"(:predicates {_print_predicates_with_types(domain.predicates)})\n"
    body += _sort_and_print_collection(
        "",
        domain.derived_predicates,
        "",
        to_string=lambda obj: str(obj) + "\n",
    )
    body += _sort_and_print_collection(
        "",
        domain.actions,
        "",
        to_string=lambda obj: str(obj) + "\n",
    )
    result = result + "\n" + indent(body, indentation) + "\n)"
    result = _remove_empty_lines(result)
    return result


def problem_to_string(problem: Problem) -> str:
    """Print a PDDL problem object."""
    result = f"(define (problem {problem.name})"
    body = f"(:domain {problem.domain_name})\n"
    indentation = " " * 4
    body += _sort_and_print_collection("(:requirements ", problem.requirements, ")\n")
    body += _print_constants("(:objects", problem.objects, ")\n")
    body += _sort_and_print_collection(
        "(:init ", problem.init, ")\n", is_mandatory=True
    )
    body += f"{'(:goal ' + str(problem.goal) + ')'}\n"
    result = result + "\n" + indent(body, indentation) + "\n)"
    result = _remove_empty_lines(result)
    return result
