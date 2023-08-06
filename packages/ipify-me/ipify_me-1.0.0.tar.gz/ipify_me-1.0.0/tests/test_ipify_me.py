#!/usr/bin/env python

"""Tests for `ipify_me` package."""


import unittest
from click.testing import CliRunner

# from ipify_me import ipify_me
from ipify_me import cli


class TestIpify_me(unittest.TestCase):
    """Tests for `ipify_me` package."""

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
        assert 'Your external IP' in result.output
