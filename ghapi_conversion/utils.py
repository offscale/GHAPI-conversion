# -*- coding: utf-8 -*-
"""
Utility functions
"""
from itertools import chain
from os import environ, path
from subprocess import call
from sys import version_info
from tempfile import gettempdir

if version_info[0] == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

clone_parent_dir_default = environ.get("CLONE_PARENT_DIR", gettempdir())


def up_clone(url, branch="master", clone_parent_dir=clone_parent_dir_default):
    """
    Clone if not present else reuse

    :param url: URL
    :type url: ```str```

    :param branch: Branch name
    :type branch: ```str```

    :param clone_parent_dir: Parent directory to clone everything from
    :type clone_parent_dir: ```str```

    :returns: target_dir, filename
    :rtype: ```Tuple[str, Optional[str]]```
    """
    u = urlparse(url.replace("api.github.com/repos", "github.com"))
    ball_idx = (lambda idx: idx if idx > -1 else u.path.rfind("/tarball"))(
        u.path.rfind("/zipball")
    )
    p = u.path[:ball_idx] if ball_idx > -1 else "/".join(u.path.split("/")[:3])
    target_dir = path.join(clone_parent_dir, p[p.rfind("/") + 1 :])
    if not path.isdir(target_dir):
        call(
            list(
                chain.from_iterable(
                    (
                        (
                            "git",
                            "clone",
                            "--depth=1",
                        ),
                        iter(()) if branch == "master" else ("-b", branch),
                        (
                            "{u.scheme}://{u.netloc}{p}".format(u=u, p=p),
                            target_dir,
                        ),
                    )
                )
            )
        )
    return target_dir, u.path[u.path.rfind("/") + 1 :].rstrip()


def clone_install_pip(pip_req_file, clone_parent_dir=clone_parent_dir_default):
    """
    Install requirements.txt as if no anonymous http access is required (do clones instead)

    :param pip_req_file: Filename where requirements are
    :type pip_req_file: ```str```

    :param clone_parent_dir: Parent directory to clone everything from
    :type clone_parent_dir: ```str```
    """
    with open(pip_req_file) as f:
        reqs = tuple(chain.from_iterable(map(rpartial(str.splitlines, False), f)))

    for req in reqs:
        if req.startswith("http:") or req.startswith("https:"):
            call(
                ["pip", "install", "."],
                cwd=up_clone(req, clone_parent_dir=clone_parent_dir)[0],
            )
        elif req.startswith("-r"):
            route = req[req.find("/", req.find(".")) :]
            offset, parts = 1, []
            for _ in range(3):
                next_slash = route.find("/", offset)
                parts.append(route[offset:next_slash])
                offset = next_slash + 1
            org, repo, branch = parts
            filepath = route[offset:]
            clone_install_pip(
                path.join(
                    up_clone(
                        "https://github.com/{org}/{repo}".format(org=org, repo=repo),
                        branch=branch,
                        clone_parent_dir=clone_parent_dir,
                    )[0],
                    filepath,
                )
            )
        else:
            call(["pip", "install", req])


# From https://github.com/Suor/funcy/blob/0ee7ae8/funcy/funcs.py#L34-L36
def rpartial(func, *args):
    """Partially applies last arguments."""
    return lambda *a: func(*(a + args))


__all__ = ["clone_install_pip", "rpartial"]
