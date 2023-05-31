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

"""This module contains the configurations for the tests."""
import inspect
from pathlib import Path

import mistune
import pytest

import pddl
from pddl.parser.domain import DomainParser
from pddl.parser.problem import ProblemParser

_current_filepath = inspect.getframeinfo(inspect.currentframe()).filename  # type: ignore
TEST_DIRECTORY = Path(_current_filepath).absolute().parent
ROOT_DIRECTORY = TEST_DIRECTORY.parent
LIBRARY_DIRECTORY = ROOT_DIRECTORY / pddl.__name__
DOCS_DIRECTORY = ROOT_DIRECTORY / "docs"


FIXTURES_DIR = TEST_DIRECTORY / "fixtures"
FIXTURES_PDDL_FILES = FIXTURES_DIR / "pddl_files"
BLOCKSWORLD_FILES = FIXTURES_PDDL_FILES / "blocksworld-ipc08"
TRIANGLE_FILES = FIXTURES_PDDL_FILES / "triangle-tireworld"
BLOCKSWORLD_FOND_FILES = FIXTURES_PDDL_FILES / "blocksworld_fond"

# TODO once missing features are supported, uncomment this
# DOMAIN_FILES = [
#     *FIXTURES_PDDL_FILES.glob("./**/domain.pddl")
# ]

DOMAIN_NAMES = [
    "acrobatics",
    "beam-walk",
    "blocksworld-ipc08",
    "blocksworld_fond",
    "doors",
    # "earth_observation",
    "elevators",
    # "faults-ipc08",
    # "first-responders-ipc08",
    "islands",
    "maintenance-sequential-satisficing-ipc2014",
    "miner",
    "rovers_fond",
    "spiky-tireworld",
    "tireworld",
    "tireworld-truck",
    "triangle-tireworld",
    "zenotravel",
    "something2-20BN"
]

DOMAIN_FILES = [
    FIXTURES_PDDL_FILES / domain_name / "domain.pddl" for domain_name in DOMAIN_NAMES
]

PROBLEM_FILES = [*FIXTURES_PDDL_FILES.glob("./**/p*.pddl")]


@pytest.fixture(scope="session")
def domain_parser():
    """Get the PDDL domain parser."""
    return DomainParser()


@pytest.fixture(scope="session")
def problem_parser():
    """Get the PDDL problem parser."""
    return ProblemParser()


@pytest.fixture(scope="session")
def markdown_parser():
    """Get the Mistune Markdown parser."""
    return mistune.create_markdown(renderer=mistune.AstRenderer())


#################################################
# Import PDDL fixtures
from tests.fixtures.code_objects.blocksworld_fond import (  # noqa: E402, F401
    blocksworld_fond_01,
    blocksworld_fond_domain,
)
from tests.fixtures.code_objects.blocksworld_ipc08 import (  # noqa: E402, F401
    blocksworld_domain,
    blocksworld_problem_01,
)
from tests.fixtures.code_objects.triangle_tireworld import (  # noqa: E402, F401
    triangle_tireworld_domain,
    triangle_tireworld_problem_01,
)

#################################################
