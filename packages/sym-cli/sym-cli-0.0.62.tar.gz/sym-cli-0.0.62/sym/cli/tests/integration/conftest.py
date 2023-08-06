import random
from contextlib import contextmanager

import pytest
from expects import *

from sym.cli.sym import sym as click_command
from sym.cli.tests.matchers import succeed

INSTANCES = [
    "i-052113589d5e8b832",
    "i-06ee7489efaeb582e",
    "i-0f3913172f1f4d1c0",
    "i-0ca07db4abb01d098",
    "i-0da5718079be3162c",
    "i-03371cb517e30eb22",
    "i-0e717dd52e0186713",
    "i-03c087811b23a2a4f",
    "i-08b3c84ebd6645df6",
    "i-0f5d63478e7cb781b",
]


@pytest.fixture
def integration_runner(capfdbinary, sandbox, wrapped_cli_runner):
    @contextmanager
    def context():
        runner = wrapped_cli_runner
        with sandbox.push_xdg_config_home():

            def run(*args):
                result = runner.invoke(click_command, args, catch_exceptions=False)
                cap = capfdbinary.readouterr()
                result.stdout_bytes = cap.out
                result.stderr_bytes = cap.err

                expect(result).to(succeed())
                return result

            yield run

    return context


def pytest_addoption(parser):
    parser.addoption("--email", default="ci@symops.io")
    parser.addoption("--org", default="sym")
    parser.addoption("--instance", default=random.choice(INSTANCES))
    parser.addoption("--resource", default="test")
