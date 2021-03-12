# -*- coding: utf-8 -*-
"""
Tests for utils for tests
"""
from sys import version_info
from unittest import TestCase

from ghapi_conversion.tests import utils_for_tests

if version_info[0] == 2:
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


class TestUtilsForTests(TestCase):
    """
    Tests whether utils for tests work
    """

    def test_unittest_main(self):
        """
        Tests whether `unittest_main` is called when `__name__ == '__main__'`
        """
        self.assertEqual(type(utils_for_tests.unittest_main).__name__, "function")
        argparse_mock, main_mock = MagicMock(), MagicMock()

        with patch.object(utils_for_tests, "__name__", "__main__"), patch.object(
            utils_for_tests, "main", main_mock
        ):
            utils_for_tests.unittest_main()

        self.assertEqual(main_mock.call_count, 1)
        self.assertIsNone(argparse_mock.call_args)


utils_for_tests.unittest_main()
