# -*- coding: utf-8 -*-
"""
Tests for utils
"""
from codecs import open
from collections import deque
from itertools import chain
from os import mkdir, path, remove, rmdir
from sys import version_info
from tempfile import gettempdir
from unittest import TestCase

from ghapi_conversion import utils
from ghapi_conversion.tests.utils_for_tests import unittest_main

if version_info[0] == 2:

    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch


class TestUtils(TestCase):
    """
    Tests whether utils work
    """

    def test_clone_install_pip_zip_and_req(self):
        """
        Tests whether `unittest_main` is called when `__name__ == '__main__'`
        """
        self.assertEqual(type(unittest_main).__name__, "function")
        call_mock = MagicMock()
        temp_dir = path.join(gettempdir(), "test_clone_install_pip_zip_and_req")
        mkdir(temp_dir)
        temp_file = path.join(temp_dir, "a")
        try:
            with open(temp_file, "w", encoding="utf8") as f:
                f.writelines(
                    (
                        "https://api.github.com/repos/{org}/{repo}/zipball#egg={package_name}",
                        "-r https://raw.githubusercontent.com/{org}/{repo0}/{branch}/{file}",
                    )
                )
            with patch.object(utils, "call", call_mock):
                utils.clone_install_pip(temp_file)

        finally:
            remove(temp_file)
            rmdir(temp_dir)

        self.assertEqual(call_mock.call_count, 2)
        self.assertListEqual(call_mock.call_args[0][0], ["pip", "install", "."])
        self.assertEqual(
            call_mock.call_args[1]["cwd"], path.join(path.dirname(temp_dir), "{repo}")
        )

    def test_clone_install_req(self):
        """
        Tests whether `unittest_main` is called when `__name__ == '__main__'`
        """
        self.assertEqual(type(unittest_main).__name__, "function")

        def call_mock(*args, **kwargs):
            """ Mock `subprocess.call` function that does more than a `MagicMock` """
            call_mock.call_count += 1
            call_mock.call_args.append([args, kwargs])
            if args and args[0][:2] == ["git", "clone"]:
                mkdir(args[0][-1])
                created_dirs.append(args[0][-1])
                req_file = path.join(args[0][-1], "{file}")
                open(req_file, "a").close()
                created_files.append(req_file)

        call_mock.call_count = 0
        call_mock.call_args = []
        temp_dir = path.join(gettempdir(), "test_clone_install_req")
        mkdir(temp_dir)
        created_dirs = [temp_dir]
        temp_file = path.join(temp_dir, "requirements.txt")
        created_files = [temp_file]
        try:
            with open(temp_file, "w", encoding="utf8") as f:
                f.writelines(
                    "-r https://raw.githubusercontent.com/{org}/{repo}/{branch}/{file}"
                )

            with patch.object(utils, "call", call_mock):
                utils.clone_install_pip(temp_file, clone_parent_dir=temp_dir)

        finally:
            try:
                with open(temp_file, "w", encoding="utf8") as f:
                    f.writelines("mock")

                with patch.object(utils, "call", call_mock):
                    utils.clone_install_pip(temp_file, clone_parent_dir=temp_dir)

                self.assertEqual(call_mock.call_count, 2)

            finally:
                deque(
                    chain.from_iterable(
                        (map(remove, created_files), map(rmdir, reversed(created_dirs)))
                    ),
                    maxlen=0,
                )

        self.assertEqual(call_mock.call_count, 2)
        self.assertEqual(
            call_mock.call_args[0][0][0],
            [
                "git",
                "clone",
                "--depth=1",
                "-b",
                "{branch}",
                "https://github.com/{org}/{repo}",
                path.join(temp_dir, "{repo}"),
            ],
        )


unittest_main()
