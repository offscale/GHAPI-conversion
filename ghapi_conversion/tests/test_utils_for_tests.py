"""
Tests for utils for tests
"""
from io import StringIO
from sys import version_info
from unittest import TestCase, skipIf
from unittest.mock import MagicMock, patch

from ghapi_conversion.tests.utils_for_tests import unittest_main


class TestUtilsForTests(TestCase):
    """
    Tests whether utils for tests work
    """

    @skipIf(
        version_info[0] == 2,
        "`AttributeError: 'module' object has no attribute 'test_utils_for_tests'` on Python 2",
    )
    def test_unittest_main(self):
        """
        Tests whether `unittest_main` is called when `__name__ == '__main__'`
        """
        self.assertEqual(type(unittest_main).__name__, "function")
        self.assertIsNone(unittest_main())
        argparse_mock = MagicMock()
        with patch(
            "ghapi_conversion.tests.utils_for_tests.__name__", "__main__"
        ), patch("sys.stderr", new_callable=StringIO), self.assertRaises(
            SystemExit
        ) as e:
            import ghapi_conversion.tests.utils_for_tests

            ghapi_conversion.tests.utils_for_tests.unittest_main()

        self.assertIsInstance(e.exception.code, bool)
        self.assertIsNone(argparse_mock.call_args)
        self.assertIsNone(ghapi_conversion.tests.utils_for_tests.unittest_main())


unittest_main()
