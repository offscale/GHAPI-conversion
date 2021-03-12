"""
Tests for CLI parsers
"""
from argparse import Namespace
from os import mkdir, path, remove, rmdir
from sys import version_info
from tempfile import gettempdir
from unittest import TestCase

from ghapi_conversion.__main__ import main
from ghapi_conversion.tests.utils_for_tests import unittest_main

if version_info[0] == 2:
    from mock import patch

    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from unittest.mock import patch


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

    def test_clone_install_pip_called(self):
        """
        Tests whether the `clone_install_pip` is called the right number of times
        """

        def clone_install_pip(arg):
            """
            Fake function for counting

            :param arg: Anything
            :type arg: ```Any```
            """
            clone_install_pip.called += 1

        clone_install_pip.called = 0

        temp_dir = path.join(gettempdir(), "test_clone_install_pip_called")
        mkdir(temp_dir)
        temp_file = path.join(temp_dir, "a")
        open(temp_file, "a").close()
        try:
            with patch(
                "ghapi_conversion.__main__.clone_install_pip", clone_install_pip
            ):
                main(cli_argv=["-r", temp_file])
            self.assertEqual(1, clone_install_pip.called)
        finally:
            remove(temp_file)
            rmdir(temp_dir)


unittest_main()