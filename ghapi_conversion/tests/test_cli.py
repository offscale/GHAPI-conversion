"""
Tests for CLI parsers
"""
from argparse import Namespace
from os import mkdir, path, rmdir, remove
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
        Tests whether the right error is raised when file is not found
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


    def test_file_found(self):
        """
        Tests whether the `Namespace` is set properly when file exists
        """
        temp_dir = path.join(gettempdir(), "test_file_found")
        mkdir(temp_dir)
        temp_file = path.join(temp_dir, "a")
        open(temp_file, "a").close()
        try:
            main_resp = main(cli_argv=["-r", temp_file], return_args=True)
            self.assertIsInstance(main_resp, Namespace)
            self.assertListEqual(main_resp.file, [temp_file])
        finally:
            remove(temp_file)
            rmdir(temp_dir)


unittest_main()
