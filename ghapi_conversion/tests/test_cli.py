"""
Tests for CLI parsers
"""
from os import mkdir, path, rmdir
from sys import version_info
from tempfile import gettempdir
from unittest import TestCase
from unittest.mock import patch

from ghapi_conversion.__main__ import main
from ghapi_conversion.tests.utils_for_tests import unittest_main

if version_info[0] == 2:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO


class TestCli(TestCase):
    """
    Tests whether cli parsers return the right thing
    """

    def test_file_not_found(self):
        """
        Tests whether the CLI parsers return a collection with first element being `ArgumentParser`
        """
        temp_dir = path.join(gettempdir(), "test_file_not_found")
        mkdir(temp_dir)
        sio = StringIO()
        try:
            temp_file = path.join(temp_dir, "a")
            with patch("ghapi_conversion.__main__", "main"), patch(
                "sys.stderr", sio
            ), self.assertRaises(SystemExit) as e:
                main(cli_argv=["-r", temp_file], return_args=True)
            self.assertEqual(e.exception.code, 2)
            sio.seek(0)
            self.assertTrue(
                sio.read().endswith(
                    "error: --requirement must be an existent file. Got: {!r}\n".format(
                        (temp_file,)
                    )
                )
            )
        finally:
            rmdir(temp_dir)


unittest_main()
