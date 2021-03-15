# -*- coding: utf-8 -*-

"""
setup.py implementation, interesting because it parsed the first __init__.py and
    extracts the `__author__` and `__version__`
"""

from ast import parse
from codecs import open
from distutils.sysconfig import get_python_lib
from functools import partial
from os import path
from sys import version_info

from setuptools import find_packages, setup

if version_info[0] == 2:
    from itertools import ifilter as filter
    from itertools import imap as map

package_name = "ghapi_conversion"

with open(path.join(path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()


def to_funcs(*paths):
    """
    Produce function tuples that produce the local and install dir, respectively.

    :param paths: one or more str, referring to relative folder names
    :type paths: ```*paths```

    :return: 2 functions
    :rtype: ```Tuple[Callable[Optional[List[str]], str], Callable[Optional[List[str]], str]]```
    """
    return (
        partial(path.join, path.dirname(__file__), package_name, *paths),
        partial(path.join, get_python_lib(prefix=""), package_name, *paths),
    )


def main():
    """ Main function for setup.py; this actually does the installation """
    with open(
        path.join(path.abspath(path.dirname(__file__)), package_name, "__init__.py")
    ) as f:
        __author__, __version__ = map(
            lambda buf: next(map(lambda e: e.value.s, parse(buf).body)),
            filter(
                lambda line: line.startswith("__version__")
                or line.startswith("__author__"),
                f,
            ),
        )

    _data_join, _data_install_dir = to_funcs("_data")

    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        description="CLI to replace HTTP GET on GitHub API with clones",
        long_description=long_description,
        long_description_content_type="text/markdown",
        test_suite=package_name + ".tests",
        packages=find_packages(),
        package_dir={package_name: package_name},
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved",
            "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation",
            "Topic :: Software Development",
        ],
    )


def setup_py_main():
    """ Calls main if `__name__ == '__main__'` """
    if __name__ == "__main__":
        main()


setup_py_main()
