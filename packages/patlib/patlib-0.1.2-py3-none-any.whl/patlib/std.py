"""Modules from standard lib.
"""

import sys
import os
from pathlib import Path
import json
import time
import re
# import dataclasses as dcs
# from typing import Optional, Any

import builtins
import warnings
import contextlib
import subprocess

# Profiling
try:
    profile = builtins.profile     # will exists if launched via kernprof
except AttributeError:
    def profile(func): return func # provide a pass-through version.


@contextlib.contextmanager
def nonchalance(*exceptions):
    """Like contextlib.suppress(), but ignores (almost) all by default."""
    with contextlib.suppress(exceptions or Exception):
        yield

@contextlib.contextmanager
def suppress_w(warning):
    """Suppress warning messages of class `warning`."""
    warnings.simplefilter("ignore",warning)
    yield
    warnings.simplefilter("default",warning)

# Raise exception on warning
#warnings.filterwarnings('error',category=RuntimeWarning)
#warnings.filterwarnings('error',category=np.VisibleDeprecationWarning)


@contextlib.contextmanager
def rewrite(fname):
    """File-editor contextmanager.

    Example:

    >>> with rewrite("myfile.txt") as lines:
    >>>     for i, line in enumerate(lines):
    >>>         lines[i] = line.replace("old","new")
    """
    with open(fname, 'r') as f:
        lines = [line for line in f]

    yield lines

    with open(fname, 'w') as f:
        f.write("".join(lines))


class Timer():
    """Timer as contextmanager.

    Example:
    >>> with Timer('<description>'):
    >>>   do_stuff()
    """
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        #pass # Turn off timer messages
        if self.name:
            print('[%s]' % self.name, end='')
        print('Elapsed: %s' % (time.time() - self.tstart))


def sub_run(*args, check=True, capture_output=True, text=True, **kwargs):
    """`subprocess.run`, with changed defaults, returning stdout.

    Example:
    >>> gitfiles = sub_run(["git", "ls-tree", "-r", "--name-only", "HEAD"])
    >>> # Alternatively:
    >>> # gitfiles = sub_run("git ls-tree -r --name-only HEAD", shell=True)
    >>> # Only .py files:
    >>> gitfiles = [f for f in gitfiles.split("\n") if f.endswith(".py")]
    """

    x = subprocess.run(*args, **kwargs,
            check=check, capture_output=capture_output, text=text)

    if capture_output:
        return x.stdout
