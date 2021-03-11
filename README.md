pip-req-cloner
==============
![Python version range](https://img.shields.io/badge/python-2.7%20|%203.5%20|%203.6%20|%203.7%20|%203.8%20|%203.9%20|%203.10a5-blue.svg)
[![License](https://img.shields.io/badge/license-CC0-blue.svg)](https://creativecommons.org/publicdomain/zero/1.0)
[![Linting, testing, coverage, and release](https://github.com/offscale/pip-req-cloner/workflows/Linting,%20testing,%20coverage,%20and%20release/badge.svg)](https://github.com/offscale/pip-req-cloner/actions)
![Tested OSs, others may work](https://img.shields.io/badge/Tested%20on-Linux%20|%20macOS%20|%20Windows-green)
![Documentation coverage](.github/doccoverage.svg)
[![codecov](https://codecov.io/gh/offscale/pip-req-cloner/branch/master/graph/badge.svg)](https://codecov.io/gh/offscale/pip-req-cloner)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPi: release](https://img.shields.io/pypi/v/pip-req-cloner.svg?maxAge=3600)](https://pypi.org/project/pip-req-cloner)

CLI to replace HTTP GET on GitHub API with clones.

## Why

In GitHub Actions the macOS machines share the same IP range, meaning that users will come against the GitHub quota often. https://github.com/actions/virtual-environments/issues/602

To overcome this issue, use this tool instead of `pip install -r`. This tool `clone`s rather than `GET`s:

  - `https://api.github.com/repos/<org>/<repo>/zipball#egg=<package_name>`
  - `https://raw.githubusercontent.com/<org>/<repo>/<branch>/<file>`

Additionally, it reuses already cloned repos. 

## Install package

### PyPi

    pip install pip-req-cloner

## Development

### Install dependencies

    pip install -r requirements.txt

### Install package

    pip install -e .

## Usage

    $ python -m pip_req_cloner --help
    
    usage: __main__.py [-h] [--version] -r FILE
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -r FILE, --requirement FILE
                            Install from the given requirements file. This option
                            can be used multiple times.

---

## License

CC0.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the CC0 license, shall be
licensed under CC0, without any additional terms or conditions.
