#!/usr/bin/env python

"""Tests for `fibonacci_calculator_onion` package."""


import unittest
from click.testing import CliRunner

from fibonacci_calculator_onion import fibonacci_calculator_onion
from fibonacci_calculator_onion import cli


class TestFibonacci_calculator_onion(unittest.TestCase):
    """Tests for `fibonacci_calculator_onion` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'fibonacci_calculator_onion.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
