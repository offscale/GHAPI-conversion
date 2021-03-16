#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
`__main__` implementation, can be run directly or with `python -m ghapi_conversion`
"""
from argparse import ArgumentParser
from collections import deque
from os import path
from sys import version_info

from ghapi_conversion import __description__, __version__
from ghapi_conversion.utils import clone_install_pip, rpartial, up_clone

if version_info[0] == 2:
    from itertools import ifilterfalse as filterfalse
else:
    from itertools import filterfalse


def _build_parser():
    """
    Parser builder

    :returns: instanceof ArgumentParser
    :rtype: ```ArgumentParser```
    """
    parser = ArgumentParser(description=__description__)
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-r",
        "--requirement",
        help="Install from the given requirements file."
        " This option can be used multiple times.",
        type=str,
        action="append",
        dest="file",
    )

    group.add_argument(
        "-l",
        "--link",
        help="Clone instead of HTTPS GET a"
        " `https://api.github.com/repos/<org>/<repo>/zipball` or"
        " `https://raw.githubusercontent.com/<org>/<repo>/<branch>` link.",
        type=str,
        action="append",
        dest="link",
    )

    return parser


def main(cli_argv=None, return_args=False):
    """
    Run the CLI parser

    :param cli_argv: CLI arguments. If None uses `sys.argv`.
    :type cli_argv: ```Optional[List[str]]```

    :param return_args: Primarily use is for tests. Returns the args rather than executing anything.
    :type return_args: ```bool```

    :returns: the args if `return_args`, else None
    :rtype: ```Optional[Namespace]```
    """
    _parser = _build_parser()
    args = _parser.parse_args(args=cli_argv)
    if args.file is not None:
        missing = tuple(filterfalse(rpartial(path.isfile), args.file))
        if missing:
            _parser.error(
                "--requirement must be an existent file. Got: {}".format(missing)
            )

    if return_args:
        return args

    deque(
        map(
            *(up_clone, args.link)
            if args.file is None
            else (clone_install_pip, args.file)
        ),
        maxlen=0,
    )


def entrypoint():
    """
    Run entrypoint when `__name__` is `"__main__"`
    """
    if __name__ == "__main__":
        main()


entrypoint()

__all__ = ["entrypoint", "main"]
