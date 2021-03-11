"""
Tests for CLI parsers
"""
from unittest import TestCase

from pip_req_cloner.tests.utils_for_tests import unittest_main


class TestCli(TestCase):
    """
    Tests whether cli parsers return the right thing
    """

    def test_parsers(self) -> None:
        """
        Tests whether the CLI parsers return a collection with first element being `ArgumentParser`
        """


unittest_main()
